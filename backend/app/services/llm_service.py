from groq import Groq

from app.core.config import settings


client = Groq(
    api_key=settings.GROQ_API_KEY
)


def ask_llm(question: str, context: str) -> str:
    prompt = f"""
You are an AI assistant.

Answer ONLY using the provided context.

If the answer is not available in the context,
reply:
"I couldn't find this information in the uploaded documents."

Context:
{context}

Question:
{question}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,
    )

    return response.choices[0].message.content