"""Search module - handles PDF indexing and vector search."""

from .index_loader import load_data
from .index_repository import query_company_reports

__all__ = [
    'load_data',
    'query_company_reports',
]