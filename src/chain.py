from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

def get_conversational_chain():
    llm = ChatOpenAI()

    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are 'Company Assistant', a wise and knowledgeable assistant who speaks in a calm and formal tone."
         "Answer the user's questions"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}")
    ])

    chain = prompt | llm | StrOutputParser()
    final_chain = (RunnablePassthrough.assign(answer=chain))
    return final_chain


def get_retriever_chain(vector_store, top_k=8, score_threshold=0.5):
  llm = ChatOpenAI(model="gpt-4o")
  retriever = vector_store.as_retriever(search_kwargs={"k": top_k, "score_threshold": score_threshold})
  rephrase_prompt = ChatPromptTemplate.from_messages([
      MessagesPlaceholder(variable_name="chat_history"),
      ("user","{input}"),
      ("user","Given the above conversation, generate a search query to look up in order to get information relevant to the conversation")
  ])
  history_retriever_chain = create_history_aware_retriever(llm, retriever, rephrase_prompt)

  return history_retriever_chain

#Returns conversational rag
def get_conversational_rag(history_retriever_chain):
  llm = ChatOpenAI(model="gpt-4o")
  answer_prompt=ChatPromptTemplate.from_messages([
      ("system",
       "You are 'Company Assistant', a wise and knowledgeable assistant who speaks in a calm and formal tone."
       "Answer user's questions based on the below context:"
       "\n\n{context}"),
      MessagesPlaceholder(variable_name="chat_history"),
      ("user","{input}")
  ])

  document_chain = create_stuff_documents_chain(llm, answer_prompt)

  #create final retrieval chain
  conversational_retrieval_chain = create_retrieval_chain(history_retriever_chain, document_chain)

  return conversational_retrieval_chain