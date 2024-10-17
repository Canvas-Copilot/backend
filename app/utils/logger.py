from loguru import logger
import sys

# Configure Loguru to log to stdout and a file
logger.remove()  # Remove default logger

logger.add(sys.stdout, format="{time} {level} {message}", level="INFO")
logger.add(
    "logs/app.log", rotation="1 MB", format="{time} {level} {message}", level="DEBUG"
)
