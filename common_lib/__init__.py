import logging
from polib import MOFile

from .config import DEBUG_LEVEL, LOG_FORMAT, MO_PATH_AND_FILENAME
from .translator import load_translation_file

# Initialize logging with the constants from config.py
logging.basicConfig(level=DEBUG_LEVEL,
                    format=LOG_FORMAT)

# You can add any initialization logic for the package here if needed

TRANSLATION_FILE: MOFile = load_translation_file(MO_PATH_AND_FILENAME)
