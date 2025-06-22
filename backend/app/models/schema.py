"""
Schema definitions for request/response models
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List


class DiagramRequest(BaseModel):
    """
    Request model for diagram generation
    """
    text: str = Field(..., min_length=10, max_length=2000, description="Text description of the diagram")
    options: Optional[Dict[str, Any]] = Field(default=None, description="Optional diagram generation options")


class DiagramResponse(BaseModel):
    """
    Response model for diagram generation
    """
    success: bool = Field(..., description="Whether the generation was successful")
    diagram_type: str = Field(..., description="Type of the diagram")
    mermaid_code: str = Field(..., description="Generated Mermaid diagram code")
    message: Optional[str] = Field(None, description="Additional information or error message")
    nodes: Optional[int] = Field(None, description="Number of nodes in the diagram")
    stats: Optional[Dict[str, Any]] = Field(None, description="Additional statistics about the generated diagram")


class ExampleResponse(BaseModel):
    """
    Response model for diagram examples
    """
    examples: List[Dict[str, Any]] = Field(..., description="List of example diagrams")