from config import (MIN_ARGS,
                    MAX_ARGS,
                    MODE_ARG,
                    COLOR_ARG,
                    LEVEL_ARG,
                    ARG_MODES,
                    SINGLE_ARG_MODES,
                    MULTI_ARG_MODES,
                    INFO_MODE,
                    SINGLE_MODE,
                    TEST_MODE)

from rgb_lib.config import COLOR_MAP, RGB_MIN, RGB_MAX

from rgb_lib.device_manager import (set_devices_to_single_color,
                                    set_devices_colors_by_mode,
                                    show_devices_info,
                                    test_all_devices)

from common_lib.translator import get_translation

import logging

# Create a logger for this module
logger = logging.getLogger(__name__)  # __name__ gives "package.module"

###############################################################################


def validate_args(args):

    try:

        if len(args) < MIN_ARGS:
            msg: str = get_translation("No arguments provided!")
            logger.exception(msg)
            raise ValueError(msg)

        if len(args) > MAX_ARGS:
            msg: str = get_translation("Too many arguments!")
            logger.exception(msg)
            raise ValueError(msg)

        if len(args) == 1:

            if (args[MODE_ARG] not in ARG_MODES[SINGLE_ARG_MODES]):

                msg1: str = get_translation("Invalid single argument: ")
                msg1 += str(args[MODE_ARG])
                logger.exception(msg1)
                msg2: str = get_translation("Permitted single arguments: ")
                msg2 += str(ARG_MODES[SINGLE_ARG_MODES])
                logger.exception(msg2)

                raise ValueError(msg1)

        else:
            if len(args) > 1:
                if args[MODE_ARG] not in ARG_MODES[MULTI_ARG_MODES]:

                    msg1: str = get_translation("Invalid first argument: ")
                    msg1 += str(args[MODE_ARG])
                    logger.exception(msg1)
                    msg2: str = get_translation("Permitted first arguments: ")
                    msg2 += str(ARG_MODES[MULTI_ARG_MODES])
                    logger.exception(msg2)

                    raise ValueError(msg1)

            if args[COLOR_ARG] not in COLOR_MAP.keys():

                msg1: str = get_translation("Invalid color argument: ")
                msg1 += str(args[COLOR_ARG])
                logger.exception(msg1)
                msg2: str = get_translation("Permitted color arguments: ")
                msg2 += str(COLOR_MAP.keys())
                logger.exception(msg2)

                raise ValueError(msg1)

            if len(args) > 2:

                if int(args[LEVEL_ARG]) not in range(int(RGB_MIN),
                                                     int(RGB_MAX)+1):

                    msg1: str = get_translation("Invalid RGB level argument: ")
                    msg1 += str(args[LEVEL_ARG])
                    logger.exception(msg1)
                    msg2: str = get_translation("Allowed from: ")
                    msg2 += str(RGB_MIN)
                    msg2 += get_translation(" to: ")
                    msg2 += str(RGB_MAX)
                    logger.exception(msg2)

                    raise ValueError(msg1)

        logger.info(get_translation("Arguments validated: ")+str(args))

    except ValueError as e:
        msg: str = get_translation("Argument Error, Exiting due to ") + str(e)
        logger.exception(msg)
        raise ValueError(msg)

###############################################################################


def process(client, args):

    try:

        logger.info(get_translation("Processing mode: ")+args[MODE_ARG])

        if args[MODE_ARG] == INFO_MODE:
            show_devices_info(client.devices)
            # show_i2c_interfaces(client)
            return

        if args[MODE_ARG] == TEST_MODE:
            test_all_devices(client.devices)
            return

        if args[MODE_ARG] == SINGLE_MODE:
            level = args[LEVEL_ARG] if len(args) == MAX_ARGS else None
            set_devices_to_single_color(client.devices,
                                        args[COLOR_ARG],
                                        level)
            return

        set_devices_colors_by_mode(client, args[MODE_ARG])
        return

    except Exception as e:

        logger_msg: str = get_translation("Exit due to process error: ")
        logger.exception(logger_msg + str(e))
