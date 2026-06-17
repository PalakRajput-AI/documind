
# EMBEDDER
# This file converts text into numerical vectors
# so that AI can understand similarity between texts


from sentence_transformers import SentenceTransformer
import numpy as np


# Load the model - it will be downloaded once (~90MB)
# all-MiniLM-L6-v2 is a fast and accurate embedding model
MODEL_NAME = "all-MiniLM-L6-v2"


def load_embedding_model():
    """
    Loads the embedding model.

    Real-life example:
    Just like buying a dictionary once and using it repeatedly,
    the model is loaded once and then reused whenever needed.
    """
    print(f"Loading embedding model: {MODEL_NAME}")
    print("The first run may take some time as the model will be downloaded...")

    model = SentenceTransformer(MODEL_NAME)

    print("Model loaded successfully!")
    return model


def create_embeddings(chunks, model):
    """
    Converts text chunks into embeddings (numerical vectors).

    Parameters:
    - chunks: list of text chunks
    - model: embedding model

    Real-life example:
    Just like every location has GPS coordinates
    (latitude and longitude), every text chunk gets
    its own numerical vector representation.
    """
    print(f"\nCreating embeddings for {len(chunks)} chunks...")

    # Generate embeddings
    embeddings = model.encode(
        chunks,
        show_progress_bar=True,   # Display progress bar
        convert_to_numpy=True     # Convert output to NumPy array
    )

    print("\nEmbeddings created successfully!")
    print(f"Embedding size: {embeddings.shape[1]} numbers")
    print(f"Total embeddings: {embeddings.shape[0]}")

    return embeddings


def get_query_embedding(query, model):
    """
    Converts a user's query into an embedding vector.

    Real-life example:
    When you type a search query into Google,
    it is also converted into numerical form
    to find the most relevant results.
    """
    query_embedding = model.encode([query], convert_to_numpy=True)
    return query_embedding[0]



# FOR TESTING

if __name__ == "__main__":
    print("Running Embedder Test...")
    print("=" * 40)

    # Load the model
    model = load_embedding_model()

    # Sample text chunks
    sample_chunks = [
        "Artificial Intelligence gives computers the ability to think.",
        "Machine Learning is a technology that learns from data.",
        "Deep Learning works similarly to the human brain.",
        "NLP helps computers understand human language."
    ]

    # Create embeddings
    embeddings = create_embeddings(sample_chunks, model)

    # Test query embedding
    print("\n--- Query Embedding Test ---")
    test_query = "What is AI?"
    query_emb = get_query_embedding(test_query, model)

    print(f"Query: '{test_query}'")
    print(f"Query embedding size: {len(query_emb)} numbers")
    print(f"First 5 values: {query_emb[:5].round(3)}")

    print("\nTest SUCCESSFUL! The Embedder is working correctly!")