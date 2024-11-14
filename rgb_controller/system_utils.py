import logging
from config import (MIN_ARGS, MAX_ARGS, MODE_ARG, COLOR_ARG, LEVEL_ARG,
                    ARG_MODES,
                    SINGLE_ARG_MODES, MULTI_ARG_MODES,
                    LEVEL_MAX, LEVEL_MIN,
                    COLOR_MAP)

# Create a logger for this module
logger = logging.getLogger(__name__)

###############################################################################





def get_args(input_args):

    args = input_args[1:]  # First arg is always path/filename. Slice off.

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

                if int(args[LEVEL_ARG]) not in range(int(LEVEL_MIN),
                                                     int(LEVEL_MAX)+1):
                    raise ValueError(f"Invalid Level Argument "
                                     f"{args[LEVEL_ARG]} Not between "
                                     f"{LEVEL_MIN} and {LEVEL_MAX}")

        return args

    except ValueError as exception_msg:

        logger.error(f"Exception: {exception_msg}")
        raise
