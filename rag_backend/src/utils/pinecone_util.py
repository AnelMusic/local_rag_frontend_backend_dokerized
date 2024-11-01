from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.pinecone import Pinecone as LangchainPinecone
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, PineconeException, ServerlessSpec

from ..config.config import config
from ..config.logger_config import LoggerConfig

logger = LoggerConfig.setup_console_logger()


# Initialize Pinecone client with error handling
try:
    pc = Pinecone(api_key=config.PINECONE_API_KEY)
except PineconeException as e:
    raise RuntimeError(f"Failed to initialize Pinecone client: {str(e)}")


def store_embedding(chunks, embedding_model):
    """
    Generates and stores embeddings for the provided text chunks in Pinecone.

    Args:
        chunks (List[str]): List of text chunks to be embedded and stored.
        embedding_model: Embedding model to generate the vector embeddings.
        config (dict): Configuration including namespace and index_name.
    """

    # Ensure Pinecone index exists, create it if not found
    if config.PINECONE_INDEX_NAME not in pc.list_indexes().names():
        create_pinecone_index(config.PINECONE_INDEX_NAME)

    # Convert chunks into LangChain Document objects and store embeddings
    store_embeddings_in_pinecone(
        chunks, embedding_model, config.PINECONE_INDEX_NAME, config.PINECONE_NAMESPACE
    )


def create_pinecone_index(index_name):
    """Create a new Pinecone index if it does not exist."""
    logger.info(f"Index '{index_name}' does not exist. Creating it now.")
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region=config.PINECONE_REGION),
    )
    logger.info(f"Index '{index_name}' created successfully.")


def split_text_into_chunks(chunks):
    """Split the input text chunks into smaller, manageable pieces."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE, chunk_overlap=config.CHUNK_OVERLAP
    )
    return [
        split_chunk
        for chunk in chunks
        for split_chunk in text_splitter.split_text(chunk)
    ]


def store_embeddings_in_pinecone(chunks, embedding_model, index_name, namespace):
    """Generate embeddings for the text chunks and store them in Pinecone."""

    documents = [Document(page_content=chunk) for chunk in chunks]

    PineconeVectorStore.from_documents(
        documents=documents,
        embedding=embedding_model,
        index_name=index_name,
        namespace=namespace,
    )


def query_vector_db(query_embedding):
    """
    Function to query the vector database (Pinecone in this case) with the query embedding.

    Args:
        query_embedding (List[float]): The query embedding vector.

    Returns:
        QueryResult: The response from the vector database, containing the most similar documents.
    """
    # Query the Pinecone index with the embedding vector
    index = pc.Index(config.PINECONE_INDEX_NAME)
    result = index.query(
        vector=query_embedding,  # Embedding should be a flat list, not nested in a list
        top_k=1,  # later n = 5 etc
        namespace=config.PINECONE_NAMESPACE,
        include_metadata=True,  # Include the text data in the results
    )
    return result


def get_vector_store(embedding_model):
    """Initializes the Pinecone vector store with the given embedding model."""
    logger.debug(f"Connecting to Pinecone index: {config.PINECONE_INDEX_NAME}")

    return LangchainPinecone.from_existing_index(
        index_name=config.PINECONE_INDEX_NAME,
        embedding=embedding_model,
        namespace=config.PINECONE_NAMESPACE,
    )
