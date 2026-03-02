from chromadb import QueryResult

from .data_embedding import _create_embedding
from .db import _chroma_client


def query_company_reports(query: str) -> QueryResult:
    query_embedding = _create_embedding(query)

    collection = _chroma_client.get_or_create_collection(name="company_reports")
    return collection.query(
        query_embeddings=[query_embedding],
        n_results=5
    )
