import json

from groq import Groq

from app.core.config import settings


client = Groq(
    api_key=settings.GROQ_API_KEY
)


def extract_findings(
    question: str,
    sources: list[dict],
) -> dict:
    """
    Extract structured research findings from retrieved sources.
    """

    context_parts = []

    for index, source in enumerate(sources, start=1):
        context_parts.append(
            f"""
SOURCE {index}

Document:
{source.get("document", "")}

Metadata:
{source.get("metadata", {})}
"""
        )

    context = "\n\n".join(context_parts)

    prompt = f"""
You are an enterprise research analysis agent.

Analyze the provided sources and extract structured findings
for the research question.

Research Question:
{question}

Sources:
{context}

Return ONLY valid JSON in this exact structure:

{{
    "summary": "A concise summary of the research.",
    "findings": [
        {{
            "claim": "A factual claim supported by the sources.",
            "evidence": "The evidence supporting the claim.",
            "source_index": 1
        }}
    ],
    "limitations": [
        "Any important limitation or missing information."
    ]
}}

Rules:
1. Use ONLY information present in the provided sources.
2. Do not invent facts.
3. Every finding must have supporting evidence.
4. source_index must refer to one of the provided sources.
5. If the sources do not provide enough information, say so in limitations.
6. Return JSON only.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a precise enterprise research analyst."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,
    )

    content = response.choices[0].message.content.strip()

    # Handle accidental markdown code fences
    if content.startswith("```"):
        content = content.replace("```json", "")
        content = content.replace("```", "")
        content = content.strip()

    try:
        return json.loads(content)

    except json.JSONDecodeError:
        return {
            "summary": content,
            "findings": [],
            "limitations": [
                "The research model did not return valid structured JSON."
            ]
        }