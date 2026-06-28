# DOCUMIND - MAIN STREAMLIT APP
# This file creates the complete chat interface

import streamlit as st
import sys
import os

# Add core modules path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))

from rag_pipeline import initialize_pipeline, process_document, ask_question


# PAGE SETUP

st.set_page_config(
    page_title="DocuMind - AI Document Assistant",
    page_icon="🧠",
    layout="wide"
)


# CUSTOM STYLING

st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }

    .chat-message-user {
        background-color: #dbeafe;
        color: #111827;
        padding: 12px;
        border-radius: 12px;
        margin: 8px 0;
        border-left: 4px solid #2563eb;
    }

    .chat-message-ai {
        background-color: #f3e8ff;
        color: #111827;
        padding: 12px;
        border-radius: 12px;
        margin: 8px 0;
        border-left: 4px solid #9333ea;
    }

    .source-box {
        background-color: #dcfce7;
        color: #111827;
        padding: 10px;
        border-radius: 8px;
        margin: 5px 0;
        border-left: 4px solid #22c55e;
        font-size: 0.9rem;
    }

    .stats-box {
        background-color: #fef3c7;
        color: #111827;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# HEADER

st.markdown("""
<div class="main-header">
    <h1>🧠 DocuMind</h1>
    <p>AI-Powered Document Q&A Assistant</p>
    <p><small>Upload any document and chat with it!</small></p>
</div>
""", unsafe_allow_html=True)


# SESSION STATE SETUP
# Stores chat history and app state

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'model' not in st.session_state:
    st.session_state.model = None

if 'document_processed' not in st.session_state:
    st.session_state.document_processed = False

if 'document_name' not in st.session_state:
    st.session_state.document_name = None

if 'answer_mode' not in st.session_state:
    st.session_state.answer_mode = "auto"


# INITIALIZE MODEL

if st.session_state.model is None:
    with st.spinner("🔄 Loading AI model... Please wait!"):
        st.session_state.model = initialize_pipeline()


# SIDEBAR - FILE UPLOAD

with st.sidebar:
    st.markdown("## 📁 Document Upload")
    st.markdown("---")

    # File uploader
    uploaded_file = st.file_uploader(
        "Choose your document",
        type=['pdf', 'docx', 'txt'],
        help="Upload a PDF, DOCX, or TXT file"
    )

    if uploaded_file is not None:
        # Display file info
        st.success(f"✅ File selected: {uploaded_file.name}")

        # Display file size
        file_size = len(uploaded_file.getvalue()) / 1024
        st.info(f"📊 Size: {file_size:.1f} KB")

        # Process button
        if st.button("🚀 Process Document", type="primary"):
            # Save file temporarily
            temp_path = f"data/{uploaded_file.name}"
            os.makedirs("data", exist_ok=True)

            with open(temp_path, 'wb') as f:
                f.write(uploaded_file.getvalue())

            # Process document
            with st.spinner("⚙️ Processing document..."):
                success = process_document(
                    temp_path,
                    st.session_state.model
                )

            if success:
                st.session_state.document_processed = True
                st.session_state.document_name = uploaded_file.name
                st.session_state.chat_history = []

                st.success("✅ Document is ready! Start asking questions!")
                st.balloons()
            else:
                st.error("❌ Failed to process document. Please try again.")

    st.markdown("---")

    # Document status
    st.markdown("## 📊 Status")

    if st.session_state.document_processed:
        st.success(f"✅ Active: {st.session_state.document_name}")
    else:
        st.warning("⚠️ No document uploaded")

    st.markdown("---")

    # Answer mode toggle
    st.markdown("## ⚙️ Answer Mode")
    answer_mode = st.radio(
        "Choose how answers are generated:",
        options=["Auto (Smart)", "Generative (AI)", "Extractive (Local)"],
        index=0,
        help="Auto tries AI-generated answers first, then falls back to local search if unavailable."
    )

    mode_map = {
        "Auto (Smart)": "auto",
        "Generative (AI)": "generative",
        "Extractive (Local)": "extractive"
    }
    st.session_state.answer_mode = mode_map[answer_mode]

    st.markdown("---")

    # Clear chat button
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

    st.markdown("---")

    # Instructions
    st.markdown("""
    ## 💡 How to Use
    1. 📄 Upload a document
    2. 🚀 Click Process Document
    3. ❓ Type your question
    4. 🤖 Get AI-powered answers

    ## 📁 Supported Files
    - PDF files
    - Word documents (DOCX)
    - Text files (TXT)
    """)


# MAIN CHAT AREA

col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("## 💬 Chat")

    # Display chat history
    if not st.session_state.chat_history:
        if st.session_state.document_processed:
            st.info("👋 Your document is ready! Ask any question.")
        else:
            st.info("👆 Upload a document from the sidebar first!")
    else:
        for chat in st.session_state.chat_history:

            # User message
            st.markdown(f"""
            <div class="chat-message-user">
                <strong>👤 You:</strong> {chat['question']}
            </div>
            """, unsafe_allow_html=True)

            # AI message
            st.markdown("""
            <div class="chat-message-ai">
                <strong>🤖 DocuMind:</strong>
            </div>
            """, unsafe_allow_html=True)

            st.write(chat['answer'])

            # Display sources
            if chat.get('sources'):
                with st.expander(
                    f"📚 View Sources ({len(chat['sources'])} found)"
                ):
                    for i, source in enumerate(chat['sources']):
                        st.markdown(f"""
                        <div class="source-box">
                            <strong>Source {i+1}:</strong>
                            {source['chunk'][:200]}...
                        </div>
                        """, unsafe_allow_html=True)

            st.markdown("---")

with col2:
    st.markdown("## 📈 Statistics")

    # Display stats
    st.markdown(f"""
    <div class="stats-box">
        <h3>{len(st.session_state.chat_history)}</h3>
        <p>Questions Asked</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.session_state.document_processed:
        st.markdown("""
        <div class="stats-box">
            <h3>✅</h3>
            <p>Document Ready</p>
        </div>
        """, unsafe_allow_html=True)


# QUESTION INPUT

st.markdown("---")

if st.session_state.document_processed:

    question = st.chat_input(
        "Type your question here..."
    )

    if question:
        # Generate answer
        with st.spinner("🤔 Thinking..."):
            result = ask_question(
                question,
                st.session_state.model,
                mode=st.session_state.get('answer_mode', 'auto')
            )

        if result:
            st.session_state.chat_history.append({
                'question': question,
                'answer': result['answer'],
                'sources': result['sources']
            })

            st.rerun()
        else:
            st.error("No answer found. Please try again!")

else:
    st.chat_input(
        "Upload a document first...",
        disabled=True
    )


# FOOTER

st.markdown("---")

st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.8rem;'>
    🧠 DocuMind | Built with Python, LangChain, FAISS & Streamlit<br>
    Made with ❤️ for an internship portfolio
</div>
""", unsafe_allow_html=True)