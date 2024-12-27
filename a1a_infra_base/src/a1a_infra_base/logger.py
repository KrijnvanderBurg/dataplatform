"""
Logger module to configure and provide a logger instance with both console and rotating file handlers.

This module provides a function `setup_logger` to configure a logger with a specified name, log file, and log level.
The logger will output log messages to both the console and a rotating log file.

Example usage:
    from logger import setup_logger

    logger = setup_logger("my_logger", "my_log_file.log", logging.DEBUG)
    logger.info("This is an info message")
    logger.error("This is an error message")
"""

import logging
from logging.handlers import RotatingFileHandler
from sys import stdout

# Log format
FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")


def setup_logger(name: str, filename: str = "ingestion.log", level: int = logging.INFO) -> logging.Logger:
    """
    Configure the logger settings. Includes a console stream handler and a rotating file handler.

    Args:
        name (str): Logger name.
        filename (str): Name of the log file, defaults to "ingestion.log" (optional).
        level (int): Logging level (default is INFO).

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)

    # Add console stream handler
    console_handler = logging.StreamHandler(stream=stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(FORMATTER)
    logger.addHandler(console_handler)

    # Add rotating log handler
    rotating_handler = RotatingFileHandler(
        filename=filename,
        maxBytes=5 * 1024 * 1024,  # 5MB
        backupCount=10,  # Max 10 log files before replacing the oldest
    )
    rotating_handler.setLevel(level)
    rotating_handler.setFormatter(FORMATTER)
    logger.addHandler(rotating_handler)

    return logger
