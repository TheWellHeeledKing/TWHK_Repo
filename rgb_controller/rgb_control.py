import time
import logging
import sys

from common_lib.config import MAIN, CLOSE_SCRIPT_WAIT_SECS

from rgb_lib.device_manager import (set_devices_to_single_color,
                                    set_devices_colors_by_mode,
                                    show_devices_info,
                                    test_all_devices)
from rgb_lib.open_RGB_utils import (start_openRGB_server,
                                    connect_openRGB_client,
                                    disconnect_openRGB_client,
                                    terminate_openRGB_server)

from config import (MAX_ARGS, MODE_ARG, COLOR_ARG, LEVEL_ARG, RGB_DEVICE_COUNT)

from utils import validate_args

#  from rgb_lib.interfaces import show_i2c_interfaces  # Not yet used

# Create a logger for this module
logger = logging.getLogger(__name__)  # __name__ gives "package.module"

###############################################################################


if __name__ == MAIN:

    # Log the script name and arguments
    logger.info(f"Starting: {' '.join(sys.argv[0:])}")
    logger.debug(f"{80*'#'}\nEntering Debug Mode\n{80*'#'}")

    try:

        try:

            args = sys.argv[1:]  # First arg always path/filename. Slice off.
            validate_args(args)
            server_process = start_openRGB_server()

        except Exception:
            logger.error("Startup Error. Exiting")
            raise

        try:

            client = connect_openRGB_client(RGB_DEVICE_COUNT)

            if args[MODE_ARG] == "Info":
                show_devices_info(client.devices)
                # show_i2c_interfaces(client)
            elif args[MODE_ARG] == "Test":
                test_all_devices(client.devices)
            elif args[MODE_ARG] == "Single":
                level = args[LEVEL_ARG] if len(args) == MAX_ARGS else None
                set_devices_to_single_color(client.devices,
                                            args[COLOR_ARG],
                                            level)
            else:
                set_devices_colors_by_mode(client, args[MODE_ARG])

            disconnect_openRGB_client(client)

        except Exception as e:
            logger.exception(f"Processing Error: {e}. Exiting")

        finally:
            terminate_openRGB_server(server_process)

    except Exception as e:
        logger.exception(f"{e}: Terminating Script")

    finally:

        logger.debug(f"Script terminates in {CLOSE_SCRIPT_WAIT_SECS} "
                     "seconds....")

        time.sleep(CLOSE_SCRIPT_WAIT_SECS)  # Wait before closing
