
# VECTOR STORE
# This file stores embeddings
# and searches for similar text chunks
# FAISS - Facebook AI Similarity Search


import faiss
import numpy as np
import pickle
import os


def create_vector_store(embeddings, chunks):
    """
    Creates a FAISS vector store.

    Parameters:
    - embeddings: NumPy array of embeddings
    - chunks: original text chunks

    Real-life example:
    Just like books are organized on library shelves
    so they can be found quickly later, embeddings
    are organized in a vector store for fast retrieval.
    """
    print("\nCreating vector store...")

    # Embedding dimension (384 for our model)
    dimension = embeddings.shape[1]

    # Create FAISS index
    # IndexFlatL2 = exact search using L2 distance
    index = faiss.IndexFlatL2(dimension)

    # Add embeddings to the index
    # FAISS requires float32 format
    embeddings_float32 = np.array(embeddings).astype('float32')
    index.add(embeddings_float32)

    print("Vector store created successfully!")
    print(f"Total vectors stored: {index.ntotal}")
    print(f"Vector dimension: {dimension}")

    return index


def save_vector_store(index, chunks, save_path="data/vector_store"):
    """
    Saves the vector store to disk.

    Real-life example:
    Just like a library maintains a catalog
    of all books for future reference,
    we save the vector store for later use.
    """
    # Create folder if it doesn't exist
    os.makedirs(save_path, exist_ok=True)

    # Save FAISS index
    faiss.write_index(index, f"{save_path}/index.faiss")

    # Save chunks using pickle
    with open(f"{save_path}/chunks.pkl", 'wb') as f:
        pickle.dump(chunks, f)

    print(f"\nVector store saved successfully: {save_path}/")
    print("Files saved:")
    print("  - index.faiss (search index)")
    print("  - chunks.pkl (original text)")


def load_vector_store(save_path="data/vector_store"):
    """
    Loads a previously saved vector store.

    Real-life example:
    Just like opening a library catalog
    before starting work, we load the
    saved vector store before searching.
    """
    try:
        # Load FAISS index
        index = faiss.read_index(f"{save_path}/index.faiss")

        # Load chunks
        with open(f"{save_path}/chunks.pkl", 'rb') as f:
            chunks = pickle.load(f)

        print("Vector store loaded successfully!")
        print(f"Total vectors: {index.ntotal}")

        return index, chunks

    except Exception as e:
        print(f"Error loading vector store: {e}")
        return None, None


def search_similar_chunks(query_embedding, index, chunks, top_k=3):
    """
    Searches for chunks similar to the user's query.

    Parameters:
    - query_embedding: embedding of the user's question
    - index: FAISS index
    - chunks: original text chunks
    - top_k: number of results to return (default 3)

    Real-life example:
    Just like Google returns the most relevant
    search results, this function returns the
    most similar text chunks.
    """
    # Convert query embedding to correct format
    query_array = np.array([query_embedding]).astype('float32')

    # Perform search
    distances, indices = index.search(query_array, top_k)

    # Prepare results
    results = []
    for i, (dist, idx) in enumerate(zip(distances[0], indices[0])):
        if idx != -1:
            results.append({
                'chunk': chunks[idx],
                'distance': float(dist),
                'rank': i + 1
            })

    return results



# FOR TESTING

if __name__ == "__main__":
    print("Running Vector Store Test...")
    print("=" * 40)

    # Import embedding functions
    from embedder import (
        load_embedding_model,
        create_embeddings,
        get_query_embedding
    )

    # Sample text chunks
    sample_chunks = [
        "Artificial Intelligence gives computers the ability to think.",
        "Machine Learning is a technology that learns from data.",
        "Deep Learning uses neural networks similar to the human brain.",
        "NLP helps computers understand human language.",
        "FAISS is a fast similarity search library developed by Facebook.",
        "Streamlit is an easy way to build web applications in Python."
    ]

    # Load model
    print("\nLoading embedding model...")
    model = load_embedding_model()

    # Create embeddings
    embeddings = create_embeddings(sample_chunks, model)

    # Create vector store
    index = create_vector_store(embeddings, sample_chunks)

    # Save vector store
    save_vector_store(index, sample_chunks)

    # Load vector store again for testing
    print("\nReloading vector store...")
    loaded_index, loaded_chunks = load_vector_store()

    # Test search
    print("\n--- Search Test ---")
    test_query = "What are AI and Machine Learning?"
    print(f"Query: '{test_query}'")

    query_emb = get_query_embedding(test_query, model)
    results = search_similar_chunks(
        query_emb,
        loaded_index,
        loaded_chunks
    )

    print(f"\nFound Top {len(results)} Similar Chunks:")

    for result in results:
        print(f"\nRank {result['rank']}:")
        print(f"Text: {result['chunk']}")
        print(f"Distance: {result['distance']:.4f}")

    print("\nTest SUCCESSFUL! The Vector Store is working correctly!")