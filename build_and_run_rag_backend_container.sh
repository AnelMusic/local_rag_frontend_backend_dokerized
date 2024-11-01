#!/bin/bash
set -e

cd rag_backend || exit 1

docker build -t rag-backend .
docker run -p 8000:8000 --env-file ./.env rag-backend