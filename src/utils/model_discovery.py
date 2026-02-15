"""
Model discovery and validation utilities for AI clients.

This module provides automatic model discovery and fallback mechanisms
to handle SDK changes and API deprecations gracefully.

@author: Vincent Wachira
@date: 2025-02-14
@version: 0.1.0
@license: MIT
"""

import os
import sys
from pathlib import Path
from typing import List, Optional, Dict
from dataclasses import dataclass

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from google import genai
from dotenv import load_dotenv
from src.logger import logger

load_dotenv()


@dataclass
class ModelInfo:
    """Information about an available AI model."""
    name: str
    display_name: str
    description: str
    supported_methods: List[str]
    provider: str  # 'gemini' or 'claude'


class ModelDiscovery:
    """
    Automatically discover and validate available AI models.
    
    This class provides fallback mechanisms when hardcoded model names
    fail due to API changes or deprecations.
    
    Example:
        >>> discovery = ModelDiscovery()
        >>> model = discovery.get_best_gemini_model('flash')
        >>> print(f"Using: {model}")
    """
    
    def __init__(self):
        """Initialize model discovery service."""
        self.gemini_api_key = os.getenv('GOOGLE_API_KEY')
        logger.info("ModelDiscovery initialized")
    
    def list_gemini_models(self) -> List[ModelInfo]:
        """
        List all available Gemini models.
        
        Returns:
            List of ModelInfo objects
            
        Raises:
            Exception: If API key is invalid or API call fails
        """
        if not self.gemini_api_key:
            logger.error("GOOGLE_API_KEY not found")
            return []
        
        try:
            client = genai.Client(api_key=self.gemini_api_key)
            models = []
            
            for model in client.models.list():
                info = ModelInfo(
                    name=model.name,
                    display_name=getattr(model, 'display_name', model.name),
                    description=getattr(model, 'description', 'N/A'),
                    supported_methods=getattr(model, 'supported_generation_methods', []),
                    provider='gemini'
                )
                models.append(info)
            
            logger.info(f"Found {len(models)} Gemini models")
            return models
            
        except Exception as e:
            logger.error(f"Failed to list Gemini models: {e}")
            return []
    
    def get_best_gemini_model(self, preference: str = 'flash') -> Optional[str]:
        """
        Get the best available Gemini model based on preference.
        
        Args:
            preference: Model type preference ('flash', 'pro', 'ultra')
            
        Returns:
            Model name string, or None if no suitable model found
            
        Example:
            >>> discovery = ModelDiscovery()
            >>> model = discovery.get_best_gemini_model('flash')
            >>> # Returns: 'gemini-2.5-flash' or similar
        """
        models = self.list_gemini_models()
        
        if not models:
            logger.warning("No Gemini models available")
            return None
        
        # Filter by preference
        preference_lower = preference.lower()
        preferred_models = [
            m for m in models 
            if preference_lower in m.name.lower()
        ]
        
        if preferred_models:
            best_model = preferred_models[0].name
            logger.info(f"Selected {best_model} (preference: {preference})")
            return best_model
        
        # Fallback to first available
        fallback = models[0].name
        logger.warning(f"No {preference} model found, using fallback: {fallback}")
        return fallback
    
    def validate_model(self, model_name: str, provider: str = 'gemini') -> bool:
        """
        Validate that a model name is currently available.
        
        Args:
            model_name: Model identifier to validate
            provider: AI provider ('gemini' or 'claude')
            
        Returns:
            True if model is available, False otherwise
        """
        if provider == 'gemini':
            models = self.list_gemini_models()
            return any(m.name == model_name for m in models)
        
        # Claude validation would go here
        return False
    
    def get_fallback_chain(self, provider: str = 'gemini') -> List[str]:
        """
        Get prioritized list of model names to try in order.
        
        Args:
            provider: AI provider
            
        Returns:
            List of model names in priority order
        """
        if provider == 'gemini':
            models = self.list_gemini_models()
            
            # Priority: flash > pro > others
            flash_models = [m.name for m in models if 'flash' in m.name.lower()]
            pro_models = [m.name for m in models if 'pro' in m.name.lower()]
            other_models = [m.name for m in models if m.name not in flash_models + pro_models]
            
            return flash_models + pro_models + other_models
        
        return []


# Module-level test
if __name__ == "__main__":
    """Test model discovery functionality."""
    logger.info("=" * 70)
    logger.info("MODEL DISCOVERY TEST")
    logger.info("=" * 70)
    
    try:
        discovery = ModelDiscovery()
        
        # List all models
        logger.info("\n📋 Listing all available Gemini models:")
        models = discovery.list_gemini_models()
        
        for i, model in enumerate(models, 1):
            logger.info(f"\n{i}. {model.name}")
            logger.info(f"   Display: {model.display_name}")
            logger.info(f"   Methods: {model.supported_methods}")
        
        # Get best flash model
        logger.info("\n🎯 Finding best Flash model:")
        best_flash = discovery.get_best_gemini_model('flash')
        logger.info(f"   Recommended: {best_flash}")
        
        # Validate a model
        logger.info("\n✅ Validating model availability:")
        is_valid = discovery.validate_model(best_flash, 'gemini')
        logger.info(f"   {best_flash} is valid: {is_valid}")
        
        # Get fallback chain
        logger.info("\n🔄 Fallback chain (priority order):")
        fallbacks = discovery.get_fallback_chain('gemini')
        for i, model in enumerate(fallbacks[:5], 1):  # Show top 5
            logger.info(f"   {i}. {model}")
        
        logger.info("\n" + "=" * 70)
        logger.info("✅ Model discovery test complete!")
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}", exc_info=True)