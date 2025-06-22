"""
Diagram Converter Application Package
"""

__version__ = "1.0.0"

# Import models and converters to make them available
from app.converters.flowchart_converter import DynamicFlowchartConverter
from app.models.schema import DiagramRequest, DiagramResponse
from flask import Flask
from flask_cors import CORS
import logging

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Register blueprints or routes if any
    # app.register_blueprint(...)

    return app