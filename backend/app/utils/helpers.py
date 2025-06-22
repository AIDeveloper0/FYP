"""
Helper functions for the application
"""
import re
from typing import Optional


def extract_main_subject(text: str) -> Optional[str]:
    """
    Extract the main subject from a text description
    
    Args:
        text: Text to extract subject from
        
    Returns:
        Optional[str]: Main subject or None if not found
    """
    # Look for common patterns that indicate the main subject
    subject_patterns = [
        # "X process where..."
        r'^([^,\.]+?)\s+(?:process|system|workflow|procedure)\s+where',
        # "In the X process..."
        r'in\s+the\s+([^,\.]+?)\s+(?:process|system|workflow|procedure)',
        # "X system that..."
        r'^([^,\.]+?)\s+(?:system|process)\s+that',
        # "X if Y then Z"
        r'^([^,\.]+?)\s+if\s+',
        # First sentence or clause
        r'^([^,\.]+?)(?:[,\.]|$)'
    ]
    
    for pattern in subject_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            subject = match.group(1).strip()
            # Clean up the subject
            subject = re.sub(r'^\s*(?:the|a|an)\s+', '', subject, flags=re.IGNORECASE)
            # Title case and limit length
            if len(subject) > 40:
                subject = subject[:37] + "..."
            return subject.title()
    
    # If no subject found, take first few words
    words = text.split()
    if words:
        potential_subject = " ".join(words[:min(5, len(words))])
        if len(potential_subject) > 40:
            potential_subject = potential_subject[:37] + "..."
        return potential_subject.title()
    
    return None


def format_mermaid_code(code: str) -> str:
    """
    Format Mermaid code for better readability
    
    Args:
        code: Mermaid code to format
        
    Returns:
        str: Formatted code
    """
    if not code:
        return code
        
    # Split into lines and ensure proper indentation
    lines = code.split('\n')
    formatted_lines = []
    
    for line in lines:
        line = line.strip()
        
        # Add standard indentation for everything except the graph declaration
        if line.startswith('graph '):
            formatted_lines.append(line)
        else:
            formatted_lines.append(f"    {line}")
    
    return '\n'.join(formatted_lines)