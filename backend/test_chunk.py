from app.services.parser_service import extract_pdf_text
from app.services.chunk_service import chunk_text

text = extract_pdf_text("uploads/sample.pdf")

chunks = chunk_text(text)

print(f"Total Chunks: {len(chunks)}")

for i, chunk in enumerate(chunks):
    print("=" * 40)
    print(f"Chunk {i+1}")
    print(chunk[:300])