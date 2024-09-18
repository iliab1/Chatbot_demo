from langchain_core.messages import HumanMessage, AIMessage
from src.chain import get_retriever_chain, get_conversational_rag, get_conversational_chain
from src.vector_db import create_vector_store
from src.sidebar import create_sidebar
import streamlit as st
from dotenv import load_dotenv
load_dotenv()
create_sidebar()

st.header(":material/folder_open: Chat with Documents")

st.markdown("""
<div style="text-align: center; font-size: 1.2rem; color: #FFF; margin-bottom: 2rem;">
    This assistant uses Retrieval-Augmented Generation (RAG) to provide
    context-aware responses by retrieving relevant information from your documents.
</div>
""", unsafe_allow_html=True)

def get_response(user_input):
    if is_rag:
        history_retriever_chain = get_retriever_chain(st.session_state.vector_store)
        conversation_rag_chain = get_conversational_rag(history_retriever_chain)

        # Returns a generator for streaming
        return conversation_rag_chain.stream({
            "chat_history": st.session_state.chat_history,
            "input": user_input
        })
    else:
        conversation_chain = get_conversational_chain()

        # Returns a generator for streaming
        return conversation_chain.stream({
            "chat_history": st.session_state.chat_history,
            "input": user_input
        })




# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [AIMessage(content="Hello! How can I assist you today?")]

if st.button("Clear Chat History"):
    st.session_state.chat_history = [AIMessage(content="Hello! How can I assist you today?")]

# Select strategy
is_rag = st.toggle("Search Locally") # Toggle between RAG and regular conversation

# Initialize vector store
if "vector_store" not in st.session_state:
    st.session_state.vector_store = create_vector_store("langchain", "langchain")

full_response = ""
def generate_responses(completion):
    global full_response
    for chunk in completion:
        response = chunk.get('answer', '')  # Extract 'answer' from the chunk
        if response:
            full_response += response  # Append to the full response
            yield response

## Chat interface
# Get input from user
user_input = st.chat_input("Type your message here...")

# Display chat history
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.write(message.content)
    else:
        with st.chat_message("Human"):
            st.write(message.content)

# If there's user input
if user_input is not None and user_input.strip() != "":

    # Write user input and add to chat history
    with st.chat_message("Human"):
        st.write(user_input)
    # Add user message to chat history
    st.session_state.chat_history.append(HumanMessage(content=user_input))

    # Write response
    with st.chat_message("AI"):
        # Stream the response using the generator
        stream = generate_responses(get_response(user_input))
        st.write_stream(stream)
    # Add AI message to chat history
    st.session_state.chat_history.append(AIMessage(content=full_response))



