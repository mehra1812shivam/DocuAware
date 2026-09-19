# 📄 DocuAware

### AI-Powered Document Intelligence with Permission-Aware RAG

DocuAware is a production-oriented **Retrieval-Augmented Generation (RAG)** application that allows users to securely upload documents, generate AI-powered summaries, and ask natural-language questions against documents they are authorized to access.

The project combines **FastAPI, Streamlit, PostgreSQL, Qdrant, Gemini, LangChain, embeddings, and BGE reranking** into a modular architecture designed around authentication, authorization, document management, and permission-aware retrieval.

> **Built as a practical end-to-end GenAI application rather than a simple PDF-to-LLM demo.**

---

## ✨ Features

### 🔐 Authentication & Authorization

* JWT-based authentication
* Secure user registration and login
* Authenticated user profile endpoint
* Role-based access control
* `USER` and `ADMIN` roles
* Department-based access control
* Backend-enforced authorization
* Permission-aware document retrieval

### 📄 Document Management

Supports:

* PDF
* DOCX
* TXT

Each document stores metadata including:

* Filename
* Owner
* Department
* File type
* Confidentiality level
* Processing status
* Creation timestamp

Document processing lifecycle:

```text
PROCESSING
     │
     ├──────────────→ READY
     │
     └──────────────→ FAILED
```

Users can delete their own documents, while administrators can manage documents across users.

---

## 🧠 Permission-Aware RAG

DocuAware does not simply retrieve documents and then attempt to filter the response.

**Authorization is applied before retrieval.**

The RAG pipeline is:

```text
User Question
      ↓
JWT Authentication
      ↓
Permission / Metadata Filtering
      ↓
Qdrant Vector Retrieval
      ↓
Top 10 Chunks
      ↓
BGE Reranking
      ↓
Top 5 Chunks
      ↓
Prompt Construction
      ↓
Gemini
      ↓
Answer + Sources
```

This ensures that unauthorized documents are excluded before their content can enter the LLM context.

---

## 🔎 Search Scopes

Users can select between two search scopes.

### My Documents

Search only documents owned by the current user.

### All Accessible Documents

Search across documents the current user is authorized to access.

The access model considers:

* Document ownership
* Confidentiality
* User department

### Access Rules

| Document     | Owner | Same Department | Other Users |
| ------------ | :---: | :-------------: | :---------: |
| PUBLIC       |   ✅   |        ✅        |      ✅      |
| INTERNAL     |   ✅   |        ✅        |      ❌      |
| CONFIDENTIAL |   ✅   |        ❌        |      ❌      |

Administrators have additional document-management privileges.

---

## 🔍 Retrieval & Reranking

Qdrant is used as the vector database.

Current retrieval configuration:

```text
Embedding Dimension: 384
Distance Metric: Cosine
Initial Retrieval: Top 10
Reranked Results: Top 5
```

The retrieval pipeline is:

```text
Question
   ↓
Query Embedding
   ↓
Permission-Aware Qdrant Search
   ↓
Top 10 Candidate Chunks
   ↓
BGE Reranker
   ↓
Top 5 Relevant Chunks
```

Reranking improves the relevance of the context that is ultimately passed to the LLM.

---

## 🤖 LLM Generation

The selected chunks are passed to a prompt builder and then to Gemini for grounded response generation.

The application also returns the document sources associated with the retrieved context.

Example:

```text
Answer:
The document identifies three major findings...

Sources:
📄 research_report.pdf · Chunk 4
📄 research_report.pdf · Chunk 7
📄 research_report.pdf · Chunk 12
```

---

## 📝 AI Document Summarization

DocuAware supports AI-powered document summarization.

Users can generate summaries only for documents they are authorized to access.

The current implementation intentionally uses a straightforward **Summary V1** approach.

Large-document Map-Reduce summarization is not part of the current implementation and can be introduced as a future enhancement.

---

## 🏗️ System Architecture

```text
                         ┌──────────────────────┐
                         │     Streamlit UI     │
                         └──────────┬───────────┘
                                    │
                                    │ HTTP
                                    ▼
                         ┌──────────────────────┐
                         │      FastAPI         │
                         │      REST API        │
                         └──────────┬───────────┘
                                    │
                  ┌─────────────────┼─────────────────┐
                  │                 │                 │
                  ▼                 ▼                 ▼
          ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
          │ PostgreSQL   │  │    Qdrant    │  │    Gemini    │
          │   Metadata   │  │ Vector Store │  │     LLM      │
          └──────────────┘  └──────────────┘  └──────────────┘
                                    ▲
                                    │
                              Embeddings
                              + Reranking
```

### Application Flow

