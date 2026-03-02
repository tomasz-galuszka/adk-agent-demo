import logging
import os
from typing import Any

import requests

EMBED_MODEL = "nomic-embed-text"


logger = logging.getLogger(__name__)

def _create_embedding(query: str) -> Any:
    logger.info("Creating embedding for query: %s", query)

    response = requests.post(
        f"{os.getenv("OLLAMA_API_BASE")}/api/embeddings",
        json={
            "model": EMBED_MODEL,
            "prompt": query
        }
    )
    response.raise_for_status()

    response_body = response.json()
    result = response_body["embedding"]

    logger.info(f"Created embeddings: {len(result)}")
    return result
