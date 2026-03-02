import logging
import uuid

from chromadb.api.models.Collection import Collection

from .data_embedding import _create_embedding
from .data_extractor import _chunk_pdf
from .db import _chroma_client

logger = logging.getLogger(__name__)


def load_data(pdf_path):
    destination_collection = _chroma_client.get_or_create_collection(name="company_reports")
    count = destination_collection.count()

    if count > 0:
        logger.info(f"Skipped {pdf_path} indexing {destination_collection.name} has {count} documents")
        return

    logger.info(f"Starting {pdf_path} indexing...")
    _create_index(destination_collection, pdf_path)
    logger.info(f"Completed {pdf_path} indexing.")


def _create_index(destination_collection: Collection, pdf_path):
    for i, chunk in _chunk_pdf(pdf_path):
        embedding = _create_embedding(chunk)

        destination_collection.add(
            ids=[str(uuid.uuid4())],
            documents=[chunk],
            embeddings=[embedding],
            metadatas=[{
                "source": pdf_path,
                "chunk_id": i,
                "ticker": "AMB.PL",
                "company_name": "Ambra S.A."
            }]
        )
