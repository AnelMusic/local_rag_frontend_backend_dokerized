from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    """Request model for query endpoint."""

    query: str = Field(..., description="The question to ask about the documents")


class EmbedDirectoryRequest(BaseModel):
    """Request model for directory embedding endpoint."""

    directory: str = Field(
        ..., description="Path to the directory containing PDF files"
    )
