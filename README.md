# Hybrid RAG — Document Question Answering System

A production-style **Hybrid Retrieval-Augmented Generation (RAG)** application that combines **semantic vector search, keyword search, Reciprocal Rank Fusion (RRF), cross-encoder reranking, and local LLM generation with Ollama**.

The system provides a ChatGPT-style web interface where users can ask questions about uploaded documents and receive synthesized, streamed answers with document source references.

---

## Architecture

```text
                         ┌─────────────────────┐
                         │    React Frontend   │
                         │      Vite + JS      │
                         └──────────┬──────────┘
                                    │
                                    │ HTTP
                                    ▼
                         ┌─────────────────────┐
                         │     FastAPI API     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                              User Question
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
             FAISS Vector Search              BM25 Search
                    │                               │
                    └───────────────┬───────────────┘
                                    ▼
                                RRF Fusion
                                    │
                                    ▼
                            Candidate Documents
                                    │
                                    ▼
                           Cross-Encoder Reranker
                                    │
                                    ▼
                              Top-K Context
                                    │
                                    ▼
                                RAG Prompt
                                    │
                                    ▼
                             Ollama / llama3.2
                                    │
                                    ▼
                             Streaming Response
                                    │
                                    ▼
                            React Chat Interface
```

---

## Key Features

* PDF document ingestion
* Recursive document chunking
* Local embedding generation using Ollama
* Persistent FAISS vector index
* BM25 keyword retrieval
* Hybrid retrieval using Reciprocal Rank Fusion (RRF)
* Cross-encoder reranking
* Configurable final `top_k`
* Local LLM inference using Ollama
* Grounded document-based answering
* Markdown-formatted responses
* Streaming responses to the frontend
* FastAPI REST API
* React + Vite frontend
* ChatGPT-style conversation interface
* Document source display
* CORS configuration for frontend/backend communication

---

## Technology Stack

### Backend

| Technology            | Purpose                  |
| --------------------- | ------------------------ |
| Python                | Backend implementation   |
| FastAPI               | REST API                 |
| LangChain             | RAG components           |
| FAISS                 | Vector similarity search |
| BM25                  | Keyword retrieval        |
| RRF                   | Hybrid result fusion     |
| Sentence Transformers | Cross-encoder reranking  |
| Ollama                | Local embeddings and LLM |
| Pydantic              | API validation           |

### Frontend

| Technology     | Purpose                         |
| -------------- | ------------------------------- |
| React          | User interface                  |
| Vite           | Frontend development/build tool |
| JavaScript     | Frontend logic                  |
| React Markdown | Markdown response rendering     |

### Models

**Embedding model**

```text
nomic-embed-text
```

**LLM**

```text
llama3.2
```

**Reranker**

```text
cross-encoder/ms-marco-MiniLM-L-6-v2
```
