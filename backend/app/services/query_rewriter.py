from groq import Groq

from app.core.config import settings
from app.services.memory_service import get_memory


client = Groq(
    api_key=settings.GROQ_API_KEY
)


def rewrite_query(question: str) -> str:

    memory = get_memory()

    messages = [
        {
            "role": "system",
            "content": """
You rewrite follow-up questions into standalone search queries.

Rules:
- Use previous conversation if needed.
- Keep the meaning unchanged.
- Return ONLY the rewritten question.
- Do not answer the question.
"""
        }
    ]

    # Previous conversation
    messages.extend(memory)

    # Current question
    messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0,
    )

    return response.choices[0].message.content.strip()