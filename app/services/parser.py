import pdfplumber
from docx import Document
import io


def extract_name(text: str) -> str:
    """Assumes the first non-empty line is the candidate's name."""
    for line in text.split("\n"):
        line = line.strip()
        if line:
            return line.title()
    return "Unknown Candidate"


def parse_pdf(file_bytes: bytes) -> tuple[str, str]:
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        text = "\n".join(page.extract_text() or "" for page in pdf.pages)
    name = extract_name(text)
    return name, text.lower()


def parse_docx(file_bytes: bytes) -> tuple[str, str]:
    doc = Document(io.BytesIO(file_bytes))
    text = "\n".join([para.text for para in doc.paragraphs])
    name = extract_name(text)
    return name, text.lower()