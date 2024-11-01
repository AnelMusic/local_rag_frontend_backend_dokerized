from pathlib import Path
from typing import Any

from ..config.config import config

from ..config.logger_config import LoggerConfig
from ..utils.pinecone_util import store_embedding

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter

logger = LoggerConfig.setup_console_logger()


def get_embedding_model():
    """Initializes the OpenAI embedding model."""
    logger.debug("Initializing OpenAI embedding model")
    return OpenAIEmbeddings(model=config.EMBEDDING_MODEL)


def retrieve_documents(vectorstore, query, top_k=3):
    """Retrieves relevant documents using similarity search."""
    logger.debug(f"Performing similarity search with k={top_k}")
    relevant_docs = vectorstore.similarity_search(query, k=top_k)
    logger.info(f"Retrieved {len(relevant_docs)} relevant documents")
    return relevant_docs


def combine_documents(docs):
    """Formats the source documents for returning as context."""
    formatted_docs = []
    for doc in docs:
        if hasattr(doc, "page_content"):
            formatted_docs.append(doc.page_content)
    return "\n\n".join(formatted_docs)


def generate_response(relevant_docs, query):
    """Generates the response using a RAG chain based on the provided documents and query."""
    chat_model = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        max_tokens=500,
    )
    prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are a helpful assistant that answers questions based on the provided context.
                      If you don't know the answer based on the context, say "I don't have enough information to answer this question."
                      Only use information from the provided context to answer the question.""",
            ),
            ("user", """Context: {context}\n\nQuestion: {question}"""),
        ]
    )

    rag_chain = (
        {
            "context": lambda x: combine_documents(relevant_docs),
            "question": RunnablePassthrough(),
        }
        | prompt_template
        | chat_model
        | StrOutputParser()
    )

    logger.debug("Executing response generation")
    return rag_chain.invoke(query)


def process_pdf_directory(
    directory: Path, text_splitter: CharacterTextSplitter, embedding_model: Any
) -> tuple[list[str], int]:
    """
    Process all PDF files in a directory for embedding.
    """
    pdf_files = list(directory.glob("*.pdf"))
    logger.info(f"Found {len(pdf_files)} PDF files to process")

    if not pdf_files:
        logger.warning(f"No PDF files found in directory: {directory}")
        return [], 0

    failed_files = []
    success_count = 0

    for pdf_path in pdf_files:
        try:
            loader = PyPDFLoader(str(pdf_path))
            pages = loader.load()
            split_docs = text_splitter.split_documents(pages)
            split_docs_texts = [
                doc.page_content for doc in split_docs if doc.page_content
            ]
            store_embedding(split_docs_texts, embedding_model)
            success_count += 1

        except Exception as e:
            logger.error(f"Error processing {pdf_path}: {str(e)}", exc_info=True)
            failed_files.append(pdf_path.name)

    return failed_files, success_count
