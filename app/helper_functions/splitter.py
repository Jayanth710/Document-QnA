# app/splitter.py
import numpy as np
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sklearn.metrics.pairwise import cosine_similarity

def split_text(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=10,
        separators=["\n\n", "\n", ".", "?", "!"],
        is_separator_regex=False
    )
    return splitter.split_text(text)

def build_sentence_objects(chunks):
    return [{'sentence': x, 'index': i} for i, x in enumerate(chunks)]

def combine_sentences(sentences, buffer_size=1):
    for i in range(len(sentences)):
        combined = ''
        for j in range(i - buffer_size, i):
            if j >= 0:
                combined += sentences[j]['sentence'] + ' '
        combined += sentences[i]['sentence']
        for j in range(i + 1, i + 1 + buffer_size):
            if j < len(sentences):
                combined += ' ' + sentences[j]['sentence']
        sentences[i]['combined_sentence'] = combined
    return sentences

def calculate_distances(sentences, embeddings):
    distances = []
    for i in range(len(sentences) - 1):
        sim = cosine_similarity([embeddings[i]], [embeddings[i + 1]])[0][0]
        distance = 1 - sim
        distances.append(distance)
        sentences[i]['distance_to_next'] = distance
    return distances