```text
Streamlit
    ↓
API Client
    ↓
FastAPI Router
    ↓
Service Layer
    ↓
┌───────────────┬───────────────┬───────────────┐
│ PostgreSQL    │ Qdrant        │ Gemini        │
│ Metadata      │ Retrieval     │ Generation    │
└───────────────┴───────────────┴───────────────┘
```

The frontend does not directly communicate with PostgreSQL, Qdrant, or Gemini.

---

## 🧩 Technology Stack

| Layer               | Technology            |
| ------------------- | --------------------- |
| Language            | Python                |
| Frontend            | Streamlit             |
| Backend             | FastAPI               |
| API Style           | REST                  |
| Authentication      | JWT                   |
| ORM                 | SQLAlchemy            |
| Relational Database | PostgreSQL            |
| PostgreSQL Hosting  | Neon                  |
| Database Migrations | Alembic               |
| Vector Database     | Qdrant                |
| LLM                 | Google Gemini         |
| RAG Framework       | LangChain             |
| Reranking           | BGE Reranker          |
| Document Formats    | PDF, DOCX, TXT        |
| Configuration       | Environment Variables |
| Version Control     | Git                   |
| CI/CD               | GitHub Actions        |

---

## 🗄️ Data Architecture

PostgreSQL stores application and document metadata.

Qdrant stores vector representations and retrieval metadata.

Raw document content is not stored as a persistent PostgreSQL record.

### User

```text
User
├── id
├── name
├── email
├── hashed_password
├── department
├── role
├── is_active
└── created_at
```

### Document

```text
Document
├── id
├── filename
├── owner_id
├── file_type
├── department
├── confidentiality
├── status
└── created_at
```

---

## 🔄 Document Processing Pipeline

```text
                    Upload
                       ↓
              File Type Detection
                       ↓
                Text Extraction
                       ↓
                    Chunking
                       ↓
               Embedding Generation
                       ↓
                 Qdrant Storage
                       ↓
              PostgreSQL Metadata
                       ↓
                     READY
```

Supported document types:

```text
PDF
DOCX
TXT
```

---

## 🔐 Security Architecture

Security is enforced at the backend rather than relying on the frontend.

Key security practices include:

* JWT authentication
* Password hashing
* Server-side authorization
* Document ownership validation
* Department-based access control
* Confidentiality-based access control
* Permission-aware vector retrieval
* Environment-based secret management
* No direct frontend access to databases or LLM credentials

Example environment configuration:

```env
DATABASE_URL=<neon-postgresql-url>

QDRANT_URL=<qdrant-url>
QDRANT_API_KEY=<qdrant-api-key>

GEMINI_API_KEY=<gemini-api-key>

JWT_SECRET_KEY=<your-secret>
```

> Never commit real credentials, API keys, database URLs containing credentials, or `.env` files to Git.

---

## 🧠 Why LangChain Is Used Selectively

LangChain is used for RAG-related functionality where its abstractions are useful.

It is **not used as the entire application framework**.

Application-level responsibilities remain within the project's own architecture:

```text
FastAPI
├── Authentication
├── Authorization
├── User Management
├── Document Management
├── Metadata Filtering
└── API Layer

RAG Services
├── Retrieval
├── Reranking
├── Prompt Construction
└── LLM Integration
```

This keeps business logic and security concerns independent of the RAG framework.

---

## 🤖 Conventional RAG, Not Agentic RAG

DocuAware currently implements a conventional RAG architecture.

```text
Question
   ↓
Retrieve
   ↓
Rerank
   ↓
Build Context
   ↓
Generate
```

It does not currently use an autonomous agent to plan multi-step tool calls.

Therefore, LangGraph is not required for the current implementation.

---

## 📁 Project Structure

```text
DocuAware/
│
├── backend/
│   ├── app/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── routers/
│   │   ├── services/
│   │   │   ├── retrieval/
│   │   │   ├── reranking/
│   │   │   ├── prompting/
│   │   │   └── llm/
│   │   └── main.py
│   │
│   ├── alembic/
│   │   └── versions/
│   │
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── app.py
│   ├── api.py
│   ├── components/
│   ├── pages/
│   ├── utils/
│   ├── requirements.txt
│   └── .env
│
└── README.md
```

---

## 🔌 API Overview

### Authentication

```http
POST /auth/register
POST /auth/login
GET  /auth/me
```

### Documents

```http
POST   /documents/upload
GET    /documents
DELETE /documents/{document_id}
POST   /documents/{document_id}/summary
```

### RAG

```http
POST /chat
```

FastAPI provides interactive API documentation through Swagger UI:

```text
http://localhost:8000/docs
```

---

## 🖥️ Local Setup

### Prerequisites

* Python 3.10+
* PostgreSQL-compatible database
* Qdrant instance
* Gemini API key

### 1. Clone the repository

