from flask import Blueprint, request, jsonify
import logging
import sys
import os

# Add converters to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'converters'))

try:
    from flowchart_converter import create_flowchart_converter
except ImportError:
    create_flowchart_converter = None

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

diagram_routes = Blueprint('diagram_routes', __name__)

@diagram_routes.route('/create-flowchart', methods=['POST'])
def create_flowchart():
    """Create flowchart - POST method"""
    try:
        logger.info("🔄 Received flowchart creation request")
        
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No JSON data provided'
            }), 400
            
        text_input = data.get('text', '').strip()
        
        logger.info(f"📊 Input text length: {len(text_input)} chars")
        logger.info(f"🔍 Processing: {text_input[:100]}...")
        
        if not text_input:
            logger.warning("❌ Empty text input received")
            return jsonify({
                'success': False,
                'error': 'Text input is required'
            }), 400
        
        # Use flowchart converter
        if create_flowchart_converter:
            logger.info("🤖 Using FlowchartConverter with spaCy NLP")
            converter = create_flowchart_converter()
            flowchart_data = converter.convert_text_to_flowchart(text_input)
            
            logger.info("✅ Flowchart generated successfully!")
            return jsonify({
                'success': True,
                'data': flowchart_data,
                'message': 'Flowchart generated successfully with NLP',
                'generator': 'FlowchartConverter + spaCy',
                'nodes_count': len(flowchart_data.get('nodes', [])),
                'edges_count': len(flowchart_data.get('edges', []))
            })
        else:
            logger.error("❌ FlowchartConverter not available")
            return jsonify({
                'success': False,
                'error': 'Flowchart converter not available'
            }), 500
            
    except Exception as e:
        logger.error(f"💥 Error in create_flowchart: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500

@diagram_routes.route('/create-flowchart', methods=['GET'])
def create_flowchart_demo():
    """Demo endpoint for browser testing - GET method"""
    return jsonify({
        'message': '🔧 This endpoint requires POST request with JSON data',
        'method': 'POST',
        'url': '/api/diagrams/create-flowchart',
        'headers': {'Content-Type': 'application/json'},
        'body_example': {
            'text': 'If user is logged in, show dashboard. Otherwise, show login.'
        },
        'test_commands': [
            'curl -X POST http://127.0.0.1:5000/api/diagrams/create-flowchart -H "Content-Type: application/json" -d "{\\"text\\":\\"If user is logged in, show dashboard.\\"}"',
            'Or visit: http://127.0.0.1:5000/api/diagrams/test'
        ]
    })

@diagram_routes.route('/test', methods=['GET'])
def test_diagrams():
    """Test endpoint - GET method"""
    converter_status = "✅ Available" if create_flowchart_converter else "❌ Not Available"
    
    return jsonify({
        'success': True,
        'message': 'Diagram routes are working! 🎉',
        'flowchart_converter': converter_status,
        'spacy_nlp': 'Enabled',
        'endpoints': {
            'create_flowchart_post': 'POST /api/diagrams/create-flowchart',
            'create_flowchart_demo': 'GET /api/diagrams/create-flowchart (demo info)',
            'test': 'GET /api/diagrams/test',
            'health': 'GET /api/diagrams/health'
        }
    })

@diagram_routes.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint - GET method"""
    try:
        # Test converter
        if create_flowchart_converter:
            converter = create_flowchart_converter()
            test_result = converter.convert_text_to_flowchart("Test input")
            converter_working = len(test_result.get('nodes', [])) > 0
            spacy_loaded = converter.nlp is not None
        else:
            converter_working = False
            spacy_loaded = False
            
        return jsonify({
            'success': True,
            'status': 'healthy',
            'converter_working': converter_working,
            'spacy_loaded': spacy_loaded,
            'timestamp': '2025-06-18T23:30:00Z',
            'test_endpoints': {
                'browser_test': 'http://127.0.0.1:5000/api/diagrams/test',
                'curl_test': 'curl -X POST http://127.0.0.1:5000/api/diagrams/create-flowchart -H "Content-Type: application/json" -d "{\\"text\\":\\"test\\"}"'
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'status': 'error',
            'error': str(e)
        })