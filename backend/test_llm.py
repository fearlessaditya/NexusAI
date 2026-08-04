from app.services.llm_service import ask_llm

context = """
Concurrent Engineering is a product development approach
where multiple teams work together simultaneously.
"""

question = "What is Concurrent Engineering?"

answer = ask_llm(question, context)

print(answer)