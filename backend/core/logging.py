"""
Logging configuration for the microscope control system
"""
import logging
from logging.handlers import RotatingFileHandler
import sys
import os


def setup_logging():
    """Configure application logging"""

    # Create logs directory
    os.makedirs("logs", exist_ok=True)

    # Create logger
    logger = logging.getLogger("microscope")
    logger.setLevel(logging.DEBUG)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)

    # File handler (rotating)
    file_handler = RotatingFileHandler(
        "logs/microscope.log",
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    )
    file_handler.setFormatter(file_formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


logger = setup_logging()
