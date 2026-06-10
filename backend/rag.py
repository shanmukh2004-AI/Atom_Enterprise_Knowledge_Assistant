from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
from rank_bm25 import BM25Okapi
from llm import generate_answer
model = SentenceTransformer("all-MiniLM-L6-v2")
chunks = []
index = None
embeddings_np = None
documents = {}
bm25 = None

def rebuild_index():

    global chunks
    global index
    global embeddings_np
    global bm25
    # =========================
    # COMBINE ALL FILES
    # =========================
    all_text = ""
    for text in documents.values():
        all_text += text + "\n"
    # =========================
    # RESET
    # =========================
    chunks = []

    # NO FILES
    if not all_text.strip():

        index = None
        embeddings_np = None
        bm25 = None

        return

    # =========================
    # CHUNKING
    # =========================
    chunk_size = 300
    overlap = 50
    
    for i in range(0,len(all_text),chunk_size - overlap):
        # chunks.append(all_text[i:i + chunk_size])
        chunk = all_text[i:i + chunk_size].strip()

        if chunk:
            chunks.append(chunk)
        
    # =========================
    # BM25
    # =========================
    tokenized_chunks = [chunk.lower().split()for chunk in chunks]
    bm25 = BM25Okapi(tokenized_chunks)
    # =========================
    # EMBEDDINGS
    # =========================
    embeddings = model.encode(chunks)
    embeddings_np = np.array(embeddings).astype("float32")
    # =========================
    # FAISS
    # =========================
    dimension = embeddings_np.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings_np)

def build_index_from_text(file_name, file_text):
    if not file_text.strip():
        return
    documents[file_name] = file_text
    rebuild_index()
    
    
def delete_document(file_name):
    if file_name in documents:
        del documents[file_name]
    rebuild_index()

def faiss_search(query):
    global bm25
    if index is None:
        return []
    # =========================
    # DYNAMIC TOP K
    # =========================
    query_words = len(query.split())
    if query_words <= 3:
        k = 2
    elif query_words <= 10:
        k = 4
    else:
        k = 6
    k = min(k, len(chunks))
    # =========================
    # SEMANTIC SEARCH
    # =========================
    query_vector = model.encode([query]).astype("float32")
    # distances, indices = index.search(query_vector, k)
    _, indices = index.search(query_vector, k)
    semantic_results = []
    for i in indices[0]:
        if i < len(chunks):
            semantic_results.append(chunks[i])
    # =========================
    # BM25 KEYWORD SEARCH
    # =========================
    if bm25 is None:
        return semantic_results
    tokenized_query = query.lower().split()
    bm25_scores = bm25.get_scores(tokenized_query)
    top_keyword_indices = np.argsort(bm25_scores)[::-1][:k]
    keyword_results = []
    for i in top_keyword_indices:
        if i < len(chunks):
            keyword_results.append(chunks[i])
    # =========================
    # HYBRID MERGE
    # =========================
    combined_results = semantic_results + keyword_results
    # REMOVE DUPLICATES
    unique_results = list(dict.fromkeys(combined_results))
    return unique_results[:k]

# def chat(query, history=[]):
def chat(query, history=None):
    if not query.strip():
        return "Please enter a valid question."
    if history is None:
        history = []
    # =========================
    # CONVERSATION MEMORY
    # =========================
    history_text = ""
    # for msg in history:
    for msg in history[-6:]:
        role = msg["role"]
        content = msg["content"]
        history_text += f"{role}: {content}\n"

    # =========================
    # NO FILE UPLOADED
    # =========================
    if index is None:
        final_prompt = f"""
Conversation History:
{history_text}

Current User Question:
{query}
"""
        answer = generate_answer(final_prompt, "")
        return answer
    # =========================
    # RAG SEARCH
    # =========================
    retrieved_chunks = faiss_search(query)
    # TOKEN LIMIT SAFETY
    context = "\n".join(retrieved_chunks)
    # =========================
    # FINAL PROMPT
    # =========================
    final_prompt = f"""
Conversation History:
{history_text}

Context:
{context}

Current User Question:
{query}
"""
    answer = generate_answer(final_prompt, "")
    return answer