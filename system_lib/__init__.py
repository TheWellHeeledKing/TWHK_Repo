import logging
from common_lib.config import DEBUG_LEVEL, LOG_FORMAT

# Initialize logging with the common constants
logging.basicConfig(level=DEBUG_LEVEL, format=LOG_FORMAT)

# You can add any initialization logic for the package here if needed
