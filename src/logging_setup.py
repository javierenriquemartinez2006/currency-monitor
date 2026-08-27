# Logging Configuration File

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from src.config import Config

def setup_logging():
    """Configure logging to both console and file"""
    
    # Create logs directory
    Path('logs').mkdir(exist_ok=True)
    
    # Root logger
    root_logger = logging.getLogger() # What is the root logger? Does it accompasses all other loggers?
    root_logger.setLevel(logging.DEBUG)
    
    # Clean existing handlers (prevent duplicates)
    root_logger.handlers.clear()
    
    # Console handler (User-facing; clear output)
    console_handler = logging.StreamHandler() # What is a stream handler? What is its function, and how does it work?
    console_handler.setLevel(getattr(logging, Config.CONSOLE_LEVEL)) # What does getattr does? I dont understand this line
    console_handler.setFormatter(logging.Formatter('%(message)s')) # What is formatter objs used for?
    
    # File handler
    file_handler = RotatingFileHandler(
        Config.LOG_FILE,
        maxBytes=10_000_000, # Why this format? What type of data is this?
        backupCount=5 # Purpose?
    )
    file_handler.setLevel(getattr(logging, Config.LOG_LEVEL)) # Haven't been set when initialized?
    file_handler.setFormatter(logging.Formatter('%(asctime)s:%(name)s:%(levelname)s| %(message)s')) # Is there another time format more clean (without microseconds)?
    
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    
    return root_logger
