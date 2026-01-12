"""
LLM model management module.
"""

from transformers import AutoModelForCausalLM, AutoTokenizer
from typing import Optional
from .config import Config


class LLMModel:
    """Manages LLM model loading and text generation."""
    
    def __init__(self, config: Config):
        """
        Initialize the LLM model.
        
        Args:
            config: Configuration object with model settings
        """
        self.config = config
        self.model = None
        self.tokenizer = None
        self._load_model()
    
    def _load_model(self):
        """Load the model and tokenizer."""
        model_kwargs = {
            "trust_remote_code": self.config.trust_remote_code,
            "revision": self.config.revision,
        }
        
        # Add device_map if specified
        if self.config.device_map:
            model_kwargs["device_map"] = self.config.device_map
        
        # Load model
        self.model = AutoModelForCausalLM.from_pretrained(
            self.config.llm_model_name,
            **model_kwargs
        )
        
        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.config.llm_model_name,
            use_fast=True
        )
    
    def generate(self, prompt: str) -> str:
        """
        Generate text from a prompt.
        
        Args:
            prompt: Input prompt text
            
        Returns:
            Generated text response
        """
        # Tokenize input
        inputs = self.tokenizer(
            prompt, 
            return_tensors="pt", 
            padding=True
        )
        
        # Generate
        outputs = self.model.generate(
            input_ids=inputs['input_ids'],
            max_new_tokens=self.config.max_new_tokens,
            num_return_sequences=self.config.num_return_sequences,
            temperature=self.config.temperature,
            top_p=self.config.top_p,
            do_sample=self.config.do_sample,
            repetition_penalty=self.config.repetition_penalty
        )
        
        # Decode response
        response_text = self.tokenizer.decode(
            outputs[0], 
            skip_special_tokens=True
        )
        
        # Extract answer if present
        if "Answer:" in response_text:
            response_text = response_text.split("Answer:")[-1].strip()
        elif "Answer" in response_text:
            response_text = response_text.split("Answer")[-1].strip()
        
        return response_text
