import json

from groq import Groq

from app.core.config import settings


client = Groq(
    api_key=settings.GROQ_API_KEY
)


def analyze_evidence(
    question: str,
    evidence: list[dict],
) -> dict:
    """
    Compare evidence and identify agreements,
    disagreements, and contradictions.
    """

    evidence_text = []

    for index, item in enumerate(evidence, start=1):
        source = item.get("source", {})

        evidence_text.append(
            f"""
EVIDENCE {index}

Claim:
{item.get("claim", "")}

Evidence:
{item.get("evidence", "")}

Source:
{source.get("metadata", {})}
"""
        )

    context = "\n\n".join(evidence_text)

    prompt = f"""
You are an enterprise research comparison agent.

Research Question:
{question}

Evidence:
{context}

Analyze the evidence.

Return ONLY valid JSON using this structure:

{{
    "agreements": [
        "Claims supported consistently by multiple sources."
    ],
    "disagreements": [
        "Claims where sources differ."
    ],
    "contradictions": [
        {{
            "claim_a": "Claim from one source.",
            "claim_b": "Conflicting claim from another source.",
            "explanation": "Why the claims conflict.",
            "source_a": 1,
            "source_b": 2
        }}
    ]
}}

Rules:
1. Use ONLY the supplied evidence.
2. Do not invent information.
3. Do not call something a contradiction unless the evidence actually conflicts.
4. If there are no contradictions, return an empty contradictions list.
5. Return valid JSON only.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a precise research comparison analyst."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,
    )

    content = response.choices[0].message.content.strip()

    if content.startswith("```"):
        content = content.replace("```json", "")
        content = content.replace("```", "")
        content = content.strip()

    try:
        return json.loads(content)

    except json.JSONDecodeError:
        return {
            "agreements": [],
            "disagreements": [],
            "contradictions": [],
        }