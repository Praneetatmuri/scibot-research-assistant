import streamlit as st
from markitdown import MarkItDown
from genai_services import summarize_text, chunk_text
from chroma_services import ingest_documents
import tempfile
import os

st.markdown("""
    <style>
        body {
            background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%);
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        .scibot-card {
            background: #fff;
            border-radius: 18px;
            box-shadow: 0 4px 24px rgba(0,0,0,0.08);
            padding: 2.5rem 2rem 2rem 2rem;
            margin: 2rem auto 2rem auto;
            max-width: 700px;
        }
        .scibot-footer {
            color: #6c757d;
            font-size: 0.95em;
            margin-top: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='scibot-card'>", unsafe_allow_html=True)
st.markdown("# 🧪 SciBot: Research Document Ingestion\n#### Upload, summarize, and prepare your scientific papers for Q&A")
st.write("Upload scientific papers or research documents (txt, pdf, docx, etc.) to summarize and prepare for Q&A.")
uploaded_file = st.file_uploader(
    "Upload a research document (txt, pdf, or any text-based file supported by markitdown)",
    type=[
        "txt", "pdf", "md", "html", "docx"
    ]
)
if uploaded_file:
    # Save to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    # Convert to text using markitdown
    converter = MarkItDown()
    doc_text = converter.convert(tmp_path).text_content
    st.subheader("Document Preview:")
    st.text_area("Extracted Research Text", doc_text, height=200)

    # Summarize
    with st.spinner("Summarizing research document..."):
        summary = summarize_text(doc_text)
    st.subheader("Summary:")
    st.write(summary)
    # Upload button        if st.button("Upload & Ingest to Chroma DB"):
    # Chunk and ingest
    with st.spinner("Ingesting research document into SciBot knowledge base..."):
        chunks = chunk_text(doc_text)
        ingest_documents(chunks)
    if st.button("Go to SciBot Chat"):
        st.switch_page("pages/chatbot_page.py")
st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<div class='scibot-footer' style='text-align:center;'>© 2024 SciBot | Powered by AI</div>", unsafe_allow_html=True)
