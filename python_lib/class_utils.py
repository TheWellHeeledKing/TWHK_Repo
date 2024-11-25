import logging

logger = logging.getLogger(__name__)  # __name__ gives "my_package.module1"

###############################################################################


def show_class_interface(obj, name="Object"):

    logger.info(f"{80*'#'}\n{name} Interface:\n{dir(obj)}")

###############################################################################
