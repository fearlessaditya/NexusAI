def build_evidence_map(
    findings: dict,
    sources: list[dict],
) -> list[dict]:
    """
    Map each research finding back to its retrieved source.
    """

    evidence_map = []

    for finding in findings.get("findings", []):
        source_index = finding.get("source_index")

        source = None

        if (
            isinstance(source_index, int)
            and 1 <= source_index <= len(sources)
        ):
            source = sources[source_index - 1]

        evidence_map.append(
            {
                "claim": finding.get("claim", ""),
                "evidence": finding.get("evidence", ""),
                "source_index": source_index,
                "source": {
                    "document": (
                        source.get("document", "")
                        if source
                        else ""
                    ),
                    "metadata": (
                        source.get("metadata", {})
                        if source
                        else {}
                    ),
                    "hybrid_score": (
                        source.get("hybrid_score")
                        if source
                        else None
                    ),
                },
            }
        )

    return evidence_map