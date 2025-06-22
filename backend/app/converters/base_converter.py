"""
Base converter class that defines the interface for all diagram converters
"""
from abc import ABC, abstractmethod
import re
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class BaseConverter(ABC):
    """
    Abstract base class for all diagram type converters.
    
    Provides common functionality for:
    - Text preprocessing
    - Node management
    - Error handling
    - Output validation
    """
    
    def __init__(self):
        """Initialize the converter with a reset node counter"""
        self.node_counter = 0
        self.error_occurred = False
        self.last_error = None
    
    def reset(self):
        """Reset the converter state"""
        self.node_counter = 0
        self.error_occurred = False
        self.last_error = None
    
    def get_next_node_id(self) -> str:
        """
        Get the next node ID (A, B, C, etc.)
        
        Returns:
            str: The next node ID
        """
        node_id = chr(ord('A') + self.node_counter)
        self.node_counter += 1
        return node_id
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize input text
        
        Args:
            text: Raw input text
            
        Returns:
            str: Cleaned text
        """
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove numbering like "1. ", "2. ", etc.
        text = re.sub(r'^\d+\.\s*', '', text)
        
        return text
    
    def clean_label(self, text: str, max_length: int = 40) -> str:
        """
        Clean text for node labels, removing unnecessary words and limiting length
        
        Args:
            text: Text to clean
            max_length: Maximum length for the label
            
        Returns:
            str: Cleaned label text
        """
        if not text:
            return "Process"
        
        # Remove common articles and demonstratives
        stop_words = ['the', 'a', 'an', 'this', 'that', 'these', 'those']
        text = re.sub(r'\b(' + '|'.join(stop_words) + r')\b\s*', '', text.lower(), flags=re.IGNORECASE)
        
        # Handle long text
        if len(text) > max_length:
            # Try to find natural break points
            if ',' in text:
                text = text.split(',')[0].strip()
            elif ' and ' in text:
                text = text.split(' and ')[0].strip()
            elif len(text.split()) > 7:
                # Take first 7 words
                words = text.split()
                text = ' '.join(words[:7])
                
            # If still too long, truncate with ellipsis
            if len(text) > max_length:
                text = text[:max_length-3] + "..."
        
        # Title case the label
        return text.strip().title() if text.strip() else "Process"
    
    def handle_error(self, error: Exception, fallback_diagram: Optional[str] = None) -> str:
        """
        Handle errors gracefully and provide fallback diagram
        
        Args:
            error: The exception that occurred
            fallback_diagram: Optional fallback diagram to return
            
        Returns:
            str: Fallback diagram code or error diagram
        """
        self.error_occurred = True
        self.last_error = str(error)
        
        logger.error(f"Converter error: {error}")
        
        if fallback_diagram:
            return fallback_diagram
        
        # Default error diagram
        return f"""graph TD
    A[Error Processing Input]
    B[Please Check Your Text]
    A --> B"""
    
    @abstractmethod
    def convert(self, text: str) -> str:
        """
        Convert text input to diagram code
        
        Args:
            text: Input text describing the diagram
            
        Returns:
            str: Generated Mermaid diagram code
        """
        pass
    
    def validate_output(self, diagram_code: str) -> bool:
        """
        Validate the generated diagram code
        
        Args:
            diagram_code: The generated Mermaid diagram code
            
        Returns:
            bool: True if the diagram code is valid
        """
        if not diagram_code:
            return False
        
        # Basic validation - check for syntax elements
        syntax_elements = ['graph', '[', ']', '-->']
        return all(element in diagram_code for element in syntax_elements)
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the conversion process
        
        Returns:
            Dict[str, Any]: Statistics about the conversion
        """
        return {
            "nodes_created": self.node_counter,
            "error_occurred": self.error_occurred,
            "error_message": self.last_error if self.error_occurred else None
        }