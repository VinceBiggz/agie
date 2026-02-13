"""
Centralized logging configuration for AGIE.

This module provides a consistent logging interface across all AGIE components.
All modules should import logger from this file to ensure uniform logging behavior.

@author: Vincent Wachira
@date: 2025-02-14
@version: 0.1.0
@license: MIT
"""

import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logger(
    name: str = "agie",
    level: str = "INFO",
    log_file: Optional[Path] = None
) -> logging.Logger:
    """
    Configure and return a logger instance with console and optional file output.
    
    Args:
        name: Logger name (typically module name or 'agie')
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional path to log file. If None, only console logging.
        
    Returns:
        Configured logger instance
        
    Example:
        >>> from src.logger import logger
        >>> logger.info("Processing started")
        2025-02-14 10:30:00 - agie - INFO - Processing started
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Prevent duplicate handlers if logger already configured
    if logger.handlers:
        return logger
    
    # Console handler - outputs to stdout
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    
    # Formatter with timestamp, module name, level, and message
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Optional file handler
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.info(f"File logging enabled: {log_file}")
    
    return logger


# Global logger instance used throughout AGIE
logger = setup_logger()


# Module-level test
if __name__ == "__main__":
    """Test logger configuration."""
    logger.debug("This is a DEBUG message")
    logger.info("This is an INFO message")
    logger.warning("This is a WARNING message")
    logger.error("This is an ERROR message")
    logger.critical("This is a CRITICAL message")

