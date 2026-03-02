import uuid

from tqdm import tqdm

from .data_embedding import _create_embedding
from .data_extractor import _chunk_text, _load_pdf
from .db import _chroma_client


def load_data(pdf_path):
    destination_collection = _chroma_client.get_or_create_collection(name="company_reports")
    count = destination_collection.count()
    if count > 0:
        print(f"📦 Kolekcja zawiera już {count} dokumentów. Pomijam indeksowanie.")
        return

    print("📄 Kolekcja pusta. Rozpoczynam indeksowanie PDF...")

    text = _load_pdf(pdf_path)
    chunks = _chunk_text(text)

    for i, chunk in enumerate(tqdm(chunks)):
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

    print("✅ Indeksowanie zakończone.")
