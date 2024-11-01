#!/bin/bash

# Change directory to rag backend
cd frontend || exit 1

# Start the uvicorn server
streamlit run src/app.py
