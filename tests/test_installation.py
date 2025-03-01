#!/usr/bin/env python3
"""
Test script to verify that all dependencies are installed correctly.
"""

import sys
import importlib
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def check_dependency(module_name, min_version=None):
    """
    Check if a dependency is installed and meets the minimum version requirement.
    
    Args:
        module_name (str): Name of the module to check
        min_version (str, optional): Minimum version required
        
    Returns:
        bool: True if the dependency is installed and meets the version requirement
    """
    try:
        module = importlib.import_module(module_name)
        if hasattr(module, '__version__'):
            version = module.__version__
        elif hasattr(module, 'VERSION'):
            version = module.VERSION
        elif hasattr(module, 'version'):
            version = module.version
        else:
            version = "Unknown"
            
        if min_version and version != "Unknown":
            from packaging import version as packaging_version
            if packaging_version.parse(version) < packaging_version.parse(min_version):
                logger.warning(f"{module_name} version {version} is installed, but version {min_version} or higher is required")
                return False
                
        logger.info(f"✅ {module_name} (version {version}) is installed")
        return True
    except ImportError:
        logger.error(f"❌ {module_name} is not installed")
        return False

def main():
    """Run the dependency checks."""
    dependencies = [
        # Core dependencies
        ("fastapi", "0.104.0"),
        ("uvicorn", "0.23.0"),
        ("pydantic", "2.4.0"),
        
        # Audio processing
        ("librosa", "0.10.0"),
        ("numpy", "1.24.0"),
        ("whisper", "1.0.0"),
        
        # NLP and AI
        ("transformers", "4.34.0"),
        ("torch", "2.0.0"),
        ("langchain", "0.0.300"),
        ("faiss", None),  # faiss-cpu package
        ("sentence_transformers", "2.2.0"),
        ("google.generativeai", "0.3.0"),
        
        # Document generation
        ("reportlab", "4.0.0"),
        ("dotenv", None),  # python-dotenv package
        
        # Utilities
        ("requests", "2.31.0"),
        ("tqdm", "4.66.0"),
    ]
    
    all_passed = True
    for module_name, min_version in dependencies:
        if not check_dependency(module_name, min_version):
            all_passed = False
    
    if all_passed:
        logger.info("All dependencies are installed correctly! 🎉")
        return 0
    else:
        logger.error("Some dependencies are missing or have incorrect versions. Please check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 