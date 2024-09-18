from llama_parse import LlamaParse
import os
from langchain_core.documents import Document

from langchain_text_splitters import RecursiveCharacterTextSplitter
import streamlit as st

def parse_data(file, file_name):
    try:
        #parsing_instruction = "This is a document. "  # It's good to define parsing instructions
        parser = LlamaParse(
            api_key=os.getenv("LLAMA_CLOUD_API_KEY"),
            result_type="markdown",
            #parsing_instruction=parsing_instruction,
            verbose=True
        )
        llama_parsed_documents = parser.load_data(file, extra_info={"file_name": file_name})
        if not llama_parsed_documents:
            raise Exception("llama_parsed_documents is empty")

    except Exception as e:
        raise Exception(f"Error parsing documents: {e}")

    return llama_parsed_documents

def store_data(file, file_name, vector_store):
    try:
        # Call the function to parse the data
        llama_parsed_documents = parse_data(file, file_name)

        # Combine documents into a single file
        langchain_documents = []
        part = 0 # Counter

        for doc in llama_parsed_documents:
            langchain_document = Document(
                page_content=doc.text,
                metadata={
                    "file_name": file_name,
                    "part": part
                }
            )
            langchain_documents.append(langchain_document)  # Append each document to the list
            part += 1

        # Split loaded documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=100)
        langchain_documents = text_splitter.split_documents(langchain_documents)

        # Add chunked documents to the vector store
        vector_store.add_documents(
            documents=langchain_documents
        )
        st.sidebar.success(f"Document {file_name} stored successfully")
        return True

    except Exception as e:
        st.sidebar.error(f"Error uploading {file_name} document: {e}")
        return False
