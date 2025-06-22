from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

# Import the CORRECT class and function names
from app.converters.flowchart_converter import create_flowchart_converter

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize converter
converter = create_flowchart_converter()

@app.route('/api/diagrams/create-flowchart', methods=['GET', 'POST'])
def create_flowchart():
    """Create flowchart from text using dynamic NLP converter"""
    try:
        # Handle GET request for testing
        if request.method == 'GET':
            return jsonify({
                'message': 'Flowchart API is working!',
                'method': 'POST required',
                'content_type': 'application/json',
                'body_format': {'text': 'Your text to convert to flowchart'},
                'example': 'curl -X POST -H "Content-Type: application/json" -d \'{"text":"if user is verified, show dashboard"}\' http://127.0.0.1:5000/api/diagrams/create-flowchart'
            }), 200
        
        # Handle POST request (actual functionality)
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        text_input = data['text']
        logger.info(f"🔄 Processing flowchart request: {text_input[:100]}...")
        
        # Use your dynamic converter
        result = converter.convert_text_to_flowchart(text_input)
        
        # Ensure proper response format
        response = {
            'data': result,
            'message': 'Flowchart generated successfully with Dynamic NLP',
            'generator': 'DynamicFlowchartConverter + spaCy',
            'nodes_count': len(result.get('nodes', [])),
            'edges_count': len(result.get('edges', []))
        }
        
        logger.info(f"✅ Flowchart generated: {response['nodes_count']} nodes, {response['edges_count']} edges")
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"❌ Error creating flowchart: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy', 
        'converter': 'DynamicFlowchartConverter',
        'spacy_loaded': converter.nlp is not None
    }), 200

@app.route('/', methods=['GET'])
def home():
    """Home endpoint"""
    return jsonify({
        'message': 'Dynamic Flowchart API is running!',
        'endpoints': {
            'create_flowchart': 'POST /api/diagrams/create-flowchart',
            'health': 'GET /health'
        }
    }), 200

@app.route('/test', methods=['GET'])
def test_endpoint():
    """Test endpoint that can be accessed via browser"""
    try:
        # Test with sample text
        test_text = "If user is verified, show dashboard. Otherwise, show error."
        
        logger.info(f"🧪 Testing with sample text: {test_text}")
        result = converter.convert_text_to_flowchart(test_text)
        
        return jsonify({
            'status': 'success',
            'test_text': test_text,
            'result': result,
            'nodes_count': len(result.get('nodes', [])),
            'edges_count': len(result.get('edges', [])),
            'mermaid_preview': result.get('mermaid', '')[:200] + '...'
        }), 200
        
    except Exception as e:
        logger.error(f"❌ Test endpoint error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e), 'status': 'failed'}), 500

if __name__ == '__main__':
    print("🚀 Starting Dynamic Flowchart Backend...")
    print("📍 Backend running on: http://127.0.0.1:5000")
    print("🔗 API Endpoint: http://127.0.0.1:5000/api/diagrams/create-flowchart")
    print("💊 Health Check: http://127.0.0.1:5000/health")
    app.run(debug=True, host='0.0.0.0', port=5000)