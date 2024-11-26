import polib
import logging
from .config import LANGUAGE
import common_lib

# Create a logger for this module
logger = logging.getLogger(__name__)  # __name__ gives "package.module"

###############################################################################


def load_translation_file(mo_path_and_filename: str) -> polib.MOFile:
    """
    Loads the .mo file
    """
    logger.debug(f"Attempting to load MO file: {mo_path_and_filename}")
    try:
        # Load the .mo file
        translation_file: polib.MOFile = polib.mofile(mo_path_and_filename)
        logger.info(f"{LANGUAGE} language file loaded successfully: "
                    f"{mo_path_and_filename}")
        return translation_file

    except Exception as e:
        logger.error(f"Error loading MO file {mo_path_and_filename}: {e}")
        raise

###############################################################################


def get_translation(msgid: str) -> str:

    try:

        # Try to find the translation for the msgid
        entry = common_lib.TRANSLATION_FILE.find(msgid)
        if entry:
            logger.debug(f"Translation found for '{msgid}': {entry.msgstr}")
            return entry.msgstr  # Return the translated string
        else:
            logger.warning(f"Translation not found for: {msgid}")
            return msgid  # Return original msgid if no translation is found
    except Exception as e:
        logger.error(f"Error getting translation for msgid {msgid}: {e}")
        return msgid  # Return original msgid in case of an error

###############################################################################
