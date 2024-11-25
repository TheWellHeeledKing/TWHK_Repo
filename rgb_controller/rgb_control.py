import time
import logging
import config

from rgb_lib.device_manager import (
    set_devices_to_single_color,
    set_devices_colors_by_mode,
    show_devices_info,
    test_all_devices
)

from rgb_lib.interfaces import show_i2c_interfaces

import sys
from config import (DEBUG_LEVEL,
                    MAX_ARGS,
                    MODE_ARG,
                    COLOR_ARG,
                    LEVEL_ARG)
from system_lib.system_utils import get_args
from rgb_lib.open_RGB_utils import (
    start_openRGB_server,
    connect_openRGB_client,
    disconnect_openRGB_client,
    terminate_openRGB_server)

###############################################################################


if __name__ == config.MAIN:

    logging.basicConfig(level=DEBUG_LEVEL)
    logger = logging.getLogger(__name__)

    # Log the script name and arguments
    logger.info(f"Starting: {' '.join(sys.argv[0:])}")
    logger.debug("Debug Mode")

    try:

        try:

            args = get_args(sys.argv)
            server_process = start_openRGB_server()

        except Exception:
            logger.error("Startup Error. Exiting")
            raise

        try:

            client = connect_openRGB_client()

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

            if DEBUG_LEVEL == logging.DEBUG:
                show_devices_info(client.devices)

            disconnect_openRGB_client(client)

        except Exception as e:
            logger.exception(f"Processing Error: {e}. Exiting")

        finally:
            terminate_openRGB_server(server_process)

    except Exception as e:
        logger.exception(f"{e}: Terminating Script")

    finally:

        logger.error(f"Script terminates in {config.CLOSE_SCRIPT_WAIT_SECS} "
                     "seconds....")

        time.sleep(config.CLOSE_SCRIPT_WAIT_SECS)  # Wait before closing
