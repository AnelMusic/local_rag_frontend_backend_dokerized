#!/bin/bash

# Create frontend .env file
echo "Creating frontend .env file..."
cd frontend
echo "BACKEND_QUERY_URL=http://host.docker.internal:8000/query" > .env
echo "Frontend .env file created successfully."

# Create backend .env file
echo "Creating rag_backend .env file..."
cd ../rag_backend
cat > .env << EOL
PINECONE_API_KEY=""
PINECONE_REGION=""
OPENAI_API_KEY=""
PINECONE_INDEX_NAME=""
PINECONE_NAMESPACE=""
BACKEND_QUERY_URL=http://host.docker.internal:8000/query
EOL
echo "Backend .env file created successfully."


echo "Environment files have been created successfully!"
echo "Please remember to fill in your API keys and other values in rag_backend/.env"