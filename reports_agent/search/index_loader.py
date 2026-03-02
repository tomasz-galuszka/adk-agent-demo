import uuid

from tqdm import tqdm

from reports_agent.search.data_embedding import create_embedding
from reports_agent.search.data_extractor import load_pdf, chunk_text


def load_data(destination_collection, pdf_path):
    count = destination_collection.count()
    if count > 0:
        print(f"📦 Kolekcja zawiera już {count} dokumentów. Pomijam indeksowanie.")
        return

    print("📄 Kolekcja pusta. Rozpoczynam indeksowanie PDF...")

    text = load_pdf(pdf_path)
    chunks = chunk_text(text)

    for i, chunk in enumerate(tqdm(chunks)):
        embedding = create_embedding(chunk)

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
