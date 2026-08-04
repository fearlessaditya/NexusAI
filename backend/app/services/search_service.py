from app.services.embedding_service import create_embeddings
from app.services.vector_service import search_similar


def search_documents(
    question: str,
    top_k: int = 3,
):
    # Create embedding for user question
    query_embedding = create_embeddings([question])[0]

    # Search ChromaDB
    results = search_similar(
        query_embedding=query_embedding,
        top_k=top_k,
    )

    return results