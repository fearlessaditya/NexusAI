import fitz
from docx import Document


def extract_pdf_text(file_path: str) -> str:

    text = ""

    pdf = fitz.open(file_path)

    for page in pdf:
        text += page.get_text()

    pdf.close()

    return text

def extract_docx_text(file_path: str) -> str:

    doc = Document(file_path)

    text = ""

    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"

    return text