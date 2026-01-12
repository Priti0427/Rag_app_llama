"""
Document processing module for loading and processing PDF files.
"""

import tempfile
import os
from typing import List
from llama_index.readers.file import PDFReader
from llama_index.core import Document


class DocumentProcessor:
    """Handles document loading and processing."""
    
    def __init__(self):
        """Initialize the document processor."""
        self.reader = PDFReader()
    
    def process_pdf(self, file_content: bytes) -> List[Document]:
        """
        Process PDF file content and return documents.
        
        Args:
            file_content: Raw bytes of the PDF file
            
        Returns:
            List of Document objects
            
        Raises:
            Exception: If PDF processing fails
        """
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                tmp_file.write(file_content)
                tmp_path = tmp_file.name
            
            try:
                # Read PDF
                documents = self.reader.load_data(tmp_path)
                
                # Filter out empty documents
                documents = [doc for doc in documents if doc.text and len(doc.text.strip()) > 0]
                
                return documents
            finally:
                # Clean up temporary file
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)
                    
        except Exception as e:
            raise Exception(f"Error processing PDF: {str(e)}") from e
