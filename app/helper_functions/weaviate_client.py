# app/weaviate_client.py
import os
from dotenv import load_dotenv
import weaviate
from weaviate.classes.config import Property, DataType, Configure
from app.helper_functions.embedding import embedder
from weaviate.classes.init import Auth
load_dotenv()

# Best practice: store your credentials in environment variables
weaviate_url = os.environ["WEAVIATE_URL"]
weaviate_api_key = os.environ["WEAVIATE_API_KEY"]

def init_client():
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=weaviate_url,
        auth_credentials=Auth.api_key(weaviate_api_key),
    )
    return client

def init_weaviate():
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=weaviate_url,
        auth_credentials=Auth.api_key(weaviate_api_key),
    )
    if client.collections.exists("DemoCollection"):
        client.collections.delete("DemoCollection")

    collection = client.collections.create(
        name="DemoCollection",
        properties=[Property(name="title", data_type=DataType.TEXT)],
        vector_index_config=Configure.VectorIndex.hnsw(),
        # generative_config=Configure.Generative.ollama(
        #     api_endpoint="http://localhost:11434",
        #     model="llama3"
        # )
    )
    return client, collection

def insert_chunks(collection, chunks):
    for chunk in chunks:
        vector = embedder.encode(chunk)
        collection.data.insert(properties={"title": chunk}, vector=vector)
