import os
import uuid

import chromadb
import requests
from dotenv import load_dotenv
from google.adk.agents.llm_agent import Agent
from google.adk.models import LiteLlm
from pypdf import PdfReader
from tqdm import tqdm

load_dotenv()
MODEL = 'ollama_chat/llama3.2:latest'
EMBED_MODEL = "nomic-embed-text"

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
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

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
PDF_PATH="report.pdf"

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


# 🔥 odpala się przy starcie aplikacji
index_if_empty()

# =====================================================
# TOOL: SEARCH RAPORTU
# =====================================================

def search_company_report(query: str) -> str:
    """
    Use this tool to search inside the company annual report.
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


my_agent = Agent(
    model=LiteLlm(model=MODEL),
    name="company_rag_agent",
    description="Local RAG agent powered by Ollama and ChromaDB.",
    instruction=(
        "You are a professional financial assistant.\n\n"
        "RULES:\n"
        "1. If question relates to revenue, profit, annual report, risks, "
        "strategy or management — ALWAYS use tool 'search_company_report'.\n"
        "2. If question relates to current time — use 'get_time'.\n"
        "3. Base answer strictly on tool output when tool is used."
    ),
    tools=[search_company_report]
)
