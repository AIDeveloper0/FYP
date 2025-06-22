"""
Class diagram API endpoints
"""
from fastapi import APIRouter, HTTPException

from app.models.schema import DiagramRequest, DiagramResponse

router = APIRouter()

@router.post("/generate", response_model=DiagramResponse)
async def generate_class_diagram(request: DiagramRequest):
    """
    Generate a Mermaid class diagram from natural language
    
    Args:
        request: DiagramRequest with input text
        
    Returns:
        DiagramResponse: Response with generated Mermaid code
    """
    # Placeholder until class diagram converter is implemented
    return DiagramResponse(
        success=True,
        diagram_type="class",
        mermaid_code="classDiagram\n    class User {\n        +String name\n        +isAuthenticated() bool\n    }\n    class System {\n        +process()\n    }\n    User --> System",
        message="Class diagram generator coming soon"
    )

@router.get("/examples")
async def get_class_examples():
    """
    Get example class diagram descriptions
    
    Returns:
        dict: Dictionary of examples
    """
    return {"message": "Class diagram examples coming soon"}