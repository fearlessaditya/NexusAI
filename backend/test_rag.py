from app.services.rag_service import ask_question

question = "What is Concurrent Engineering?"

answer = ask_question(question)

print("\nQuestion:")
print(question)

print("\nAnswer:")
print(answer)