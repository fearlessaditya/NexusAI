from app.services.search_service import search_documents

question = "What is Concurrent Engineering?"

results = search_documents(question)

print(results)