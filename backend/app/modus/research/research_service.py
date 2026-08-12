from app.services.search_service import hybrid_search
from app.services.llm_service import ask_llm

from app.modus.intelligence.finding_service import (
    extract_findings,
)


def run_research(
    question: str,
    top_k: int = 5,
):
    """
    Run the MODUS research pipeline.
    """

    # ---------------------------------
    # 1. Retrieve relevant sources
    # ---------------------------------

    search_results = hybrid_search(
        question=question,
        top_k=top_k,
    )

    # ---------------------------------
    # 2. Build context
    # ---------------------------------

    context_parts = []

    for index, result in enumerate(search_results, start=1):
        document = result.get("document", "")
        metadata = result.get("metadata", {})

        context_parts.append(
            f"""
SOURCE {index}

Document:
{document}

Metadata:
{metadata}
"""
        )

    context = "\n\n".join(context_parts)

    # ---------------------------------
    # 3. Generate research answer
    # ---------------------------------

    answer = ask_llm(
        question=question,
        context=context,
    )

    # ---------------------------------
    # 4. Extract structured findings
    # ---------------------------------

    findings = extract_findings(
        question=question,
        sources=search_results,
    )

    # ---------------------------------
    # 5. Return research intelligence
    # ---------------------------------

    return {
        "question": question,
        "answer": answer,

        "findings": findings,

        "sources": [
            {
                "document": result.get("document", ""),
                "metadata": result.get("metadata", {}),
                "hybrid_score": result.get("hybrid_score"),
            }
            for result in search_results
        ],
    }