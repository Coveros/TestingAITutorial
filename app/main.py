from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import logging
from dotenv import load_dotenv
from app.rag_pipeline import RAGPipeline
import time
import traceback

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO')))
logger = logging.getLogger(__name__)

# Configure Flask with correct template and static directories
template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
CORS(app)

# Initialize RAG pipeline
rag_pipeline = None

def initialize_rag():
    """Initialize the RAG pipeline with error handling."""
    global rag_pipeline
    try:
        rag_pipeline = RAGPipeline()
        logger.info("RAG pipeline initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize RAG pipeline: {str(e)}")
        logger.error(traceback.format_exc())
        return False

@app.route('/')
def index():
    """Serve the main chat interface."""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat requests and return responses."""
    start_time = time.time()
    
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({
                'error': 'No message provided',
                'status': 'error'
            }), 400
        
        user_message = data['message'].strip()
        if not user_message:
            return jsonify({
                'error': 'Empty message provided',
                'status': 'error'
            }), 400
        
        # Check if RAG pipeline is initialized
        if rag_pipeline is None:
            if not initialize_rag():
                return jsonify({
                    'error': 'RAG pipeline not available',
                    'status': 'error'
                }), 500
        
        # Get response from RAG pipeline
        response_data = rag_pipeline.query(user_message)
        
        # Calculate response time
        response_time = time.time() - start_time
        
        # Add metadata to response
        response_data['response_time'] = round(response_time, 3)
        response_data['status'] = 'success'
        
        logger.info(f"Query processed successfully in {response_time:.3f}s")
        return jsonify(response_data)
        
    except Exception as e:
        response_time = time.time() - start_time
        error_msg = f"Error processing query: {str(e)}"
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        
        return jsonify({
            'error': error_msg,
            'status': 'error',
            'response_time': round(response_time, 3)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    try:
        # Check if RAG pipeline is working
        if rag_pipeline is None:
            if not initialize_rag():
                return jsonify({
                    'status': 'unhealthy',
                    'cohere_client': False,
                    'vector_db': False,
                    'collection': False,
                    'documents_loaded': False,
                    'error': 'Failed to initialize RAG pipeline'
                }), 500
        
        # Get detailed health status from RAG pipeline
        health_status = rag_pipeline.health_check()
        health_status['status'] = 'healthy' if all(health_status.values()) else 'unhealthy'
        
        return jsonify(health_status)
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'cohere_client': False,
            'vector_db': False,
            'collection': False,
            'documents_loaded': False,
            'error': str(e)
        }), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get pipeline statistics for testing purposes."""
    try:
        if rag_pipeline is None:
            return jsonify({'error': 'RAG pipeline not initialized'}), 500
        
        stats = rag_pipeline.get_stats()
        return jsonify(stats)
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Initialize RAG pipeline on startup
    logger.info("Starting GenAI Testing Tutorial Application...")
    
    if not initialize_rag():
        logger.warning("RAG pipeline initialization failed, but starting server anyway")
    
    # Get configuration from environment
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    logger.info(f"Starting Flask server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)