"""
Main RAG system orchestrator.
Coordinates all components to provide a unified RAG interface.
"""

from typing import Optional
from llama_index.core.query_engine import RetrieverQueryEngine

from .config import Config
from .document_processor import DocumentProcessor
from .embeddings import EmbeddingManager
from .models import LLMModel
from .query_engine import QueryEngineBuilder
from .prompts import PromptTemplate


class RAGSystem:
    """Main RAG system that orchestrates all components."""
    
    def __init__(self, config: Optional[Config] = None):
        """
        Initialize the RAG system.
        
        Args:
            config: Configuration object. If None, uses default config.
        """
        self.config = config or Config.from_env()
        
        # Initialize components
        self.embedding_manager = EmbeddingManager(self.config)
        self.llm_model = LLMModel(self.config)
        self.document_processor = DocumentProcessor()
        self.query_engine_builder = QueryEngineBuilder(self.config)
        self.prompt_template = PromptTemplate()
    
    def process_pdf(self, file_content: bytes) -> bool:
        """
        Process a PDF file and build the index.
        
        Args:
            file_content: Raw bytes of the PDF file
            
        Returns:
            True if processing succeeded, False otherwise
        """
        try:
            # Process PDF into documents
            documents = self.document_processor.process_pdf(file_content)
            
            if not documents:
                return False
            
            # Build index
            self.query_engine_builder.build_index(documents)
            
            return True
            
        except Exception as e:
            print(f"Error processing PDF: {str(e)}")
            return False
    
    def get_query_engine(self, top_k: Optional[int] = None) -> RetrieverQueryEngine:
        """
        Get a query engine for querying the indexed documents.
        
        Args:
            top_k: Number of top documents to retrieve (overrides config if provided)
            
        Returns:
            RetrieverQueryEngine instance
            
        Raises:
            ValueError: If no index is available
        """
        return self.query_engine_builder.get_query_engine(top_k=top_k)
    
    def generate_response(
        self, 
        query_engine: RetrieverQueryEngine, 
        query: str
    ) -> str:
        """
        Generate a response to a query using RAG.
        
        Args:
            query_engine: Query engine instance
            query: User query/question
            
        Returns:
            Generated response text
        """
        try:
            if not query_engine:
                return "Error: Query engine is not initialized."
            
            # Retrieve relevant context
            response = query_engine.query(query)
            
            # Extract context from source nodes
            context = ""
            top_k = self.config.similarity_top_k
            for node in response.source_nodes[:top_k]:
                context += f"{node.text}\n\n"
            
            if not context.strip():
                return "No relevant information from PDF document"
            
            # Create prompt
            prompt = self.prompt_template.create_prompt(context, query)
            
            # Generate response using LLM
            response_text = self.llm_model.generate(prompt)
            
            return response_text if response_text else "Unable to generate a response from PDF documents"
            
        except Exception as e:
            print(f"Error generating a response: {str(e)}")
            return f"Error processing your question: {str(e)}"
