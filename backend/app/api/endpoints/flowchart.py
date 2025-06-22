"""
Flowchart API endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
import logging

from app.converters.flowchart_converter import FlowchartConverter
from app.models.schema import DiagramRequest, DiagramResponse
from app.utils.validators import validate_input_text

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize flowchart converter
flowchart_converter = FlowchartConverter()

@router.post("/generate", response_model=DiagramResponse)
async def generate_flowchart(request: DiagramRequest):
    """
    Generate a Mermaid flowchart diagram from natural language
    
    Args:
        request: DiagramRequest with input text
        
    Returns:
        DiagramResponse: Response with generated Mermaid code
    """
    logger.info(f"Flowchart generation request received: {request.text[:50]}...")
    
    # Validate input
    if not validate_input_text(request.text):
        logger.warning(f"Invalid input: {request.text[:50]}...")
        raise HTTPException(status_code=400, detail="Invalid input text. Please provide a more detailed description.")
    
    # Generate flowchart
    mermaid_code = flowchart_converter.convert(request.text)
    
    # Create response
    response = DiagramResponse(
        diagram_type="flowchart",
        mermaid_code=mermaid_code,
        success=True,
        message="Flowchart generated successfully"
    )
    
    # Check if an error occurred during conversion
    stats = flowchart_converter.get_stats()
    if stats["error_occurred"]:
        response.success = False
        response.message = f"Warning: {stats['error_message']}"
    
    return response

@router.get("/examples")
async def get_flowchart_examples():
    """
    Get example flowchart descriptions and their generated diagrams
    
    Returns:
        dict: Dictionary of examples
    """
    examples = [
        {
            "description": "User registration process where system collects user information if validation successful then create account and send welcome email else show error message",
            "name": "User Registration Process"
        },
        {
            "description": "Order processing if payment approved then ship product else refund payment",
            "name": "Order Processing"
        },
        {
            "description": "First collect data then validate input then process request finally return results",
            "name": "Data Processing Sequence"
        },
        {
            "description": "Login system where user attempts to log in if credentials valid and account active then grant access and log activity if credentials invalid or account locked then show error message and increase security counter",
            "name": "Complex Login Process"
        }
    ]
    
    # Generate diagrams for examples
    for example in examples:
        example["mermaid_code"] = flowchart_converter.convert(example["description"])
    
    return {"examples": examples}