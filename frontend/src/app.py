import requests
import streamlit as st
import os
from pathlib import Path
from dotenv import load_dotenv

# Try to load .env from parent directory
env_path = Path(__file__).parent.parent / '.env'
if env_path.exists():
    load_dotenv(env_path)

# Get BACKEND_QUERY_URL from env or use default/raise error
BACKEND_QUERY_URL = os.getenv('BACKEND_QUERY_URL')
if not BACKEND_QUERY_URL:
    raise ValueError("BACKEND_QUERY_URL not found in environment variables or .env file")


# Set the app layout to "wide"
st.set_page_config(layout="centered", page_title="AI Question Answering")

# App title and description
st.title("Ask Your Question to GPT-4o")
st.write("Type a question and get an AI-generated answer.")

# Create a text input for the user query
user_query = st.text_area("Enter your question below:", height=100)

# API URL

# Display the API URL for debugging purposes
st.text(f"Backend API URL: {BACKEND_QUERY_URL}")

# Add a button to submit the query
if st.button("Get Answer"):
    if user_query.strip() == "":
        st.error("Please enter a question before submitting.")
    else:
        with st.spinner("Generating answer..."):
            try:

                # Send a POST request to the FastAPI endpoint
                response = requests.post(BACKEND_QUERY_URL, json={"query": user_query})

                if response.status_code == 200:
                    response_data = response.json()
                    st.text_area(
                        "Generated Answer",
                        response.json()["answer"],
                        height=200,
                        disabled=True,
                    )
                else:
                    st.error(
                        f"Error: {response.status_code}. Unable to get the answer."
                    )
            except Exception as e:
                st.error(f"An error occurred: {e}")
