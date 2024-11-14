import config
import colorsys
from openrgb.utils import RGBColor
from decimal import Decimal, ROUND_DOWN
import logging

H_MIN = 0.000
H_MAX = 0.933

ROUND_DIGITS = "0.001"

# Create a logger for this module
logger = logging.getLogger(__name__)

###############################################################################



###############################################################################


def get_RGB_color_spectrum(num_colors):

    logger.debug(f"Get {num_colors} Spectrum colors as RGB colors")

    RGBcolors = []

    for index in range(num_colors):

        if num_colors == 1:
            hue = H_MIN
        else:
            hue_value = Decimal((index * H_MAX) / (num_colors - 1))
            hue = float(hue_value.quantize(Decimal(ROUND_DIGITS),
                                           rounding=ROUND_DOWN))

        rgb_float = colorsys.hsv_to_rgb(hue, 1.0, 1.0)

        # Convert from float (0.0-1.0) to integer (0-255) RGB values
        r = int(rgb_float[0] * 255)
        g = int(rgb_float[1] * 255)
        b = int(rgb_float[2] * 255)

        logger.debug(f"RGBcolors Hue: {hue} Mapped to: r: {r} g: {g} b: {b}")

        RGBcolors.append(RGBColor(r, g, b))

    return RGBcolors

###############################################################################


def get_bespoke_zone_color_scheme(device_name, zone_name, num_zone_leds):

    # Returns an array containg the RGB colors for the zone within device

    logger.debug(f"Get Bespoke Zone Lighting Scheme for "
                 f"{device_name}.{zone_name}")

    zone_color_scheme = []

    if device_name == "ASUS TUF GAMING B650-PLUS":

        if zone_name == "Aura Addressable 1":

            for led_index in range(num_zone_leds):
                zone_color_scheme.append(config.COLOR_MAP.get("Red"))
            return zone_color_scheme

        if zone_name == "Aura Addressable 2":

            for led_index in range(num_zone_leds):
                if led_index <= 3 or led_index >= 9:
                    zone_color_scheme.append(config.COLOR_MAP.get("Red"))
                else:
                    zone_color_scheme.append(config.COLOR_MAP.get("White"))
            return zone_color_scheme

        if zone_name == "Aura Addressable 3":

            for led_index in range(num_zone_leds):
                if led_index <= 6 or (led_index >= 10 and led_index <= 15):
                    zone_color_scheme.append(config.COLOR_MAP.get("Red"))
                else:
                    zone_color_scheme.append(config.COLOR_MAP.get("White"))
            return zone_color_scheme

    if device_name == "G502 HERO Gaming Mouse":

        if zone_name == "Primary Zone":

            for led_index in range(num_zone_leds):
                zone_color_scheme.append(config.COLOR_MAP.get("White"))
            return zone_color_scheme

    if device_name == "Logitech G213":

        for led_index in range(num_zone_leds):
            if led_index == 3:
                zone_color_scheme.append(config.COLOR_MAP.get("White"))
            else:
                zone_color_scheme.append(config.COLOR_MAP.get("Red"))
        return zone_color_scheme

    # All other LEDs default to Red
    for led_index in range(num_zone_leds):
        zone_color_scheme.append(config.COLOR_MAP.get("Red"))

    return zone_color_scheme
