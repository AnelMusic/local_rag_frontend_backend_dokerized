# Local RAG System

A containerized Retrieval-Augmented Generation (RAG) system with Streamlit frontend and document processing backend. This project serves as a starter template for your local RAG applications.
Due to containerization porting to cloud e.g AWS Fargate should be fairly easy as well.

## 🏗️ Architecture

- **Frontend**: Streamlit-based web interface
- **Backend**: RAG processing service
- **Vector Database**: Pinecone
- **Models**: OpenAI for embeddings and instruction following
- **Document Storage**: Local filesystem (my_documents)

## 🚀 Quick Start

### Prerequisites

- Docker
- Python 3.10+
- OpenAI API Key (code could easily be modified for other model providers)
- Pinecone API Key (code could easily be modified for other vector db services)

### Environment Setup

1. Clone the repository

```bash
git clone https://github.com/AnelMusic/local_rag_frontend_backend_dokerized
cd local_rag_frontend_backend_dokerized
```

2. Set up environment variables in both `.env` files and add your tokens to rag_backend/.env:

   - `frontend/.env`
   - `rag_backend/.env`
```bash
./create_env_files.sh
```
- Use create_env_files.sh to automatically create the .env (Don't forget to update Pinecone and OpenAI Token)


### Running the Application

1. Build and run the backend container:

```bash
./build_and_run_rag_backend_container.sh
```

2. Build and run the frontend container:

```bash
./build_and_run_frontend_container.sh
```

3. Access the application at `http://localhost:8501`

## 📁 Project Structure

```
local-rag/
├── frontend/
│   ├── src/
│   │   ├── app.py          # Streamlit application
│   │   └── __init__.py
│   ├── Dockerfile
│   └── requirements.txt create_env_files
│   └── .env 
│
├── rag_backend/
│   ├── my_documents/       # Document storage
│   ├── src/
│   │   ├── config/        # Configuration management
│   │   ├── utils/         # Utility functions
│   │   └── main.py        # Backend service entry point
│   ├── tests/             # Test suite 
│   └── Dockerfile
│   └── .env
│
└── scripts/
    ├── build_and_run_frontend_container.sh
    └── build_and_run_rag_backend_container.sh
    └── create_env_files.sh
```

## 🔧 Configuration

### Backend Configuration

- Configure document processing settings in `rag_backend/src/config/config.py`
- Logging configuration in `rag_backend/src/config/logger_config.py`
- API models defined in `rag_backend/src/api_models.py`

### Frontend Configuration

- Streamlit settings in `frontend/src/app.py`

## 📚 API Documentation

The RAG backend service exposes the following RESTful endpoints:

### Health Check
```http
GET /
```
Returns basic API information and available endpoints.

**Response Example:**
```json
{
    "message": "Welcome to the Document QA API",
    "version": "2.0.0",
    "endpoints": {
        "/query": "Query the document database",
        "/embed_directory": "Embed PDF documents from a directory"
    }
}
```

### Query Documents
```http
POST /query
```
Queries the vector database using RAG (Retrieval-Augmented Generation) to answer questions based on embedded documents.

**Request Body:**
```json
{
    "query": "What is the main topic of the document?"
}
```

**Response Example:**
```json
{
    "answer": "The detailed answer based on the documents...",
    "source_documents": "Relevant excerpts from the source documents..."
}
```

**Postman Setup:**
1. Create a new POST request to `http://localhost:8000/query`
2. Set Content-Type header to `application/json`
3. In the request body tab, select "raw" and "JSON"
4. Enter your query JSON

### Embed Documents
```http
POST /embed_directory
```
Processes and embeds PDF documents from a specified directory into the vector database.

**Request Body:**
```json
{
    "directory": "/path/to/documents"
}
```

**Response Example (Success):**
```json
{
    "message": "Embedding process completed successfully",
    "processed_files": 5
}
```

**Response Example (Partial Success):**
```json
{
    "message": "Embedding process completed with errors",
    "failed_files": ["doc1.pdf", "doc2.pdf"],
    "successful_files": 3
}
```

**Postman Setup:**
1. Create a new POST request to `http://localhost:8000/embed_directory`
2. Set Content-Type header to `application/json`
3. In the request body tab, select "raw" and "JSON"
4. Enter your directory path JSON

### Error Handling

All endpoints include proper error handling with appropriate HTTP status codes:
- `400`: Bad Request (e.g., invalid directory path)
- `500`: Internal Server Error (with detailed error messages)

### Testing with Curl

You can also test the endpoints using curl:

```bash
# Health check
curl http://localhost:8000/

# Query documents
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Is there corruption in Bosnia?"}'

# Embed documents
curl -X POST http://localhost:8000/embed_directory \
  -H "Content-Type: application/json" \
  -d '{"directory": "/rag_backend/my_documents"}'
```

### Examplary Postman config:
#### QA Query:
![image](https://github.com/user-attachments/assets/e0427d0a-c102-4803-bcc2-368484edda1a)
#### Embedd Directory:
![image](https://github.com/user-attachments/assets/23661eb0-2965-4a6c-a242-1ca84b69d282)

## 🌩️ Cloud Deployment

1. Push Docker images to Amazon ECR
2. Deploy containers using AWS Fargate
3. Replace local document storage with S3
4. Configure appropriate IAM roles and security groups
5. Set up Application Load Balancer for the frontend

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## ⚠️ Disclaimer

This is a starter template and may need additional security and performance optimizations for production use.
