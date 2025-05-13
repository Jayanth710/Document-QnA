# app/reranker.py
from langchain_ollama import OllamaLLM
llm = OllamaLLM(model="llama3")
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# tokenizer = AutoTokenizer.from_pretrained("app/models/bge-reranker-large")
# model = AutoModelForSequenceClassification.from_pretrained("app/models/bge-reranker-large")
# model.eval()
tokenizer = AutoTokenizer.from_pretrained("BAAI/bge-reranker-large")
model = AutoModelForSequenceClassification.from_pretrained("BAAI/bge-reranker-large")
model.eval()

def rerank(chunks, question, top_k=3):
    # Create query-document pairs
    pairs = [(question, chunk) for chunk in chunks]

    # Tokenize
    inputs = tokenizer(pairs, padding=True, truncation=True, return_tensors="pt")

    with torch.no_grad():
        scores = model(**inputs).logits.squeeze(-1)

    # Score and sort
    scored_chunks = list(zip(chunks, scores.tolist()))
    sorted_chunks = sorted(scored_chunks, key=lambda x: x[1], reverse=True)

    # Return top_k chunks only
    return [chunk for chunk, _ in sorted_chunks[:top_k]]