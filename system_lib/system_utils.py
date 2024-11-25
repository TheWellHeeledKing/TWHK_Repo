import logging

# Create a logger for this module
logger = logging.getLogger(__name__)  # __name__ gives "package.module"

###############################################################################


def get_args(input_args, min_args, max_args):

    args = input_args[1:]  # First arg is always path/filename. Slice off.

    try:

        if len(args) < min_args:
            raise ValueError("No arguments provided!")
        if len(args) > max_args:
            raise ValueError("Too many arguments!")

        logger.info(f"Script arguments fetched: {args}")
        return args

    except ValueError as exception_msg:

        logger.error(f"Exception: {exception_msg}")
        raise
