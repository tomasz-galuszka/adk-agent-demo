from chromadb import QueryResult

from reports_agent.search.data_embedding import create_embedding
from reports_agent.search.db import chroma_client


def query_company_reports(query: str) -> QueryResult:
    collection = chroma_client.get_or_create_collection(name="company_reports")
    query_embedding = create_embedding(query)
    return collection.query(
        query_embeddings=[query_embedding],
        n_results=5
    )
