import time
import logging
import sys

from common_lib.config import MAIN, CLOSE_SCRIPT_WAIT_SECS
from common_lib.translator import translate

from rgb_lib.open_RGB_utils import (start_openRGB_server,
                                    connect_openRGB_client,
                                    disconnect_openRGB_client,
                                    terminate_openRGB_server)

from config import RGB_DEVICE_COUNT
from utils import (validate_args, process)

#  from rgb_lib.interfaces import show_i2c_interfaces  # Not yet used

# Create a logger for this module
logger = logging.getLogger(__name__)  # __name__ gives "package.module"

###############################################################################


if __name__ == MAIN:

    # Log the script start with script name
    logger.info(f"{translate("START_MSG_ID")}: {sys.argv[0:]}")
    logger.debug(translate("DEBUG_MODE_MSG_ID"))

    try:

        args = sys.argv[1:]  # First arg always path/filename. Slice off.
        validate_args(args)
        server_process = start_openRGB_server()
        try:
            client = connect_openRGB_client(RGB_DEVICE_COUNT)
            process(client, args)
            disconnect_openRGB_client(client)

        except Exception as e:
            logger.exception(str(e))

        finally:
            terminate_openRGB_server(server_process)

    except Exception as e:
        logger.exception(str(e))

    finally:
        logger_msg: str = translate("SCRIPT_CLOSE_MSG_ID")
        logger.info(f"{logger_msg} {CLOSE_SCRIPT_WAIT_SECS}")
        time.sleep(CLOSE_SCRIPT_WAIT_SECS)  # Wait before closing
