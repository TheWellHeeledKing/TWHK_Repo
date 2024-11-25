import logging
from .config import DEBUG_LEVEL, LOG_FORMAT

# Initialize logging with the constants from config.py
logging.basicConfig(level=DEBUG_LEVEL,
                    format=LOG_FORMAT)

# You can add any initialization logic for the package here if needed
