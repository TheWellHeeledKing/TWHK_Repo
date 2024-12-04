
from common_lib.translator import translate

from rgb_lib.config import COLOR_MAP, RGB_MIN, RGB_MAX
from rgb_lib.device_manager import (set_devices_to_single_color,
                                    set_devices_colors_by_mode,
                                    show_devices_info,
                                    test_all_devices)

from config import (MIN_ARGS, MAX_ARGS,
                    MODE_ARG, COLOR_ARG, LEVEL_ARG,
                    ARG_MODES,
                    SINGLE_ARG_MODES, MULTI_ARG_MODES,
                    INFO_MODE, SINGLE_MODE, TEST_MODE)

# Create a logger for this module
import logging
logger = logging.getLogger(__name__)  # __name__ gives "package.module"

###############################################################################


def raiseException(msg: str, exception_type: Exception):

    logger.exception(msg)
    raise exception_type(msg, ValueError)

###############################################################################


def validate_args(args):

    if len(args) < MIN_ARGS:
        raiseException(translate("NO_ARGS_MSG_ID"), ValueError)

    if len(args) > MAX_ARGS:
        raiseException(translate("TOO_MANY_ARGS_MSG_ID"), ValueError)

    if len(args) == 1 and (args[MODE_ARG] not in ARG_MODES[SINGLE_ARG_MODES]):
        raiseException(f"{translate("INVALID_SINGLE_ARG_MSG_ID")}: "
                       f"'{args[MODE_ARG]}'. "
                       f"{translate("PERMITTED_MSG_ID")}: "
                       f"{ARG_MODES[SINGLE_ARG_MODES]}", ValueError)

    if len(args) == 2:
        if args[MODE_ARG] not in ARG_MODES[MULTI_ARG_MODES]:
            raiseException(f"{translate("INVALID_FIRST_ARG_MSG_ID")}: "
                           f"{args[MODE_ARG]}. "
                           f"{translate("PERMITTED_MSG_ID")}: "
                           f"{ARG_MODES[MULTI_ARG_MODES]}", ValueError)

        if args[COLOR_ARG] not in COLOR_MAP.keys():
            raiseException(f"{translate("INVALID_COLOR_ARG_MSG_ID")}: "
                           f"'{args[COLOR_ARG]}'. "
                           f"{translate("PERMITTED_MSG_ID")}: "
                           f"{str(list(COLOR_MAP.keys()))}", ValueError)

    if len(args) > 2:
        if int(args[LEVEL_ARG]) not in range((RGB_MIN), (RGB_MAX)+1):
            raiseException(f"{translate("INVALID_RGB_LEVEL_MSG_ID")}: "
                           f"{args[LEVEL_ARG]}. "
                           f"{translate("ALLOWED_FROM_MSG_ID")}: {RGB_MIN} "
                           f"{translate("TO_MSG_ID")}: {RGB_MAX}", ValueError)

    logger.info(f"{translate("ARGS_VALIDATED_MSG_ID")}: {(args)}")

###############################################################################


def process(client, args):

    logger.info(f"{translate("INFO_MSG_PROCESSING_MODE")}: {args[MODE_ARG]}")

    if args[MODE_ARG] == INFO_MODE:
        show_devices_info(client.devices)
        # show_i2c_interfaces(client)
        return

    if args[MODE_ARG] == TEST_MODE:
        test_all_devices(client.devices)
        return

    if args[MODE_ARG] == SINGLE_MODE:
        level = args[LEVEL_ARG] if len(args) == MAX_ARGS else None
        set_devices_to_single_color(client.devices, args[COLOR_ARG], level)
        return

    set_devices_colors_by_mode(client, args[MODE_ARG])
    return
