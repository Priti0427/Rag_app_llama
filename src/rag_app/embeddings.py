"""
Embedding model management module.
"""

from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
from .config import Config


class EmbeddingManager:
    """Manages embedding model initialization and configuration."""
    
    def __init__(self, config: Config):
        """
        Initialize the embedding manager.
        
        Args:
            config: Configuration object with embedding settings
        """
        self.config = config
        self.embed_model = None
        self._initialize()
    
    def _initialize(self):
        """Initialize the embedding model and configure LlamaIndex settings."""
        # Initialize embedding model
        self.embed_model = HuggingFaceEmbedding(
            model_name=self.config.embedding_model_name
        )
        
        # Configure LlamaIndex global settings
        Settings.embed_model = self.embed_model
        Settings.llm = None  # LLM is handled separately
        Settings.chunk_size = self.config.chunk_size
        Settings.chunk_overlap = self.config.chunk_overlap
    
    def get_embed_model(self):
        """Get the embedding model instance."""
        return self.embed_model
