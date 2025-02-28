#!/usr/bin/env python3
"""
Main entry point for the Medical Transcription Analysis application.
This script runs the FastAPI application that provides the API endpoints
for the medical transcription service.
"""

import os
import sys
import logging
import uvicorn
from dotenv import load_dotenv

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log")
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Run the FastAPI application using Uvicorn."""
    try:
        logger.info("Starting Medical Transcription Analysis API")
        
        # Import the app here to ensure environment variables are loaded first
        from medical_transcription.api.app import app
        
        # Get port from environment variable or use default
        port = int(os.getenv("PORT", 8000))
        
        # Run the application
        uvicorn.run(
            "medical_transcription.api.app:app",
            host="0.0.0.0",
            port=port,
            reload=True
        )
    except Exception as e:
        logger.error(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 