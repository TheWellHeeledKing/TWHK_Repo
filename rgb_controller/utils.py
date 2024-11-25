from config import (MIN_ARGS,
                    MAX_ARGS,
                    MODE_ARG,
                    COLOR_ARG,
                    LEVEL_ARG,
                    ARG_MODES,
                    SINGLE_ARG_MODES,
                    MULTI_ARG_MODES)

from rgb_lib.config import COLOR_MAP, RGB_MIN, RGB_MAX

import logging

# Create a logger for this module
logger = logging.getLogger(__name__)  # __name__ gives "package.module"

###############################################################################


def validate_args(args):

    try:

        if len(args) < MIN_ARGS:
            raise ValueError("No arguments provided!")

        if len(args) > MAX_ARGS:
            raise ValueError("Too many arguments!")

        if len(args) == 1:

            if (args[MODE_ARG] not in ARG_MODES[SINGLE_ARG_MODES]):
                raise ValueError("Invalid single argument! "
                                 f"{args[MODE_ARG]} not in "
                                 f"{ARG_MODES[SINGLE_ARG_MODES]}")

        else:
            if len(args) > 1:
                if args[MODE_ARG] not in ARG_MODES[MULTI_ARG_MODES]:
                    raise ValueError("Invalid first Argument! "
                                     f"{args[MODE_ARG]} not in "
                                     f"{ARG_MODES[MULTI_ARG_MODES]}")

            if args[COLOR_ARG] not in COLOR_MAP.keys():
                raise ValueError("Invalid Color Argument! "
                                 f"{args[COLOR_ARG]} not in "
                                 f"{COLOR_MAP.keys()}")

            if len(args) > 2:

                if int(args[LEVEL_ARG]) not in range(int(RGB_MIN),
                                                     int(RGB_MAX)+1):
                    raise ValueError(f"Invalid Level Argument "
                                     f"{args[LEVEL_ARG]} Not between "
                                     f"{RGB_MIN} and {RGB_MAX}")

        logger.info(f"Arguments validated: {args}")

    except ValueError as e:
        logger.exception(f"Argument Error: {e}. Exiting")
        raise
