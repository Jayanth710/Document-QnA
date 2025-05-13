# app/qa_pipeline.py
from app.helper_functions.reranker import rerank
from app.helper_functions.embedding import get_query_embedding
from langchain_ollama import OllamaLLM
import ollama

llm = OllamaLLM(model="llama3")

def search_and_answer(collection, query, top_k=4):
    query_vector = get_query_embedding(query)
    response = collection.query.near_vector(near_vector=query_vector, limit=top_k)
    top_chunks = [obj.properties["title"] for obj in response.objects]
    best_chunk = rerank(top_chunks, query)

    final_prompt = f"""You are a helpful assistant. Given the following context:
{best_chunk}

Answer the following question:
{query}
Add some additional information on top that best answers the question.
"""
    stream = ollama.chat(
    model='llama3',
    messages=[{'role': 'user', 'content': final_prompt}],
    stream=True
)

    for chunk in stream:
        print(chunk['message']['content'], end='', flush=True)

    # return llm.invoke(final_prompt)
