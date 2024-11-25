from .config import (RGB_MAX, H_MIN, H_MAX, ROUND_DIGITS)
import colorsys
from openrgb.utils import RGBColor
from decimal import Decimal, ROUND_DOWN
from .config import COLOR_MAP
import logging

# Create a logger for this module
logger = logging.getLogger(__name__)  # __name__ gives "package.module"

##############################################################################


def set_color_level(rgb, level):

    try:

        rgb_levelled = rgb

        rgb_levelled.red = level if rgb.red == RGB_MAX else rgb.red
        rgb_levelled.green = level if rgb.green == RGB_MAX else rgb.green
        rgb_levelled.blue = level if rgb.blue == RGB_MAX else rgb.blue

        return rgb_levelled

    except Exception as e:

        logger.error(f"Error occurred setting color level to {level}: {e}")
        raise

###############################################################################


def get_spectrum_colors(device):

    try:

        zone_leds_color_map = {}

        for zone in device.zones:

            led_count = len(zone.leds)
            color_count = led_count

            if (device.name == "ASUS TUF GAMING B650-PLUS" and
                    zone.name == "Aura Addressable 1"):

                logger.debug(f"Zone {zone.name}, Arctic Liquid-Freezer III,"
                             "has {led_count} addressable LEDs. "
                             "1st 12 : CPU Fan and Front Radiator Fan, "
                             "2nd 12 : Back Radiator Fan")

                color_count = len(zone.leds)//2
                logger.debug(f"Get the first {color_count} colours.")
                spectrum_colors = get_RGB_color_spectrum(color_count)
                logger.debug(f"Repeat colours for second {color_count} "
                             "colours.")

                for color_index in range(color_count):
                    spectrum_colors.append(spectrum_colors[color_index])
                    logger.debug(f"RGBcolors[{12+color_index}]: Mapped to "
                                 f"{spectrum_colors[12+color_index]}")

            else:
                logger.debug(f"Zone {zone.name} has {led_count} "
                             "addressable LEDs")
                color_count = len(zone.leds)
                spectrum_colors = get_RGB_color_spectrum(color_count)

            zone_leds_color_map[zone.name] = spectrum_colors

        return (zone_leds_color_map)

    except Exception as e:

        logger.error(f"Error occurred while getting spectrum colors: {e}")
        raise

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
                zone_color_scheme.append(COLOR_MAP.get("Red"))
            return zone_color_scheme

        if zone_name == "Aura Addressable 2":

            for led_index in range(num_zone_leds):
                if led_index <= 3 or led_index >= 9:
                    zone_color_scheme.append(COLOR_MAP.get("Red"))
                else:
                    zone_color_scheme.append(COLOR_MAP.get("White"))
            return zone_color_scheme

        if zone_name == "Aura Addressable 3":

            for led_index in range(num_zone_leds):
                if led_index <= 6 or (led_index >= 10 and led_index <= 15):
                    zone_color_scheme.append(COLOR_MAP.get("Red"))
                else:
                    zone_color_scheme.append(COLOR_MAP.get("White"))
            return zone_color_scheme

    if device_name == "G502 HERO Gaming Mouse":

        if zone_name == "Primary Zone":

            for led_index in range(num_zone_leds):
                zone_color_scheme.append(COLOR_MAP.get("White"))
            return zone_color_scheme

    if device_name == "Logitech G213":

        for led_index in range(num_zone_leds):
            if led_index == 3:
                zone_color_scheme.append(COLOR_MAP.get("White"))
            else:
                zone_color_scheme.append(COLOR_MAP.get("Red"))
        return zone_color_scheme

    # All other LEDs default to Red
    for led_index in range(num_zone_leds):
        zone_color_scheme.append(COLOR_MAP.get("Red"))

    return zone_color_scheme
