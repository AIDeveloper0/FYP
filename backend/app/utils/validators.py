"""
Utility functions for input validation
"""
import re
from typing import Optional


def validate_input_text(text: str) -> bool:
    """
    Validate that input text is appropriate for diagram generation
    
    Args:
        text: Input text to validate
        
    Returns:
        bool: True if the input is valid
    """
    if not text or not isinstance(text, str):
        return False
    
    # Check minimum length
    if len(text.strip()) < 10:
        return False
    
    # Check maximum length
    if len(text.strip()) > 2000:
        return False
    
    # Must contain some alphabetic characters
    if not re.search(r'[a-zA-Z]', text):
        return False
    
    return True


def validate_mermaid_code(code: str) -> bool:
    """
    Validate that the generated Mermaid code is syntactically valid
    
    Args:
        code: Mermaid diagram code
        
    Returns:
        bool: True if the code is syntactically valid
    """
    if not code or not isinstance(code, str):
        return False
    
    # Basic syntax requirements
    required_elements = ['graph', '[', ']', '-->']
    
    for element in required_elements:
        if element not in code:
            return False
    
    # Check for balanced brackets and parentheses
    brackets = {'[': ']', '(': ')', '{': '}'}
    stack = []
    
    for char in code:
        if char in brackets.keys():
            stack.append(char)
        elif char in brackets.values():
            if not stack:
                return False
            
            last_open = stack.pop()
            if brackets[last_open] != char:
                return False
    
    # Stack should be empty if all brackets are balanced
    return len(stack) == 0