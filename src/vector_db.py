from langchain_astradb import AstraDBVectorStore
from astrapy import DataAPIClient
from astrapy.constants import VectorMetric

from langchain_openai import OpenAIEmbeddings
import os

def create_db_connection(namespace):
    client = DataAPIClient()
    database = client.get_database(
        os.getenv("ASTRA_DB_API_ENDPOINT"),
        token=os.getenv("ASTRA_DB_APPLICATION_TOKEN"),
        namespace=namespace
    )
    return database

def create_vector_store(collection_name, namespace):
    try:
        db = create_db_connection(namespace)
        collection = db.create_collection(
            "langchain",
            metric=VectorMetric.COSINE,
            dimension=1536
        )

    except Exception as e:
        print(f"Error creating collection: {e}")
        pass

    embeddings = OpenAIEmbeddings()

    vector_store = AstraDBVectorStore(
        collection_name=collection_name,
        embedding=embeddings,
        api_endpoint=os.getenv("ASTRA_DB_API_ENDPOINT"),
        token=os.getenv("ASTRA_DB_APPLICATION_TOKEN"),
        namespace=namespace,
    )

    return vector_store



