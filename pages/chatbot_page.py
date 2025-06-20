import streamlit as st
from genai_services import answer_with_context
from chroma_services import query_documents

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
st.markdown("# 🧪 SciBot: Scientific Research Chatbot\n#### Your AI-powered research assistant")
st.write("Ask scientific questions about your ingested research documents!")
user_query = st.chat_input("Enter your scientific question:")
if user_query:
    # Query Chroma for context
    context_chunks = query_documents(user_query, n_results=3)

    if not context_chunks:
        st.warning("No relevant context found for your question. Please make sure you have ingested a document and your question matches its content.")
    else:
        with st.spinner("Analyzing research and generating answer..."):
            answer = answer_with_context(user_query, context_chunks)
        st.markdown(f"**SciBot's Answer:** {answer}")
        st.expander("Show supporting research context").write("\n---\n".join(context_chunks))
st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<div class='scibot-footer' style='text-align:center;'>© 2024 SciBot | Powered by AI</div>", unsafe_allow_html=True)
