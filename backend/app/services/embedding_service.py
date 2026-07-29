from sentence_transformers import SentenceTransformer

# Load embedding model only once
model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embeddings(chunks: list[str]):

    embeddings = model.encode(chunks)

    return embeddings