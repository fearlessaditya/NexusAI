from app.services.search_service import search_documents
from app.services.llm_service import ask_llm


def ask_question(question: str):

    # Search relevant chunks
    results = search_documents(question)

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

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