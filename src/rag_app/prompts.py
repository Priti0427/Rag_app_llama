"""
Prompt template management module.
"""

from typing import Optional


class PromptTemplate:
    """Manages prompt templates for RAG responses."""
    
    DEFAULT_TEMPLATE = """you are an AI assistant tasked with answering question based on the provided PDF content.
Please analyze the following excerpt from the PDF and answer the question.
PDF content:
{context}

Question : {query}

Instructions:
- Answer only based on the information provided in the PDF content above.
- If the answer cannot be found in the provided content, say " I cannot find the answer to the question and provide a pdf documents"
- BE concise and specific.
- Include relevant quote or references from the PDF when applicable.

Answer:
"""
    
    def __init__(self, template: Optional[str] = None):
        """
        Initialize prompt template.
        
        Args:
            template: Custom prompt template. If None, uses default template.
        """
        self.template = template or self.DEFAULT_TEMPLATE
    
    def create_prompt(self, context: str, query: str) -> str:
        """
        Create a prompt from context and query.
        
        Args:
            context: Retrieved context from documents
            query: User query/question
            
        Returns:
            Formatted prompt string
        """
        return self.template.format(context=context, query=query)
    
    def set_template(self, template: str):
        """
        Set a custom prompt template.
        
        Args:
            template: New prompt template with {context} and {query} placeholders
        """
        self.template = template