```bash
git clone https://github.com/mehra1812shivam/DocuAware.git
cd DocuAware
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

### 3. Install backend dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 4. Configure backend environment variables

Create:

```text
backend/.env
```

Add the required configuration:

```env
DATABASE_URL=<your-database-url>

QDRANT_URL=<your-qdrant-url>
QDRANT_API_KEY=<your-qdrant-api-key>

GEMINI_API_KEY=<your-gemini-api-key>

JWT_SECRET_KEY=<your-jwt-secret>
```

### 5. Run database migrations

```bash
alembic upgrade head
```

### 6. Start the backend

```bash
uvicorn app.main:app --reload
```

Backend:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

---

## 🎨 Start the Frontend

Open another terminal:

```bash
cd frontend
pip install -r requirements.txt
```

Create:

```text
frontend/.env
```

```env
BACKEND_URL=http://localhost:8000
```

Start Streamlit:

```bash
streamlit run app.py
```

---

## 🔁 Typical User Journey

```text
Register
   ↓
Login
   ↓
Upload Document
   ↓
Process Document
   ↓
Document READY
   ↓
Generate Summary
   ↓
Ask Questions
   ↓
Permission-Aware Retrieval
   ↓
Reranking
   ↓
Gemini
   ↓
Answer + Sources
```

---

## 🧪 Testing Scenarios

The application is designed to validate both functionality and authorization.

### Authentication

* User registration
* Duplicate email handling
* Login
* Invalid credentials
* Authenticated user retrieval

### Document Management

* PDF upload
* DOCX upload
* TXT upload
* Document listing
* Document processing status
* Document deletion
* Unauthorized deletion

### Authorization

* Owner access
* Public document access
* Same-department internal access
* Cross-department internal denial
* Confidential document restriction
* Admin document management

### RAG

* Questions against owned documents
* Questions against all accessible documents
* Permission-aware retrieval
* Vector retrieval
* Reranking
* Source attribution
* No-relevant-context scenarios

### Summarization

* Authorized summary generation
* Owner access
* Internal document access
* Confidential document restrictions
* Unauthorized summary attempts

---

## 📌 Design Principles

### Separation of Concerns

Authentication, document management, retrieval, reranking, prompting, and LLM interaction are separated into appropriate layers.

### Backend-Enforced Security

The frontend is never trusted to enforce document permissions.

### Permission-Aware Retrieval

Access control is applied before vector retrieval so unauthorized content does not enter the RAG context.

### Framework Independence

LangChain is used selectively instead of coupling the complete application to it.

### Production-Oriented Engineering

The project incorporates concepts commonly required in real-world backend and GenAI systems:

* REST APIs
* Authentication
* Authorization
* Service-layer architecture
* PostgreSQL
* Database migrations
* Vector databases
* Semantic retrieval
* Reranking
* Prompt construction
* LLM integration
* Environment-based configuration
* CI/CD-ready repository structure

---

## 🚧 Current Scope

The current implementation includes:

* Secure user authentication
* Role and department-based authorization
* Document upload
* PDF/DOCX/TXT processing
* Document metadata management
* Qdrant vector storage
* Permission-aware retrieval
* Semantic reranking
* Gemini-powered answers
* AI document summarization
* Source attribution
* Document deletion
* Streamlit interface

The current RAG pipeline is intentionally **non-agentic** and follows:

```text
Retrieve → Rerank → Generate
```

---

## 🔮 Future Enhancements

Potential future improvements include:

* Streaming LLM responses
* Persistent conversation history
* Improved citation rendering
* Hybrid keyword + vector retrieval
* Query rewriting
* Multi-query retrieval
* Map-Reduce summarization for very large documents
* Agentic workflows using LangGraph
* Background document processing
* Async task queues
* RAG evaluation and automated quality metrics
* Observability and tracing
* Production deployment and CI/CD automation

These are future extensions and are **not part of the current core implementation**.

---

## 💡 What This Project Demonstrates

DocuAware goes beyond a basic:

```text
PDF → Embeddings → LLM
```

implementation.

It combines:

```text
Authentication
      +
Authorization
      +
Document Management
      +
Metadata Filtering
      +
Vector Search
      +
Semantic Reranking
      +
Prompt Construction
      +
LLM Generation
      +
Source Attribution
      +
PostgreSQL Persistence
```

This makes the project a practical demonstration of how RAG can be integrated into a complete backend application with real application-level security and access-control requirements.

---

## 👨‍💻 Author

**Shivam Mehra**

Software Engineer | AI/ML Engineer

Interested in building practical AI systems, RAG applications, cloud-native backends, and production-oriented GenAI solutions.

---

## ⭐ Project

**Repository:**
https://github.com/mehra1812shivam/DocuAware

**Development branch:**
https://github.com/mehra1812shivam/DocuAware/tree/dev
