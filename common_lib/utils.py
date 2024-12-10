from time import sleep
from logging import (getLogger, Logger)
from common_lib.translator import translate

# Create a logger for this module
logger: Logger = getLogger(__name__)  # __name__ gives "package.module"

###############################################################################


def start_script(path_and_filename: str = ""):

    # Log the script start with script name
    logger.info(f"{translate("START_MSG_ID")}: {path_and_filename}")
    logger.debug(translate("DEBUG_MODE_MSG_ID"))

###############################################################################


def close_script(wait_secs: int = 0):

    # Log the script end
    logger_msg: str = translate("SCRIPT_CLOSE_MSG_ID")
    logger.info(f"{logger_msg} {wait_secs}")
    sleep(wait_secs)  # Wait before closing
