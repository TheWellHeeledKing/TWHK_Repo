import sys
from psutil import Process
from logging import (getLogger, Logger)
from typing import Dict

from common_lib.config import (MAIN, CLOSE_SCRIPT_WAIT_SECS)
from common_lib.utils import start_script, close_script
from common_lib.translator import translate

from system_lib.utils import (get_proc_dict, is_process_running)
from system_lib.config import PROCESS_ID

from rgb_lib.open_RGB_utils import (start_openRGB_server,
                                    is_openrgb_server_running,
                                    is_openrgb_server_available)

# Create a logger for this module
logger: Logger = getLogger(__name__)  # __name__ gives "package.module"

###############################################################################


if __name__ == MAIN:

    try:

        start_script(sys.argv[0:])

        ProcDict: Dict = get_proc_dict()

        if (is_openrgb_server_running(ProcDict)) is False:
            proc: Process = start_openRGB_server()
            if is_process_running(proc.pid) is False:
                raise RuntimeError(f"{translate("TEXT_ServerStartFailed")}")

        if (is_openrgb_server_available()) is False:
            raise RuntimeError(f"{translate("TEXT_ServerNotAvailable")}")

        close_script(CLOSE_SCRIPT_WAIT_SECS)

    except Exception as e:
        logger.exception(str(e))
