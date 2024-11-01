#!/bin/bash

# Change directory to rag backend
cd rag_backend || exit 1

# Start the uvicorn server
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload