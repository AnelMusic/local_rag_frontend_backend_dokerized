import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Set

from dotenv import load_dotenv


@dataclass
class Config:
    """Configuration class to manage environment variables and settings with validation."""

    # Environment variables that will be loaded after environment setup
    OPENAI_API_KEY: str = field(default=None)
    PINECONE_API_KEY: str = field(default=None)
    PINECONE_REGION: str = field(default=None)
    PINECONE_INDEX_NAME: str = field(default=None)
    PINECONE_NAMESPACE: str = field(default=None)

    # Configuration settings with default values
    EMBEDDING_MODEL: str = "text-embedding-ada-002"
    LLM_MODEL: str = "gpt-4o-mini"
    CHUNK_SIZE: int = 2000
    CHUNK_OVERLAP: int = 50

    # Class-level constants
    ALLOWED_MODELS: Dict[str, Set[str]] = field(default_factory=lambda: {
        "EMBEDDING_MODEL": {"text-embedding-ada-002"},
        "LLM_MODEL": {"gpt-4o-mini"},
    })

    def __post_init__(self):
        """Initialize and validate configuration."""
        self._load_environment()
        self._load_env_variables()
        self._validate()

    def _load_environment(self) -> None:
        """Load environment variables, prioritizing .env file over system environment variables."""
        # Try loading from .env file first
        env_path = Path(__file__).resolve().parent.parent.parent / ".env"
        print(f"Checking for .env at: {env_path}")
        
        if env_path.exists():
            print(f"Loading environment from file: {env_path}")
            load_dotenv(dotenv_path=env_path, override=True)
        else:
            print(".env file not found, will use system environment variables")

    def _load_env_variables(self) -> None:
        """Load environment variables into class attributes after environment is set up."""
        env_vars = {
            "OPENAI_API_KEY": "OPENAI_API_KEY",
            "PINECONE_API_KEY": "PINECONE_API_KEY",
            "PINECONE_REGION": "PINECONE_REGION",
            "PINECONE_INDEX_NAME": "PINECONE_INDEX_NAME",
            "PINECONE_NAMESPACE": "PINECONE_NAMESPACE",
        }
        
        for attr, env_var in env_vars.items():
            setattr(self, attr, os.getenv(env_var))

    def _validate(self) -> None:
        """Comprehensive validation of all configuration settings."""
        # Validate required environment variables
        required_env_vars = {
            "OPENAI_API_KEY": self.OPENAI_API_KEY,
            "PINECONE_API_KEY": self.PINECONE_API_KEY,
            "PINECONE_REGION": self.PINECONE_REGION,
            "PINECONE_INDEX_NAME": self.PINECONE_INDEX_NAME,
            "PINECONE_NAMESPACE": self.PINECONE_NAMESPACE,
        }

        missing_vars = [key for key, value in required_env_vars.items() if not value]
        if missing_vars:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_vars)}"
            )

        # Validate model names
        for model_type, allowed_values in self.ALLOWED_MODELS.items():
            model_value = getattr(self, model_type)
            if model_value not in allowed_values:
                raise ValueError(
                    f"Invalid {model_type}: {model_value}. "
                    f"Must be one of: {', '.join(allowed_values)}"
                )

        # Validate chunk settings
        if not isinstance(self.CHUNK_SIZE, int) or self.CHUNK_SIZE <= 0:
            raise ValueError("CHUNK_SIZE must be a positive integer")

        if not isinstance(self.CHUNK_OVERLAP, int) or self.CHUNK_OVERLAP < 0:
            raise ValueError("CHUNK_OVERLAP must be a non-negative integer")

        if self.CHUNK_OVERLAP >= self.CHUNK_SIZE:
            raise ValueError(
                f"CHUNK_OVERLAP ({self.CHUNK_OVERLAP}) must be less than CHUNK_SIZE ({self.CHUNK_SIZE})"
            )

    def as_dict(self) -> Dict[str, str]:
        """Return configuration as a dictionary for logging purposes."""
        return {
            key: str(value) 
            for key, value in self.__dict__.items() 
            if not key.startswith('_') and key.isupper()
        }


# Create singleton instance
config = Config()