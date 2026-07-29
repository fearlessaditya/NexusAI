from app.services.parser_service import extract_pdf_text
from app.services.langchain_chunk_service import chunk_text_langchain

text = extract_pdf_text("uploads/sample.pdf")

chunks = chunk_text_langchain(text)

print(f"Total Chunks: {len(chunks)}")

for i, chunk in enumerate(chunks):
    print("=" * 50)
    print(f"Chunk {i+1}")
    print(chunk)