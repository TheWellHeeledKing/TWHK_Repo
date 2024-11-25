import logging

# Create a logger for this module
logger = logging.getLogger(__name__)  # __name__ gives "package.module"

###############################################################################


def show_class_interface(obj, name="Object"):

    logger.info(f"{80*'#'}\n{name} Interface:\n{dir(obj)}")

###############################################################################
