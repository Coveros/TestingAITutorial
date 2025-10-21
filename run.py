#!/usr/bin/env python3
"""
GenAI Testing Tutorial - RAG Chatbot Application
Entry point for running the Flask application
"""

import os
import sys
from dotenv import load_dotenv

# Add the app directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

# Load environment variables
load_dotenv()

# Import and run the Flask app
from app.main import app

if __name__ == '__main__':
    # Validate required environment variables
    required_vars = ['COHERE_API_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease add your LLM API Key to the .env file.")
        sys.exit(1)
    
    print("🚀 Starting GenAI Testing Tutorial Application...")
    print(f"📚 Documents directory: {os.path.join(os.path.dirname(__file__), 'data', 'documents')}")
    print(f"🔧 Environment: {os.getenv('FLASK_ENV', 'development')}")
    print(f"🌐 Server will start on: http://localhost:{os.getenv('FLASK_PORT', 5000)}")
    print("\n" + "="*50)
    
    # Start the Flask application
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('FLASK_PORT', 5000)),
        debug=os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    )