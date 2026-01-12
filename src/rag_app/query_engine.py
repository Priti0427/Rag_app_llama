"""
Query engine and retriever setup module.
"""

from llama_index.core import VectorStoreIndex
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.core import Document
from typing import List
from .config import Config


class QueryEngineBuilder:
    """Builds and configures query engines for RAG."""
    
    def __init__(self, config: Config):
        """
        Initialize the query engine builder.
        
        Args:
            config: Configuration object with retrieval settings
        """
        self.config = config
        self.index = None
    
    def build_index(self, documents: List[Document]) -> VectorStoreIndex:
        """
        Build a vector store index from documents.
        
        Args:
            documents: List of Document objects
            
        Returns:
            VectorStoreIndex instance
        """
        if not documents:
            raise ValueError("Cannot build index from empty document list")
        
        self.index = VectorStoreIndex.from_documents(documents)
        return self.index
    
    def get_query_engine(self, top_k: Optional[int] = None) -> RetrieverQueryEngine:
        """
        Create and return a query engine.
        
        Args:
            top_k: Number of top documents to retrieve (overrides config if provided)
            
        Returns:
            RetrieverQueryEngine instance
            
        Raises:
            ValueError: If index is not built yet
        """
        if not self.index:
            raise ValueError("No index available. Please build an index first.")
        
        # Use provided top_k or config default
        similarity_top_k = top_k if top_k is not None else self.config.similarity_top_k
        
        # Create retriever
        retriever = VectorIndexRetriever(
            index=self.index,
            similarity_top_k=similarity_top_k,
        )
        
        # Create query engine with postprocessor
        query_engine = RetrieverQueryEngine(
            retriever=retriever,
            node_postprocessors=[
                SimilarityPostprocessor(
                    similarity_cutoff=self.config.similarity_cutoff
                )
            ]
        )
        
        return query_engine
    
    def get_index(self) -> VectorStoreIndex:
        """Get the current index."""
        return self.index
