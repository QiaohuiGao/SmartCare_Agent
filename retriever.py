"""
Retriever
----------
Combines semantic (vector), keyword, and metadata filtering.
"""
import json, os

KB_PATH = os.path.join("data", "kb_docs.json")
KB_DOCS = json.load(open(KB_PATH)) if os.path.exists(KB_PATH) else []

def retrieve_kb(query: str, filters: dict, top_k: int = 5) -> list:
    query_lower = query.lower()
    hits = []
    for d in KB_DOCS:
        if filters.get("product") and d.get("product") != filters["product"]:
            continue
        if filters.get("fault_code") and d.get("fault_code") != filters["fault_code"]:
            continue
        score = _match_score(d["text"].lower(), query_lower)
        if score > 0:
            hits.append((score, d))
    hits.sort(key=lambda x: x[0], reverse=True)
    return [d for _, d in hits[:top_k]]

def _match_score(text, query):
    """Crude keyword overlap for demo (replace with FAISS/BM25)."""
    return sum(word in text for word in query.split())