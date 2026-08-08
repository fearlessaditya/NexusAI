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
            "content":   """
You are a helpful AI assistant for a document-based question answering system.

Answer the user's question using ONLY the provided context.

You may summarize, combine, and infer information when the inference is directly
supported by the facts in the context.

If the context describes features, capabilities, functions, or improvements,
you may explain how those can be considered advantages when the user asks
about advantages or benefits.

Do not invent facts that are not supported by the context.

Only say:
"I couldn't find this information in the uploaded documents."

when the provided context contains no relevant information for the question.
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