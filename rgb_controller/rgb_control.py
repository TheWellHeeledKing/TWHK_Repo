import time
import logging
import sys

from common_lib.config import MAIN, CLOSE_SCRIPT_WAIT_SECS
from common_lib.translator import translate
from common_lib.utils import start_script, close_script

from rgb_lib.open_RGB_utils import (is_openrgb_server_running,
                                    start_openRGB_server,
                                    is_openrgb_server_available,
                                    connect_openRGB_client,
                                    disconnect_openRGB_client)

from system_lib.utils import (get_proc_dict)

from config import RGB_DEVICE_COUNT
from utils import (validate_args, set_rgb_lighting)

#  from rgb_lib.interfaces import show_i2c_interfaces  # Not yet used

# Create a logger for this module
logger = logging.getLogger(__name__)  # __name__ gives "package.module"

###############################################################################


if __name__ == MAIN:

    start_script(sys.argv[0:])

    try:

        if (
            validate_args(sys.argv[1:]) and
            is_openrgb_server_running(get_proc_dict()) and
            is_openrgb_server_available()
        ):

            client = connect_openRGB_client(RGB_DEVICE_COUNT)
            set_rgb_lighting(client, sys.argv[1:])
            disconnect_openRGB_client(client)

        else:

            logger.error(f"{translate("TEXT_RGBControlFailed")}")

        close_script(CLOSE_SCRIPT_WAIT_SECS)

    except Exception as e:
        logger.exception(str(e))
