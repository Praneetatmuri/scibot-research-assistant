import chromadb
import os

from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(
    name=os.getenv("CHROMA_COLLECTION_NAME")
)

# --- Begin: Persistent unique chunk ID logic (reversible) ---
import shelve

def get_next_chunk_id():
    with shelve.open("chroma_chunk_counter.db") as db:
        last_id = db.get("last_id", 0)
        db["last_id"] = last_id + 1
        return last_id

def ingest_documents(docs):
    """Ingest documents into ChromaDB using 'all-MiniLM-L6-v2' Sentence Transformer

    Args:
        docs: list of strings (document chunks)
    """
    # Use persistent counter for unique IDs
    ids = [f"chunk_{get_next_chunk_id()}" for _ in range(len(docs))]
    collection.add(documents=docs, ids=ids)
    return len(docs)
# --- End: Persistent unique chunk ID logic (reversible) ---

def query_documents(query_text, n_results=3):
    """Query the collection for relevant documents

    Args:
        query_text: string to search for
        n_results: number of results to return

    Returns:
        List of relevant document chunks
    """
    results = collection.query(query_texts=[query_text], n_results=n_results)
    if 'documents' in results and results['documents']:
        return results['documents'][0]
    else:
        return []
