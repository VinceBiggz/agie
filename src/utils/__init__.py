"""
Utility modules for AGIE.

This package contains reusable utilities for model discovery,
configuration management, and other cross-cutting concerns.

@author: Vincent Wachira
@date: 2025-02-14
@version: 0.1.0
@license: MIT
"""

from .model_discovery import ModelDiscovery, ModelInfo

__all__ = [
    'ModelDiscovery',
    'ModelInfo',
]

__version__ = '0.1.0'