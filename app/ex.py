# import requests

# def query(payload):
#     response = requests.post(API_URL, headers=headers, json=payload)
#     return response.json()

# output = query({"inputs": "What's the meaning of life?"})
# print(output)
from sentence_transformers import SentenceTransformer, util

# Load the model (supports both HF hub and local path)
model = SentenceTransformer("BAAI/bge-m3")

# Sentences to compare
query = "What is artificial intelligence?"
candidates = ["AI is about simulating human intelligence.", "Bananas are yellow."]

# Get embeddings
query_embedding = model.encode(query, convert_to_tensor=True)
candidate_embeddings = model.encode(candidates, convert_to_tensor=True)

# Compute cosine similarity
cos_scores = util.cos_sim(query_embedding, candidate_embeddings)

# Print similarity scores
for sentence, score in zip(candidates, cos_scores[0]):
    print(f"{sentence} \n Score: {score.item():.4f}")


from sentence_transformers import CrossEncoder

# Load the reranker model
reranker = CrossEncoder("BAAI/bge-reranker-large")

# Define query and candidate passages
query = "What is artificial intelligence?"
passages = [
    "AI is about simulating human intelligence.",
    "Bananas are yellow.",
    "Machine learning is a subset of AI."
]

# Prepare (query, passage) pairs
pairs = [(query, passage) for passage in passages]

# Get relevance scores
scores = reranker.predict(pairs)

# Show results
for passage, score in sorted(zip(passages, scores), key=lambda x: x[1], reverse=True):
    print(f"{score:.4f} - {passage}")
