from .search import query_company_reports


def _search_company_report(query: str) -> str:
    """Use this tool to search and analyze company reports."""
    results = query_company_reports(query)
    documents = results.get("documents", [[]])[0]

    if not documents:
        return "Brak informacji w raporcie."

    return "\n\n---\n\n".join(documents)
