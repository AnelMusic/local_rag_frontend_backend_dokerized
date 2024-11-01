# Use Python base image
FROM python:3.9

# Set working directory in the container
WORKDIR /rag_backend

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy the src directory
COPY src/ src/

COPY my_documents/ my_documents/

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]