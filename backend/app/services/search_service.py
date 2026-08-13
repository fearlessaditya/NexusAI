from app.services.embedding_service import create_embeddings
from app.services.vector_service import (
    search_similar,
    get_all_documents,
)


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

import re

from app.services.embedding_service import create_embeddings
from app.services.vector_service import (
    search_similar,
    get_all_documents,
)


def search_documents(
    question: str,
    top_k: int = 3,
):
    query_embedding = create_embeddings([question])[0]

    results = search_similar(
        query_embedding=query_embedding,
        top_k=top_k,
    )

    return results


def keyword_search(
    question: str,
    top_k: int = 3,
):
    # Get all stored chunks
    results = get_all_documents()

    documents = results["documents"]
    metadatas = results["metadatas"]

    # Common words that should not affect keyword score
    stopwords = {
        "what",
        "are",
        "is",
        "the",
        "a",
        "an",
        "does",
        "do",
        "did",
        "of",
        "to",
        "in",
        "on",
        "for",
        "and",
        "or",
        "its",
        "their",
        "this",
        "that",
        "how",
        "why",
        "which",
        "with",
    }

    # Extract meaningful words
    keywords = re.findall(
        r"\b[a-zA-Z]+\b",
        question.lower(),
    )

    keywords = [
        keyword
        for keyword in keywords
        if keyword not in stopwords
    ]

    scored_documents = []

    for document, metadata in zip(
        documents,
        metadatas,
    ):
        text = document.lower()

        score = 0

        for keyword in keywords:
            if keyword in text:
                score += 1

        if score > 0:
            scored_documents.append(
                {
                    "document": document,
                    "metadata": metadata,
                    "score": score,
                }
            )

    # Highest score first
    scored_documents.sort(
        key=lambda x: x["score"],
        reverse=True,
    )

    return scored_documents[:top_k]


def hybrid_search(
    question: str,
    top_k: int = 3,
):
    # -------------------------
    # 1. Vector Search
    # -------------------------
    vector_results = search_documents(
        question,
        top_k=top_k,
    )

    vector_documents = vector_results["documents"][0]
    vector_metadatas = vector_results["metadatas"][0]
    vector_distances = vector_results["distances"][0]

    # -------------------------
    # 2. Keyword Search
    # -------------------------
    keyword_results = keyword_search(
        question,
        top_k=top_k,
    )

    # -------------------------
    # 3. Combine results
    # -------------------------
    combined = {}

    # Add vector results
    for document, metadata, distance in zip(
        vector_documents,
        vector_metadatas,
        vector_distances,
    ):
        combined[document] = {
            "document": document,
            "metadata": metadata,
            "vector_distance": distance,
            "keyword_score": 0,
        }

    # Add keyword results
    for item in keyword_results:

        document = item["document"]

        if document not in combined:
            combined[document] = {
                "document": document,
                "metadata": item["metadata"],
                "vector_distance": None,
                "keyword_score": item["score"],
            }
        else:
            combined[document]["keyword_score"] = item["score"]

    # -------------------------
    # 4. Calculate hybrid score
    # -------------------------
    # -------------------------
# 4. Normalize scores
# -------------------------

    max_keyword_score = max(
        [item["keyword_score"] for item in combined.values()],
        default=1,
    )

    max_vector_score = max(
        [
            1 / (1 + item["vector_distance"])
            for item in combined.values()
            if item["vector_distance"] is not None
        ],
        default=1,
    )


    for item in combined.values():

        # Vector similarity
        if item["vector_distance"] is not None:
            vector_score = 1 / (
                1 + item["vector_distance"]
            )
        else:
            vector_score = 0

        # Normalize vector score
        vector_score = vector_score / max_vector_score

        # Normalize keyword score
        if max_keyword_score > 0:
            keyword_score = (
            item["keyword_score"]
            / max_keyword_score
        )
        else:
            keyword_score = 0

        # Final hybrid score
        item["hybrid_score"] = (
            0.7 * vector_score
            + 0.3 * keyword_score
        )

    # -------------------------
    # 5. Sort
    # -------------------------
    ranked_results = sorted(
        combined.values(),
        key=lambda x: x["hybrid_score"],
        reverse=True,
    )

    return ranked_results[:top_k]