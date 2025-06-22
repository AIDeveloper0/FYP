"""
API Router configuration
"""
from fastapi import APIRouter
from app.api.endpoints import flowchart, sequence, class_diagram, usecase, dfd
from app.core.config import settings

api_router = APIRouter(prefix=settings.API_V1_STR)

# Include all endpoint routers
api_router.include_router(flowchart.router, prefix="/flowchart", tags=["flowchart"])
api_router.include_router(sequence.router, prefix="/sequence", tags=["sequence"])
api_router.include_router(class_diagram.router, prefix="/class", tags=["class-diagram"])
api_router.include_router(usecase.router, prefix="/usecase", tags=["usecase"])
api_router.include_router(dfd.router, prefix="/dfd", tags=["dfd"])