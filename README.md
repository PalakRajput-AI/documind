# DocuMind — AI-Powered Document Q&A Chatbot
> Upload any document (PDF, DOCX, TXT) and chat with it using AI-powered semantic search — get instant, cited answers in plain English.

🔗 **Live Demo:** [https://chatbot-docai.streamlit.app](https://chatbot-docai.streamlit.app)

## Problem Statement
Professionals and students waste hours manually scanning through lengthy PDFs, reports, and research papers to find specific information. **DocuMind** solves this by letting users upload any document and ask questions in natural language — receiving accurate, source-cited answers in seconds.

## Features
- 📄 Multi-format support — Upload PDF, DOCX, or TXT files
- 🔍 Semantic search — Finds relevant content using vector embeddings, not just keyword matching
- 💬 Natural language Q&A — Ask questions the way you'd ask a person
- 🤖 Dual answer modes — Generative (AI-written, natural answers via Groq) and Extractive (100% local, no-API fallback)
- 📚 Source citations — Every answer shows exactly which part of the document it came from
- 📊 Live statistics — Track questions asked and document status
- ⚡ Fast retrieval — FAISS-powered vector search returns results in milliseconds
- 🆓 Free-tier architecture — Uses Groq's free API for generative answers, with a fully local extractive fallback if the API is ever unavailable

## Architecture
Document Upload → Text Chunking → Embedding Generation → FAISS Vector Store → User Question → Query Embedding → Similarity Search → Generative or Extractive Answer

The system uses a Retrieval-Augmented Generation (RAG) style pipeline:
1. Documents are split into overlapping chunks for context preservation
2. Each chunk is converted into a 384-dimensional vector using Sentence Transformers
3. FAISS indexes these vectors for fast nearest-neighbor search
4. User queries are embedded the same way and matched against stored chunks
5. The most relevant chunks are passed to Groq's free LLM API (Llama 3.3 70B) to generate a natural, grounded answer
6. If the API is unavailable, the system automatically falls back to a local extractive method — ranking and returning the most relevant sentences directly from the document, with no external dependency

## Tech Stack
| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Embeddings | Sentence-Transformers (all-MiniLM-L6-v2) |
| Vector Search | FAISS (Facebook AI Similarity Search) |
| Generative LLM | Groq API (Llama 3.3 70B) — free tier |
| Document Parsing | PyPDF2, python-docx |
| Text Processing | LangChain Text Splitters |
| Language | Python 3.13 |
| Deployment | Streamlit Community Cloud |

## Project Structure
documind/
├── app/
│   └── main.py              # Streamlit UI
├── core/
│   ├── document_loader.py   # PDF/DOCX/TXT parsing
│   ├── chunker.py           # Text splitting logic
│   ├── embedder.py          # Sentence embedding generation
│   ├── vector_store.py      # FAISS index management
│   └── rag_pipeline.py      # End-to-end RAG orchestration (generative + extractive)
├── data/                    # Uploaded files & vector store (gitignored)
├── tests/                   # Unit tests
├── requirements.txt
└── README.md

## Run Locally
git clone https://github.com/PalakRajput-AI/documind.git
cd documind
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

Create a .env file in the root folder with your free Groq API key:
GROQ_API_KEY=your_key_here

Then run:
streamlit run app/main.py

## What I Learned
- Designing an end-to-end RAG pipeline from scratch — document ingestion, chunking strategy, embedding generation, and retrieval
- Working with vector databases (FAISS) and understanding similarity search at scale
- Building a fallback-resilient system — generative answers via a free LLM API, with a 100% local extractive method as a safety net if the API fails
- Deploying a full-stack ML application end-to-end, from local development to live cloud hosting, including managing API secrets securely
- UI/UX design for AI products using Streamlit, including mode toggles for flexible answer generation

## Future Improvements
- Hybrid search combining BM25 keyword matching with vector similarity for better recall
- Support for tables, images, and multi-document cross-referencing
- User authentication with per-user document libraries
- Caching frequent queries to reduce API calls further
