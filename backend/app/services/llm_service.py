from groq import Groq

from app.core.config import settings
from app.services.memory_service import (
    add_message,
    get_memory,
)

client = Groq(
    api_key=settings.GROQ_API_KEY
)


def ask_llm(question: str, context: str) -> str:

    # Get previous conversation
    memory = get_memory()

    messages = [
        {
            "role": "system",
            "content": """
You are an AI assistant.

Answer ONLY using the provided context.

If the answer is not available in the context,
reply:

'I couldn't find this information in the uploaded documents.'
"""
        }
    ]

    # Add previous conversation
    messages.extend(memory)

    # Add current question with RAG context
    messages.append(
        {
            "role": "user",
            "content": f"""
Context:
{context}

Question:
{question}
"""
        }
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0,
    )

    answer = response.choices[0].message.content

    # Save conversation
    add_message("user", question)
    add_message("assistant", answer)

    return answer