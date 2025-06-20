import streamlit as st

st.set_page_config(page_title="SciBot: Scientific Research Assistant", layout="wide")

ingest_page = st.Page("pages/ingest_page.py", title="Ingest Research")
chatbot_page = st.Page("pages/chatbot_page.py", title="SciBot Chat")

pg = st.navigation([
    ingest_page,
    chatbot_page
])

pg.run()
