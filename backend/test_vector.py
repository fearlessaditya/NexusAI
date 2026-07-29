from app.services.parser_service import extract_pdf_text
from app.services.langchain_chunk_service import chunk_text_langchain
from app.services.embedding_service import create_embeddings
from app.services.vector_service import (
    store_embeddings,
    search_similar,
)

text = extract_pdf_text("uploads/sample.pdf")

chunks = chunk_text_langchain(text)

embeddings = create_embeddings(chunks)

store_embeddings(chunks, embeddings)

query = "Concurrent Engineering"

query_embedding = create_embeddings([query])[0]

results = search_similar(query_embedding)

print(results)