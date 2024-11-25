import logging
from .class_utils import show_class_interface as util_show_class_interface

__all__ = [util_show_class_interface]

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s -'
                           '%(levelname)s - %(message)s')
