"""
Configuration management for RAG application.
Centralizes all configuration settings with support for environment variables.
"""

import os
from typing import Optional
from dataclasses import dataclass


@dataclass
class Config:
    """Configuration class for RAG application settings."""
    
    # Embedding model configuration
    embedding_model_name: str = "BAAI/bge-small-en-v1.5"
    
    # LLM model configuration
    llm_model_name: str = "Qwen/Qwen2.5-1.5B-Instruct"
    trust_remote_code: bool = False
    revision: str = "main"
    
    # Chunking configuration
    chunk_size: int = 256
    chunk_overlap: int = 15
    
    # Retrieval configuration
    similarity_top_k: int = 2
    similarity_cutoff: float = 0.5
    
    # Generation configuration
    max_new_tokens: int = 512
    num_return_sequences: int = 1
    temperature: float = 0.3
    top_p: float = 0.9
    do_sample: bool = True
    repetition_penalty: float = 1.2
    
    # Device configuration
    device_map: Optional[str] = None  # Set to 'cuda:0' for GPU
    
    @classmethod
    def from_env(cls) -> 'Config':
        """Create Config instance from environment variables."""
        return cls(
            embedding_model_name=os.getenv(
                "EMBEDDING_MODEL_NAME", 
                "BAAI/bge-small-en-v1.5"
            ),
            llm_model_name=os.getenv(
                "LLM_MODEL_NAME", 
                "Qwen/Qwen2.5-1.5B-Instruct"
            ),
            trust_remote_code=os.getenv("TRUST_REMOTE_CODE", "False").lower() == "true",
            revision=os.getenv("REVISION", "main"),
            chunk_size=int(os.getenv("CHUNK_SIZE", "256")),
            chunk_overlap=int(os.getenv("CHUNK_OVERLAP", "15")),
            similarity_top_k=int(os.getenv("SIMILARITY_TOP_K", "2")),
            similarity_cutoff=float(os.getenv("SIMILARITY_CUTOFF", "0.5")),
            max_new_tokens=int(os.getenv("MAX_NEW_TOKENS", "512")),
            num_return_sequences=int(os.getenv("NUM_RETURN_SEQUENCES", "1")),
            temperature=float(os.getenv("TEMPERATURE", "0.3")),
            top_p=float(os.getenv("TOP_P", "0.9")),
            do_sample=os.getenv("DO_SAMPLE", "True").lower() == "true",
            repetition_penalty=float(os.getenv("REPETITION_PENALTY", "1.2")),
            device_map=os.getenv("DEVICE_MAP", None),
        )
