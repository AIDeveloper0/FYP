"""
Data Flow Diagram (DFD) API endpoints
"""
from fastapi import APIRouter, HTTPException

from app.models.schema import DiagramRequest, DiagramResponse

router = APIRouter()

@router.post("/generate", response_model=DiagramResponse)
async def generate_dfd_diagram(request: DiagramRequest):
    """
    Generate a Mermaid DFD from natural language
    
    Args:
        request: DiagramRequest with input text
        
    Returns:
        DiagramResponse: Response with generated Mermaid code
    """
    # Placeholder until DFD converter is implemented
    return DiagramResponse(
        success=True,
        diagram_type="dfd",
        mermaid_code="graph TD\n    User[External Entity: User]\n    Process((Data Processing))\n    DB[(Database)]\n    User -->|Input| Process\n    Process -->|Store| DB\n    Process -->|Output| User",
        message="DFD generator coming soon"
    )

@router.get("/examples")
async def get_dfd_examples():
    """
    Get example DFD descriptions
    
    Returns:
        dict: Dictionary of examples
    """
    return {"message": "DFD examples coming soon"}