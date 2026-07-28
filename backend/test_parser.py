from app.services.parser_service import (
    extract_pdf_text,
    extract_docx_text,
)

file_path = "uploads/sample.pdf"

text = extract_pdf_text(file_path)

print(text)