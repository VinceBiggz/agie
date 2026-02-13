"""
Diagnostic script to list available Gemini models for your API key.

This helps identify the correct model identifier to use.

@author: Vincent Wachira
@date: 2025-02-14
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from google import genai
from dotenv import load_dotenv
from src.logger import logger

load_dotenv()

logger.info("=" * 70)
logger.info("GEMINI MODEL AVAILABILITY CHECK")
logger.info("=" * 70)

try:
    # Create client
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        logger.error("GOOGLE_API_KEY not found in .env")
        sys.exit(1)
    
    client = genai.Client(api_key=api_key)
    logger.info("✓ Client created successfully")
    
    # List all available models
    logger.info("\nAvailable models for your API key:")
    logger.info("-" * 70)
    
    models = list(client.models.list())
    
    if not models:
        logger.warning("No models found! Check your API key permissions.")
    else:
        for model in models:
            logger.info(f"\n  Model: {model.name}")
            logger.info(f"  Display Name: {getattr(model, 'display_name', 'N/A')}")
            logger.info(f"  Description: {getattr(model, 'description', 'N/A')[:80]}...")
            
            # Check if it supports generateContent
            supported_methods = getattr(model, 'supported_generation_methods', [])
            if supported_methods:
                logger.info(f"  Supported Methods: {supported_methods}")
    
    logger.info("-" * 70)
    logger.info(f"\nTotal models available: {len(models)}")
    
    # Recommend which to use
    logger.info("\n" + "=" * 70)
    logger.info("RECOMMENDATIONS:")
    logger.info("=" * 70)
    
    flash_models = [m for m in models if 'flash' in m.name.lower()]
    if flash_models:
        logger.info("\n✓ Flash models (fast & free):")
        for m in flash_models:
            logger.info(f"  • {m.name}")
        logger.info(f"\nRecommended: Use '{flash_models[0].name}' in your gemini_client.py")
    else:
        logger.warning("\n⚠ No Flash models found. Available models:")
        for m in models[:3]:  # Show first 3
            logger.info(f"  • {m.name}")

except Exception as e:
    logger.error(f"Failed to list models: {e}")
    logger.error("Check your GOOGLE_API_KEY is valid")
    sys.exit(1)