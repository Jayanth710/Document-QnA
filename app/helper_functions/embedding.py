# app/embedder.py
# from langchain.embeddings import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer

embedder = SentenceTransformer('BAAI/bge-m3')


# embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def embed_sentences(sentences):
    texts = [s['combined_sentence'] for s in sentences]
    
    embeddings = embedder.encode(texts, normalize_embeddings=True)
    # embeddings = embedder.embed_documents(texts)
    for i, s in enumerate(sentences):
        s['combined_sentence_embedding'] = embeddings[i]
    return sentences, embeddings

def get_query_embedding(query):
    return embedder.encode(query, normalize_embeddings=True)
