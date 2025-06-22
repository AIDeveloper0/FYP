"""
Use case diagram API endpoints
"""
from fastapi import APIRouter, HTTPException

from app.models.schema import DiagramRequest, DiagramResponse

router = APIRouter()

@router.post("/generate", response_model=DiagramResponse)
async def generate_usecase_diagram(request: DiagramRequest):
    """
    Generate a Mermaid use case diagram from natural language
    
    Args:
        request: DiagramRequest with input text
        
    Returns:
        DiagramResponse: Response with generated Mermaid code
    """
    # Placeholder until use case diagram converter is implemented
    return DiagramResponse(
        success=True,
        diagram_type="usecase",
        mermaid_code="graph TD\n    User(User)\n    UC1[Login]\n    UC2[Logout]\n    User --> UC1\n    User --> UC2",
        message="Use case diagram generator coming soon"
    )

@router.get("/examples")
async def get_usecase_examples():
    """
    Get example use case diagram descriptions
    
    Returns:
        dict: Dictionary of examples
    """
    return {"message": "Use case diagram examples coming soon"}