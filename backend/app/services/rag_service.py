from app.services.search_service import search_documents
from app.services.llm_service import ask_llm
#from app.services.memory_service import get_last_user_message
from app.services.query_rewriter import rewrite_query

def ask_question(question: str):

   
# Rewrite question using conversation history
    search_query = rewrite_query(question)

    print("=" * 60)
    print("Original Question :", question)
    print("Rewritten Query   :", search_query)
    print("=" * 60)

    # ===== DEBUG START =====
    '''
    print("=" * 50)
    print("Previous Question :", previous_question)
    print("Current Question  :", question)
    print("Search Query      :", search_query)
    print("=" * 50)
    # ===== DEBUG END =====
    '''
    # Search relevant chunks
    results = search_documents(search_query)

    # ===== DEBUG START =====
    print("\nRetrieved Documents:")
    for i, doc in enumerate(results["documents"][0], start=1):
        print(f"\nChunk {i}:")
        print(doc[:200], "...")
    # ===== DEBUG END =====

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