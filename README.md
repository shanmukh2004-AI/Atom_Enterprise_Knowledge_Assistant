# 🤖 Atom AI — Enterprise Knowledge Assistant

Atom AI is an AI-powered enterprise knowledge assistant built using FastAPI, Streamlit, RAG, FAISS, BM25, Sentence Transformers, and Gemini LLM.

The project allows users to upload documents and ask questions based on the uploaded knowledge base using Retrieval-Augmented Generation (RAG).

---

# 🚀 Features

* Multi-chat support
* Upload and use custom knowledge base files
* Retrieval-Augmented Generation (RAG)
* Semantic search using embeddings
* BM25 keyword retrieval
* FAISS vector database integration
* Gemini LLM integration
* Context-aware AI responses
* Rewrite/Edit previous user queries
* Streaming response effect
* Beginner-friendly UI
* FastAPI backend
* Streamlit frontend

---

# 🧠 Tech Stack

## Frontend

* Streamlit

## Backend

* FastAPI
* Uvicorn

## AI / RAG

* Gemini API
* Sentence Transformers
* FAISS
* BM25
* RAG (Retrieval-Augmented Generation)

## Other Libraries

* NumPy
* Requests
* Python Dotenv

---

# 📁 Project Structure

```text
Atom_Enterprise_Knowledge_Assistant/
│
├── backend/
│   ├── f_api.py
│   ├── llm.py
│   ├── rag.py
│   ├── .env
│
├── frontend/
│   ├── app.py
│
├── requirements.txt
├── .gitignore
├── README.md
```

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/shanmukh2004-AI/Atom_Enterprise_Knowledge_Assistant.git
```

---

## 2. Move Into the Project Folder

```bash
cd Atom_Enterprise_Knowledge_Assistant
```

---

## 3. Create Virtual Environment

```bash
python -m venv atom
```

---

## 4. Activate Virtual Environment

### Windows

```bash
atom\Scripts\activate
```

### Linux / Mac

```bash
source atom/bin/activate
```

---

## 5. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file inside the `backend` folder.

```env
GEMINI_API_KEY=your_api_key_here
```

---

# ▶️ Run Backend Server

Move into backend folder:

```bash
cd backend
```

Run FastAPI server:

```bash
uvicorn f_api:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

---

# ▶️ Run Frontend

Move into frontend folder:

```bash
cd frontend
```

Run Streamlit app:

```bash
streamlit run app.py
```

Frontend URL:

```text
http://localhost:8501
```

---

# 🧠 What is RAG?

RAG (Retrieval-Augmented Generation) is a method where the system first retrieves relevant information from uploaded documents and then sends that context to the LLM to generate better and more accurate responses.

---

# ⚡ How RAG Works in This Project

1. User uploads documents
2. Documents are converted into embeddings
3. Embeddings are stored in FAISS
4. BM25 performs keyword-based retrieval
5. Relevant chunks are retrieved
6. Retrieved context is sent to Gemini LLM
7. Gemini generates the final response
8. Streamlit displays the response to the user

---

# 📌 System Architecture

```text
                User
                  ↓
          Streamlit Frontend
                  ↓
            FastAPI Backend
                  ↓
          RAG Retrieval Layer
            ↓            ↓
         BM25         FAISS
            ↓            ↓
         Retrieved Context
                  ↓
             Gemini LLM
                  ↓
            Final Response
```

---

# 📚 Supported File Types

* TXT
* MD
* JSON
* HTML
* CSV

---

# 🎯 Future Improvements

* PDF support
* Authentication system
* Database integration
* Multi-user support
* Cloud vector database
* Voice input support
* Docker deployment

---

# 👨‍💻 Author

Shanmukh

GitHub:
https://github.com/shanmukh2004-AI

---

# 💡 Concepts Used

* RAG (Retrieval-Augmented Generation)
* Vector Databases
* Embeddings
* Semantic Search
* BM25 Retrieval
* FastAPI APIs
* Streamlit Applications
* LLM Integration
* Context Retrieval Pipelines

---

# ⭐ Project Purpose

This project was built for:

* AI portfolio projects
* Interview demonstrations
* Learning RAG systems
* Understanding vector databases
* Building enterprise AI assistant workflows

---

# 📄 License

This project is created for educational and learning purposes.
