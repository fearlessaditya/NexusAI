from app.services.search_service import hybrid_search
from app.services.llm_service import ask_llm
from app.services.query_rewriter import rewrite_query


def ask_question(question: str):

    # Rewrite question using conversation history
    search_query = rewrite_query(question)

    print("=" * 60)
    print("Original Question :", question)
    print("Rewritten Query   :", search_query)
    print("=" * 60)

    # Search relevant chunks using hybrid search
    results = hybrid_search(
        search_query,
        top_k=3,
    )

    # ===== DEBUG START =====
    print("\nRetrieved Documents:")

    for i, item in enumerate(results, start=1):

        print(f"\nChunk {i}:")
        print(item["document"][:200], "...")

        print(
            "Hybrid Score:",
            round(item["hybrid_score"], 3)
        )

    # ===== DEBUG END =====

    # Extract documents
    documents = [
        item["document"]
        for item in results
    ]

    # Extract metadata
    metadatas = [
        item["metadata"]
        for item in results
    ]

    # Merge context
    context = "\n\n".join(documents)

    # Ask LLM
    answer = ask_llm(
        question=question,
        context=context,
    )

    # Remove duplicate sources
    seen = set()
    sources = []

    for metadata in metadatas:

        key = (
            metadata["filename"],
            metadata["uploaded_by"],
        )

        if key not in seen:

            seen.add(key)

            sources.append(
                {
                    "filename": metadata["filename"],
                    "uploaded_by": metadata["uploaded_by"],
                }
            )

    return {
        "answer": answer,
        "sources": sources,
    }