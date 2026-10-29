"""Module 3 · Embeddings: find the trip closest in meaning to a question.

Needs an embedding deployment in your Foundry project (EMBEDDING_DEPLOYMENT in .env).
Run:  python concepts/embeddings_demo.py "quiet nature holiday"
"""
import json
import math
import os
import sys

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()
project = AIProjectClient(
    endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)
client = project.get_openai_client()
MODEL = os.environ.get("EMBEDDING_DEPLOYMENT", "text-embedding-3-small")


def embed(texts):
    """Turn a list of texts into a list of embeddings (lists of numbers)."""
    response = client.embeddings.create(model=MODEL, input=texts)
    return [item.embedding for item in response.data]


def similarity(a, b):
    """Cosine similarity: 1.0 means the same meaning, 0 means unrelated."""
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))


trips = json.load(open("data/trip-catalog.json", encoding="utf-8"))
trip_texts = [f"{t['name']}: {t['desc']}" for t in trips]
trip_vectors = embed(trip_texts)

question = " ".join(sys.argv[1:]) or "quiet nature holiday"
question_vector = embed([question])[0]

print(f"Embedding length: {len(question_vector)} numbers")
print(f'Trips closest to "{question}":')
scores = sorted(
    ((similarity(question_vector, v), t["name"]) for v, t in zip(trip_vectors, trips)),
    reverse=True,
)
for score, name in scores[:3]:
    print(f"  {score:.3f}  {name}")
