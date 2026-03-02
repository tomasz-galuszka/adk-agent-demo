import os

import requests

EMBED_MODEL = "nomic-embed-text"


def _create_embedding(text: str):
    response = requests.post(
        f"{os.getenv("OLLAMA_API_BASE")}/api/embeddings",
        json={
            "model": EMBED_MODEL,
            "prompt": text
        }
    )
    response.raise_for_status()
    return response.json()["embedding"]
