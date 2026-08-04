import chromadb

# Create Chroma client
client = chromadb.PersistentClient(path="chroma_db")

# Create/Get collection
collection = client.get_or_create_collection(
    name="documents"
)


def store_embeddings(
    chunks,
    embeddings,
    filename: str,
    uploaded_by: str,
):

    ids = [f"chunk_{i}" for i in range(len(chunks))]

    metadatas = [
        {
            "filename": filename,
            "uploaded_by": uploaded_by,
        }
        for _ in chunks
    ]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings.tolist(),
        metadatas=metadatas,
    )


def search_similar(query_embedding, top_k=3):

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k,
        include=[
            "documents",
            "metadatas",
            "distances",
        ],
    )

    return results