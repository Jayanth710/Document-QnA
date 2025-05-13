import os
from flask import Blueprint, render_template, request, jsonify

import logging
from app.helper_functions import embedding, loader, splitter, weaviate_client, qa_pipeline
from app.database_support.database_template import DatabaseTemplate
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

logger = logging.getLogger(__name__)

def upload_api(db_template: DatabaseTemplate) -> Blueprint:
    api = Blueprint('upload_api', __name__)

    @api.route('/upload', methods=['GET','POST'])
    def upload_file():
        try:
            if request.method == 'GET':
                return render_template('upload.html')

            if request.method == 'POST':
                if not request.files:
                    return jsonify({'error': 'No file part in the request'}), 400

                file = request.files[next(iter(request.files))]

                if file.filename == '':
                    return jsonify({'error': 'No selected file'}), 400

                if file:
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(UPLOAD_FOLDER, filename))

                    text = loader.load_pdf("data/cv.pdf")

                    # Split and process text
                    raw_chunks = splitter.split_text(text)
                    sentences = splitter.build_sentence_objects(raw_chunks)
                    sentences = splitter.combine_sentences(sentences)
                    sentences, embeddings = embedding.embed_sentences(sentences)

                    # Compute distances and chunk intelligently
                    distances = splitter.calculate_distances(sentences, embeddings)
                    threshold = 0.9 * max(distances)
                    indices = [i for i, d in enumerate(distances) if d > threshold]

                    # Group into chunks
                    grouped = []
                    start = 0
                    for idx in indices:
                        group = " ".join([s['sentence'] for s in sentences[start:idx+1]])
                        grouped.append(group)
                        start = idx + 1
                    if start < len(sentences):
                        grouped.append(" ".join([s['sentence'] for s in sentences[start:]]))

                    # Weaviate init
                    client, collection = weaviate_client.init_weaviate()
                    weaviate_client.insert_chunks(collection, grouped)
                    client.close()
                    
                    return jsonify({'message': 'File uploaded successfully'}), 200
                
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return jsonify({'error': 'An error occurred during file upload'}), 500
        
    return api
        
