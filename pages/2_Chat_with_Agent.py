import os
from dotenv import load_dotenv
import streamlit as st

from langchain_core.tools import Tool
from langchain.tools.retriever import create_retriever_tool
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langchain_google_community import GoogleSearchAPIWrapper
from src.vector_db import create_vector_store
from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.tools import TavilySearchResults
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_community.tools.asknews import AskNewsSearch
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from src.sidebar import create_sidebar
# Load environment variables
load_dotenv()
create_sidebar()

# Header with icon
st.header(":material/home_repair_service: Chat with Agent")

# Description with centered text
st.markdown("""
<div style="text-align: center; font-size: 1.2rem; color: #FFF; margin-bottom: 2rem;">
    The agent uses a language model as a reasoning engine to determine which actions to take and in which order.
</div>
""", unsafe_allow_html=True)


# Initialize Streamlit session state for vector store
if "vector_store" not in st.session_state:
    st.session_state.vector_store = create_vector_store("langchain", "langchain")

# Initialize chat history
if "agent_chat_history" not in st.session_state:
    st.session_state.agent_chat_history = [AIMessage(content="Hello! I can use various tools to help with your queries. How can I assist you today?")]

if st.button("Clear Chat History"):
    st.session_state.agent_chat_history = [AIMessage(content="Hello! I can use various tools to help with your queries. How can I assist you today?")]

# This is needed cause Langchain is stupid
class GoogleSearchInput(BaseModel):
    """Inputs to the Google search tool."""
    query: str = Field(
        description="query to search for in Google",
    )

# Initialize Google Search Tool
search = GoogleSearchAPIWrapper()
google_search_tool = Tool(
    name="google_search",
    description="Search Google for recent results.",
    func=search.run,
    args_schema=GoogleSearchInput,
)

# Initialize Tavily Search Tool
tavily_search_tool = TavilySearchResults(
    max_results=5,
    include_raw_content=True,
    include_answer=True,
)

# Initialize AskNews Search Tool
ask_news_search = AskNewsSearch(max_results=2)

# Initialize Retriever Tool (works but markdown is a problem)
retriever_tool = create_retriever_tool(
    retriever=st.session_state.vector_store.as_retriever(),
    name="retriever_tool",
    description="Retrieve documents from the vector store."
)


# Define all available tools
all_tools = {
    "local docs": retriever_tool,
    "web search": google_search_tool,
    "news search": ask_news_search,
}

# Select tools using Streamlit
selected_tool_names = st.multiselect(
    "Select tools to use:",
    options=list(all_tools.keys()),
    default=list(all_tools.keys())  # Select all by default
)

# Filter the selected tools based on user selection
selected_tools = [all_tools[name] for name in selected_tool_names]

# Display chat history
for message in st.session_state.agent_chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.write(message.content)
    else:
        with st.chat_message("user"):
            st.write(message.content)

llm = ChatOpenAI(temperature=0, model="gpt-4o",  streaming=False)

#prompt = hub.pull("hwchase17/openai-tools-agent")
prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are 'Company Assistant', a knowledgeable assistant who speaks in a calm and formal tone."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
agent = create_openai_tools_agent(llm, selected_tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=selected_tools, verbose=True)

# Streamlit input handling
if user_input := st.chat_input():
    # Create agent on demand

    # Write user prompt
    with st.chat_message("user"):
        st.write(user_input)
    # Write user prompt to chat history
    st.session_state.agent_chat_history.append(HumanMessage(content=user_input))

    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container())
        response = agent_executor.invoke(
            {
                "input": user_input,
                "chat_history": st.session_state.agent_chat_history
            },
            {"callbacks": [st_callback]}
        )

        output = response.get("output", "No response generated.")
        st.write(output)
    st.session_state.agent_chat_history.append(AIMessage(content=output))

        # Display the response
        #st.write(response.get("output", "No response generated."))
