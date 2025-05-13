import os
import re
from flask import Flask, Response, json, render_template, request, jsonify, Blueprint, stream_with_context

import logging
import weaviate
from app.database_support.database_template import DatabaseTemplate
from app.helper_functions.reranker import rerank
from app.helper_functions.embedding import get_query_embedding
from app.helper_functions.weaviate_client import init_client
from langchain_ollama import OllamaLLM
import ollama

logger = logging.getLogger(__name__)

llm = OllamaLLM(model="llama3")

def qna_api(db_template: DatabaseTemplate) -> Blueprint:
    api = Blueprint('qna_api', __name__)
    # ollama_client = ollama.Client(host="http://127.0.0.1:11434")
    ollama_client = ollama.Client(host=os.getenv("OLLAMA_HOST", "http://host.docker.internal:11434"))


    @api.route('/chat_qna', methods=['GET'])
    def chat_qna():
        return render_template('chat.html')

    @api.route('/qna', methods=['POST'])
    def qna():
        try:
            logger.info('Q&A API called')
            data = request.get_json()
            logger.info(f"Data received: {data}")
            query = data.get("query", "Summarize the profile of the user based on their interests.")
            query_vector = get_query_embedding(query)
            client = init_client()
            collection  = client.collections.get("DemoCollection")
            response = collection.query.near_vector(near_vector=query_vector, limit=4)
            top_chunks = [obj.properties["title"] for obj in response.objects]
            best_chunk = rerank(top_chunks, query)

            final_prompt = f"""You are a helpful assistant. Given the following context:
    {best_chunk}

    Answer the following question:
    {query}
    Add some additional information on top that best answers the question.
    """
            logger.info(f"Final prompt: {final_prompt}")
            
            def generate(query):
                response = ollama_client.chat(
                    model='llama3',
                    messages=[{'role': 'user', 'content': query}],
                    stream=True
                )
                logger.info(f"Response: {response}")

                # for chunk in stream:
                #     if 'message' in chunk and 'content' in chunk['message']:
                #         yield chunk['message']['content']

                buffer = ""
                for chunk in response:
                    content = chunk.get('message', {}).get('content', '')
                    buffer += content

                    if re.search(r"[\n.!?]$|^\s*[-*]\s|^\s*\d+\.\s", buffer.strip()):
                        msg = buffer.strip() + '\n'
                        yield f"data: {json.dumps({'message': {'content': msg}})}\n\n"
                        buffer = ""

                if buffer.strip():
                    msg = buffer.strip() + '\n'
                    yield f"data: {json.dumps({'message': {'content': msg}})}\n\n"
            return Response(generate(final_prompt),  mimetype='text/event-stream')
            
        except Exception as e:
            logger.error(f"Error in Q&A API: {e}")


    return api
