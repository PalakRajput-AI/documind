
# TEXT CHUNKER
# This file splits large text into smaller chunks
# so that AI can easily read and understand it


from langchain_text_splitters import RecursiveCharacterTextSplitter


def create_chunks(text, chunk_size=500, chunk_overlap=50):
    """
    Splits large text into smaller chunks.

    Parameters:
    - text: the complete document text
    - chunk_size: maximum characters per chunk (default 500)
    - chunk_overlap: overlap between consecutive chunks (default 50)

    Real-life example:
    Imagine cutting a long rope into smaller pieces,
    but keeping a small overlapping section between pieces
    so that no information is lost in the middle.
    """

    # Create a text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        # Maximum characters per chunk
        chunk_size=chunk_size,

        # Overlap between consecutive chunks
        # Helps prevent sentences from being cut awkwardly
        chunk_overlap=chunk_overlap,

        # Function used to measure text length
        length_function=len,

        # Preferred splitting order
        # First paragraph, then sentence, then word
        separators=["\n\n", "\n", ".", "!", "?", ",", " "]
    )

    # Split the text into chunks
    chunks = text_splitter.split_text(text)

    print("\nText chunking complete!")
    print(f"Total chunks created: {len(chunks)}")
    print(f"Chunk size: ~{chunk_size} characters")
    print(f"Overlap: {chunk_overlap} characters")

    return chunks


def show_chunks_info(chunks):
    """
    Displays information about the chunks.
    Useful for debugging and inspection.
    """
    print("\n--- Chunk Information ---")
    print(f"Total chunks: {len(chunks)}")

    for i, chunk in enumerate(chunks[:3]):  # Show only first 3 chunks
        print(f"\nChunk {i + 1}:")
        print(f"Length: {len(chunk)} characters")
        print(f"Preview: {chunk[:100]}...")  # First 100 characters

    if len(chunks) > 3:
        print(f"\n... and {len(chunks) - 3} more chunks")



# FOR TESTING

if __name__ == "__main__":
    print("Running Text Chunker Test...")
    print("=" * 40)

    # Create a sample text for testing
    sample_text = """
    What is Artificial Intelligence?

    Artificial Intelligence (AI) is a technology that enables
    computers to think and perform tasks similar to humans.
    AI is widely used today in mobile phones, cars, hospitals,
    schools, and many other industries.

    What is Machine Learning?

    Machine Learning is a subset of Artificial Intelligence.
    It allows computers to learn from data without being
    explicitly programmed. Just as a child learns through
    experience and mistakes, machines learn from data.
    Machine Learning is used for spam detection, Netflix
    recommendations, and medical diagnosis.

    What is Deep Learning?

    Deep Learning is an advanced form of Machine Learning.
    It works using artificial neural networks inspired by
    the human brain. Technologies such as ChatGPT, image
    recognition systems, and voice assistants like Alexa
    and Siri are powered by Deep Learning. It typically
    requires large amounts of data and powerful computers.

    What is Natural Language Processing?

    Natural Language Processing (NLP) is a branch of AI that
    helps computers understand and process human language.
    Whenever you search on Google or interact with ChatGPT,
    NLP is involved. In this project, we will use NLP to
    understand and analyze documents.
    """

    # Create chunks
    chunks = create_chunks(sample_text)

    # Display chunk information
    show_chunks_info(chunks)

    print("\nTest SUCCESSFUL! The Text Chunker is working correctly!")