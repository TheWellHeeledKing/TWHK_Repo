import logging
from openrgb.utils import RGBColor

DEBUG_LEVEL = logging.DEBUG

MAIN = "__main__"

COLOR_MAP = {
    "Black": RGBColor(0, 0, 0),
    "Blue": RGBColor(0, 0, 255),
    "Green": RGBColor(0, 255, 0),
    "Cyan": RGBColor(0, 255, 255),
    "Red": RGBColor(255, 0, 0),
    "Magenta": RGBColor(255, 0, 255),
    "Yellow": RGBColor(255, 255, 0),
    "White": RGBColor(255, 255, 255),

    "Orange": RGBColor(255, 42, 0),
    "Indigo": RGBColor(75, 0, 130),
    "Violet": RGBColor(238, 130, 238),
    "Purple": RGBColor(86, 4, 250)
}

MIN_ARGS = 1
MAX_ARGS = 3

MODE_ARG = 0
COLOR_ARG = 1
LEVEL_ARG = 2

SINGLE_ARG_MODES = 0
MULTI_ARG_MODES = 1

ARG_MODES = [["Clear", "Spectrum", "Info", "Breathing", "Bespoke"], ["Single"]]

COLORS = COLOR_MAP.keys

LEVEL_MIN = 50
LEVEL_MAX = 255

OPEN_RGB_PATH = "C:\\Users\\Mike\\Software\\OpenRGB Windows 64-bit\\"
OPEN_RGB_EXE = "OpenRGB.exe"
OPEN_RGB_SERVER_ARG = "--server"
OPEN_RGB_LOGLEVEL_ARG = "--loglevel"
OPEN_RGB_LOGLEVEL = "6"

OPEN_RGB_STARTUP_WAIT_SECS = 8
OPEN_RGB_TERMINATE_WAIT_SECS = 1

LOCAL_HOST = "localhost"
PORT = 6742

NUMBER_OF_RGB_DEVICES = 3

EXIT_STATUS_ABNORMAL = 1
EXIT_STATUS_NORMAL = 0

CLOSE_SCRIPT_WAIT_SECS = 3
