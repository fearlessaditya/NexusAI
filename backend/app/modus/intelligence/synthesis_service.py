import json

from groq import Groq

from app.core.config import settings


client = Groq(
    api_key=settings.GROQ_API_KEY
)


def generate_conclusion(
    question: str,
    findings: dict,
    comparison: dict,
) -> dict:
    """
    Generate a final research conclusion from
    structured findings and evidence comparison.
    """

    prompt = f"""
You are an enterprise research synthesis agent.

Research Question:
{question}

Research Findings:
{json.dumps(findings, indent=2)}

Evidence Comparison:
{json.dumps(comparison, indent=2)}

Produce a final research conclusion.

Return ONLY valid JSON using this structure:

{{
    "conclusion": "A concise conclusion directly supported by the findings.",
    "confidence": "high | medium | low",
    "key_takeaways": [
        "Important takeaway supported by the research."
    ],
    "caveats": [
        "Important limitation, uncertainty, or contradiction."
    ]
}}

Rules:
1. Use ONLY the provided findings and comparison.
2. Do not introduce outside facts.
3. Do not hide contradictions.
4. If evidence is weak or incomplete, use lower confidence.
5. Keep the conclusion concise and evidence-based.
6. Return valid JSON only.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a precise enterprise research "
                    "synthesis analyst."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
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
            "conclusion": content,
            "confidence": "low",
            "key_takeaways": [],
            "caveats": [
                "The synthesis model did not return valid structured JSON."
            ],
        }