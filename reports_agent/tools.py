import logging

from chromadb import QueryResult

from .search import query_company_reports

logger = logging.getLogger(__name__)

def _search_company_report(query: str) -> str:
    """Use this tool to search and analyze company reports."""

    logger.info("Searching company report with query: %s", query)
    results: QueryResult = query_company_reports(query)
    logger.info(f"Searching company report result {len(results.get("documents", [[]]))}")

    documents = results.get("documents", [[]])[0]

    if not documents:
        return "No relevant documents found."

    return "\n\n---\n\n".join(documents)
