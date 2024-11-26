import time
import logging
import sys

from common_lib.config import MAIN, CLOSE_SCRIPT_WAIT_SECS
from common_lib.translator import get_translation

from rgb_lib.open_RGB_utils import (start_openRGB_server,
                                    connect_openRGB_client,
                                    disconnect_openRGB_client,
                                    terminate_openRGB_server)

from config import (RGB_DEVICE_COUNT)

from utils import (validate_args, process)

#  from rgb_lib.interfaces import show_i2c_interfaces  # Not yet used

# Create a logger for this module
logger = logging.getLogger(__name__)  # __name__ gives "package.module"

###############################################################################


if __name__ == MAIN:

    # Log the script name and arguments

    logger.info(get_translation("Starting: ")+str(sys.argv[0:]))
    logger.debug(get_translation("Entering Debug Mode"))

    try:

        try:

            args = sys.argv[1:]  # First arg always path/filename. Slice off.
            validate_args(args)
            server_process = start_openRGB_server()

        except Exception:
            logger.error(get_translation("Startup Error. Exiting"))
            raise

        try:

            client = connect_openRGB_client(RGB_DEVICE_COUNT)
            process(client, args)
            disconnect_openRGB_client(client)

        except Exception as e:

            logger_msg: str = get_translation("Exit due to processing error: ")
            logger.exception(logger_msg + str(e))

        finally:
            terminate_openRGB_server(server_process)

    except Exception as e:

        logger.exception(get_translation("Exit due to exception: ") + str(e))

    finally:

        logger_msg: str = get_translation("Script finishes in (secs): ")
        logger.info(logger_msg + str(CLOSE_SCRIPT_WAIT_SECS))

        time.sleep(CLOSE_SCRIPT_WAIT_SECS)  # Wait before closing
