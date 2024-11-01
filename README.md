# Local RAG System

A containerized Retrieval-Augmented Generation (RAG) system with Streamlit frontend and document processing backend. This project serves as a starter template for building production-ready RAG applications.

## 🏗️ Architecture

- **Frontend**: Streamlit-based web interface
- **Backend**: RAG processing service
- **Vector Database**: Pinecone
- **Models**: OpenAI for embeddings and instruction following
- **Document Storage**: Local filesystem (my_documents)

## 🚀 Quick Start

### Prerequisites

- Docker
- Python 3.8+
- OpenAI API Key
- Pinecone API Key

### Environment Setup

1. Clone the repository

```bash
git clone [your-repo-url]
cd local-rag
```

2. Set up environment variables in both `.env` files and add your tokens to rag_backend/.env:

   - `frontend/.env`
   - `rag_backend/.env`

   run --> ./create_env_files.sh o not manually create the .env files run:

   ```bash
   ./create_env_files.sh
   ```

### Running the Application

1. Build and start the backend container:

```bash
./build_and_run_rag_backend_container.sh
```

2. Build and start the frontend container:

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

## 🌩️ Cloud Deployment

While this project is set up for local development, it's designed to be cloud-ready. For production deployment:

1. Push Docker images to Amazon ECR
2. Deploy containers using AWS Fargate
3. Replace local document storage with S3
4. Configure appropriate IAM roles and security groups
5. Set up Application Load Balancer for the frontend

## 🧪 Testing

```bash
cd rag_backend
python -m pytest tests/
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## ⚠️ Disclaimer

This is a starter template and may need additional security and performance optimizations for production use.
