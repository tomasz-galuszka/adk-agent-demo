from pypdf import PdfReader
from tqdm import tqdm

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


def _load_pdf(path: str) -> str:
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text


def _chunk_text(content: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    chunks = []
    start = 0

    while start < len(content):
        end = start + chunk_size
        chunks.append(content[start:end])
        start += chunk_size - overlap
    return chunks


def _chunk_pdf(pdf_path: str) -> enumerate[str]:
    text = _load_pdf(pdf_path)
    chunks: list[str] = _chunk_text(text)
    result: enumerate[str] = enumerate(tqdm(chunks))
    return result