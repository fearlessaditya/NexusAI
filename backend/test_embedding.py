from app.services.parser_service import extract_pdf_text
from app.services.langchain_chunk_service import chunk_text_langchain
from app.services.embedding_service import create_embeddings

text = extract_pdf_text("uploads/sample.pdf")

chunks = chunk_text_langchain(text)

embeddings = create_embeddings(chunks)

print(f"Total Chunks: {len(chunks)}")
print(f"Embedding Shape: {embeddings.shape}")

print("\nFirst Embedding:\n")
print(embeddings[0])