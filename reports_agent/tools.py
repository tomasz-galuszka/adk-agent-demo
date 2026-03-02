import os
import uuid

import chromadb
import requests
from dotenv import load_dotenv
from pypdf import PdfReader
from tqdm import tqdm

load_dotenv()
EMBED_MODEL = "nomic-embed-text"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
PDF_PATH = "report.pdf"

chroma_client = chromadb.HttpClient(host=os.getenv("CHROMA_HOST"), port=int(os.getenv("CHROMA_PORT")))
collection = chroma_client.get_or_create_collection(name="company_reports")


# =====================================================
# PDF → TEXT
# =====================================================

def load_pdf(path: str) -> str:
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text


# =====================================================
# CHUNKING
# =====================================================

def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks


# =====================================================
# EMBEDDING (OLLAMA)
# =====================================================

def get_embedding(text: str):
    response = requests.post(
        f"{os.getenv("OLLAMA_API_BASE")}/api/embeddings",
        json={
            "model": EMBED_MODEL,
            "prompt": text
        }
    )
    response.raise_for_status()
    return response.json()["embedding"]


# =====================================================
# INDEKSOWANIE (AUTO START)
# =====================================================
def index_if_empty():
    try:
        count = collection.count()
    except:
        count = 0

    if count > 0:
        print(f"📦 Kolekcja zawiera już {count} dokumentów. Pomijam indeksowanie.")
        return

    print("📄 Kolekcja pusta. Rozpoczynam indeksowanie PDF...")

    text = load_pdf(PDF_PATH)
    chunks = chunk_text(text)

    for i, chunk in enumerate(tqdm(chunks)):
        embedding = get_embedding(chunk)

        collection.add(
            ids=[str(uuid.uuid4())],
            documents=[chunk],
            embeddings=[embedding],
            metadatas=[{
                "source": PDF_PATH,
                "chunk_id": i
            }]
        )

    print("✅ Indeksowanie zakończone.")


def search_company_report(query: str) -> str:
    """
    Use this tool to search and analyze company reports.
    """
    query_embedding = get_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5
    )

    documents = results.get("documents", [[]])[0]

    if not documents:
        return "Brak informacji w raporcie."

    return "\n\n---\n\n".join(documents)


index_if_empty()
