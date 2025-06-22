"""
Sequence diagram API endpoints
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.models.schema import DiagramRequest, DiagramResponse

router = APIRouter()

@router.post("/generate", response_model=DiagramResponse)
async def generate_sequence_diagram(request: DiagramRequest):
    """
    Generate a Mermaid sequence diagram from natural language
    
    Args:
        request: DiagramRequest with input text
        
    Returns:
        DiagramResponse: Response with generated Mermaid code
    """
    # Placeholder until sequence diagram converter is implemented
    return DiagramResponse(
        success=True,
        diagram_type="sequence",
        mermaid_code="sequenceDiagram\n    participant User\n    participant System\n    User->>System: Request\n    System-->>User: Response",
        message="Sequence diagram generator coming soon"
    )

@router.get("/examples")
async def get_sequence_examples():
    """
    Get example sequence diagram descriptions
    
    Returns:
        dict: Dictionary of examples
    """
    return {"message": "Sequence diagram examples coming soon"}