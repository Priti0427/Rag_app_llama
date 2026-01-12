"""
RAG Application Package
A modular RAG (Retrieval-Augmented Generation) system for PDF question answering.
"""

from .rag_system import RAGSystem
from .config import Config

__all__ = ['RAGSystem', 'Config']
__version__ = '1.0.0'
