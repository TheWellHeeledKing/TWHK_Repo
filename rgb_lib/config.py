from openrgb.utils import RGBColor

PATH = "C:\\Users\\Mike\\Software\\OpenRGB Windows 64-bit\\"
EXE = "OpenRGB.exe"
SERVER_ARG = "--server"
LOGLEVEL_ARG = "--loglevel"
LOGLEVEL = "6"

STARTUP_WAIT_SECS = 8
TERMINATE_WAIT_SECS = 1

HOST: str = "localhost"
PORT: int = 6742
SOCKET_TIMEOUT_SECS: int = 10

DIRECT = "Direct"

H_MIN = 0.000
H_MAX = 0.933

ROUND_DIGITS = "0.001"

RGB_MIN = 50
RGB_MAX = 255

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
