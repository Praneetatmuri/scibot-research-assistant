import os
from genai_services import summarize_text, chunk_text, answer_with_context
from chroma_services import ingest_documents, query_documents

# 1. Simulate document ingestion
sample_text = """
The mitochondria is the powerhouse of the cell. It generates ATP through cellular respiration. ATP is the energy currency of the cell, used in many biological processes.
"""

print("--- Simulating Document Ingestion ---")
summary = summarize_text(sample_text)
print("Summary:", summary)
chunks = chunk_text(sample_text)
print(f"Number of Chunks: {len(chunks)}")
for i, chunk in enumerate(chunks):
    print(f"Chunk {i+1}: {chunk}")
num_ingested = ingest_documents(chunks)
print(f"Ingested {num_ingested} chunks into ChromaDB.")

# 2. Simulate chatbot Q&A
print("\n--- Simulating Chatbot Q&A ---")
question = "What is the powerhouse of the cell?"
context_chunks = query_documents(question, n_results=3)
print(f"Retrieved {len(context_chunks)} context chunks:")
for i, ctx in enumerate(context_chunks):
    print(f"Context {i+1}: {ctx}")
if context_chunks:
    answer = answer_with_context(question, context_chunks)
    print("\nChatbot Answer:", answer)
else:
    print("No relevant context found for the question.") 