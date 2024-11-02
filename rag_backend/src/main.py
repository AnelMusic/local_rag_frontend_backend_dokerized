from pathlib import Path
from typing import Any, Dict

import uvicorn
from .api_models import EmbedDirectoryRequest, QueryRequest
from fastapi import FastAPI, HTTPException, status
from langchain_text_splitters import CharacterTextSplitter

from .config.config import config
from .config.logger_config import LoggerConfig
from .utils.pinecone_util import get_vector_store
from .utils.rag_utils import (combine_documents, generate_response,
                          get_embedding_model, process_pdf_directory,
                          retrieve_documents)

logger = LoggerConfig.setup_console_logger()

app = FastAPI(title="Document QA API", version="2.0.0")



# Landing page route
@app.get("/", status_code=status.HTTP_200_OK)
async def read_root():
    """Landing page endpoint."""
    logger.info("Health check request received")
    return {
        "message": "Welcome to the Document QA API",
        "version": "2.0.0",
        "endpoints": {
            "/query": "Query the document database",
            "/embed_directory": "Embed PDF documents from a directory",
        },
    }


@app.post("/query", response_model=Dict[str, str])
async def query_embedding_endpoint(request: QueryRequest):
    """
    Query endpoint that uses Pinecone vector store for cosine similarity-based retrieval.
    Implements RAG pattern with proper error handling and chain construction.
    """
    logger.info(
        f"Processing query request: {request.query[:50]}..."
    )  # Log first 50 chars for brevity

    try:
        embedding_model = get_embedding_model()
        vectorstore = get_vector_store(embedding_model)
        relevant_docs = retrieve_documents(vectorstore, request.query, top_k=3)
        context = combine_documents(relevant_docs)
        response = generate_response(relevant_docs, request.query)
        return {"answer": response, "source_documents": context}

    except Exception as e:
        logger.error(f"Error processing query: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.post("/embed_directory", response_model=Dict[str, Any])
async def embed_directory_endpoint(request: EmbedDirectoryRequest):
    """Embed directory endpoint using LangChain's sequential processing."""
    logger.info(f"Processing embedding request for directory: {request.directory}")

    # Validate directory
    try:
        directory = Path(request.directory)
        if not directory.is_dir():
            logger.error(f"Invalid directory path: {request.directory}")
            raise HTTPException(status_code=400, detail="Invalid directory path")
    except (TypeError, ValueError) as e:
        logger.error(f"Invalid directory path format: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid directory path format")

    # Initialize components
    try:
        embedding_model = get_embedding_model()
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP,
            length_function=len,
        )
    except Exception as e:
        logger.error(
            f"Failed to initialize embedding components: {str(e)}", exc_info=True
        )
        raise HTTPException(
            status_code=500, detail="Failed to initialize embedding components"
        )

    # Process PDF files
    failed_files, success_count = process_pdf_directory(
        directory=directory,
        text_splitter=text_splitter,
        embedding_model=embedding_model,
    )

    if failed_files:
        return {
            "message": "Embedding process completed with errors",
            "failed_files": failed_files,
            "successful_files": success_count,
        }

    return {
        "message": "Embedding process completed successfully",
        "processed_files": success_count,
    }


if __name__ == "__main__":
    logger.info("Starting Document QA API server")
    uvicorn.run(app, host="0.0.0.0", port=8000)
