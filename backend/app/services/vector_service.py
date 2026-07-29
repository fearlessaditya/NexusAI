import chromadb

# Create Chroma client
client = chromadb.PersistentClient(path="chroma_db")

# Create/Get collection
collection = client.get_or_create_collection(
    name="documents"
)


def store_embeddings(chunks, embeddings):

    ids = [f"chunk_{i}" for i in range(len(chunks))]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings.tolist()
    )


def search_similar(query_embedding, top_k=3):

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k
    )

    return results