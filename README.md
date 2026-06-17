#  DocuMind — AI-Powered Document Q&A Chatbot

> Upload any document (PDF, DOCX, TXT) and chat with it using AI-powered semantic search — get instant, cited answers in plain English.

🔗 **Live Demo:** [https://chatbot-docai.streamlit.app](https://chatbot-docai.streamlit.app)



##  Problem Statement

Professionals and students waste hours manually scanning through lengthy PDFs, reports, and research papers to find specific information. **DocuMind** solves this by letting users upload any document and ask questions in natural language — receiving accurate, source-cited answers in seconds.



##  Features

- 📄 Multi-format support — Upload PDF, DOCX, or TXT files
- 🔍 Semantic search — Finds relevant content using vector embeddings, not just keyword matching
- 💬 Natural language Q&A — Ask questions the way you'd ask a person
- 📚 Source citations — Every answer shows exactly which part of the document it came from
- 📊 Live statistics — Track questions asked and document status
- ⚡ Fast retrieval — FAISS-powered vector search returns results in milliseconds
- 🆓 Zero-cost architecture — No paid API dependency; runs entirely on open-source models



##  Architecture

Document Upload → Text Chunking → Embedding Generation → FAISS Vector Store → User Question → Query Embedding → Similarity Search → Extractive Answer Generation

The system uses a Retrieval-Augmented Generation (RAG) style pipeline:
1. Documents are split into overlapping chunks for context preservation
2. Each chunk is converted into a 384-dimensional vector using Sentence Transformers
3. FAISS indexes these vectors for fast nearest-neighbor search
4. User queries are embedded the same way and matched against stored chunks
5. The most semantically relevant sentences are extracted and presented as the answer, with full source traceability



##  Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Embeddings | Sentence-Transformers (all-MiniLM-L6-v2) |
| Vector Search | FAISS (Facebook AI Similarity Search) |
| Document Parsing | PyPDF2, python-docx |
| Text Processing | LangChain Text Splitters |
| Language | Python 3.13 |
| Deployment | Streamlit Community Cloud |



##  Project Structure

documind/
├── app/
│   └── main.py              # Streamlit UI
├── core/
│   ├── document_loader.py   # PDF/DOCX/TXT parsing
│   ├── chunker.py           # Text splitting logic
│   ├── embedder.py          # Sentence embedding generation
│   ├── vector_store.py      # FAISS index management
│   └── rag_pipeline.py      # End-to-end RAG orchestration
├── data/                    # Uploaded files & vector store (gitignored)
├── tests/                   # Unit tests
├── requirements.txt
└── README.md



##  Run Locally

git clone https://github.com/PalakRajput-AI/documind.git
cd documind
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app/main.py



##  What I Learned

- Designing an end-to-end RAG pipeline from scratch — document ingestion, chunking strategy, embedding generation, and retrieval
- Working with vector databases (FAISS) and understanding similarity search at scale
- Building a fallback-resilient system that doesn't depend on third-party LLM APIs for core functionality
- Deploying a full-stack ML application end-to-end, from local development to live cloud hosting
- UI/UX design for AI products using Streamlit



##  Future Improvements

- Hybrid search combining BM25 keyword matching with vector similarity for better recall
- Add a lightweight open-source LLM (e.g., via Ollama) for more natural, generative answers
- Support for tables, images, and multi-document cross-referencing
- User authentication with per-user document libraries



