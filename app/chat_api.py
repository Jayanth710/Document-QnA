import os
import re
import time
from flask import Flask, Response, json, request, jsonify, Blueprint

import logging
import ollama
from app.database_support.database_template import DatabaseTemplate

logger = logging.getLogger(__name__)

def chat_api(db_template: DatabaseTemplate) -> Blueprint:
    api = Blueprint('chat_api', __name__)
    # ollama_client = ollama.Client(host="http://127.0.0.1:11434")
    ollama_client = ollama.Client(host=os.getenv("OLLAMA_HOST", "http://host.docker.internal:11434"))


    @api.route('/chat', methods=['GET', 'POST'])
    def chat():
        def markdown_safe_chunks(text):
            pattern = r"(\*\*.*?\*\*|\*.*?\*|`.*?`|[-*] .+|\n\n|\n|[^\s]+|\s+)"
            return re.findall(pattern, text)

        def generate_markdown_stream(response_text):
            tokens = markdown_safe_chunks(response_text)
            for token in tokens:
                chunk = {"message": {"content": token}}
                yield f"data: {json.dumps(chunk)}\n\n"
                time.sleep(0.03)

        try:
            if request.method == 'POST':
                data = request.get_json()
                query = data.get('query', '').strip()
                if not query:
                    return jsonify({'error': 'Query is required'}), 400
                logger.info(f"Received query: {query}")

            elif request.method == 'GET':
                query = request.args.get('query', '').strip()

            def generate(query):
                response = ollama_client.chat(
                    model='llama3',
                    messages=[{'role': 'user', 'content': query}],
                    stream=True
                )

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

            return Response(generate(query), mimetype="text/event-stream")

        except Exception as e:
            logger.error(f"Error in chat API: {e}")
            return jsonify({'error': str(e)}), 500

    return api