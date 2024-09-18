import streamlit as st
from src.doc_loader import store_data
from src.vector_db import create_vector_store, create_db_connection

def create_sidebar():
    # Create sidebar for loading documents
    with st.sidebar:
        st.sidebar.title("Document Loader")

        uploaded_files = st.sidebar.file_uploader("Load Documents", accept_multiple_files=True)
        if uploaded_files:  # Check if there are any uploaded files
            if st.sidebar.button("Load Documents"):
                with st.spinner("Uploading documents..."):
                    for uploaded_file in uploaded_files:
                        st.sidebar.info(f"Loading document: {uploaded_file.name}")
                        bytes_data = uploaded_file.read()
                        store_data(bytes_data, uploaded_file.name, st.session_state.vector_store)

        st.sidebar.title("Edit Documents")

        if st.sidebar.button("Clear Documents"):
            with st.spinner("Clearing documents..."):
                st.session_state.vector_store.delete_collection()
                del st.session_state['vector_store']
