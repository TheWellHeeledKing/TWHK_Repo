import logging
from config import DIRECT
from python_utils.class_utils import show_class_interface

# Create a logger for this module
logger = logging.getLogger(__name__)

###############################################################################


def set_device_mode(device, mode=None):
    if mode is None:
        mode = DIRECT
    logger.info(f"Setting device {device.name} to mode {mode}")
    device.set_mode(mode)

###############################################################################


def show_device_info(device):

    try:

        for mode_index, mode in enumerate(device.modes):

            logger.info(f"{mode_index} Mode: {mode.name}")

        zones = device.zones
        for zone_index, zone in enumerate(zones):

            logger.info(f"    {zone_index} Zone {zone.name}")

            leds = zone.leds
            for led_index, led in enumerate(leds):

                logger.info(f"        {led_index} Led {led.name}")

    except Exception as e:
        logger.exception(f"Error occurred while showing device info: {e}")
        raise

###############################################################################


def print_attributes(obj, name="Object"):

    logger.info(f"\n{'#'*6} {name} Attributes:")

    for attribute, value in vars(obj).items():
        logger.info(f"{' '*6} {attribute}: {value}")


###############################################################################


def show_device_interface(device):

    show_class_interface(device, "Device")
    show_class_interface(device.zones[0], "Zone")
    show_class_interface(device.zones[0].leds[0], "Led")

###############################################################################


def set_single_color(device, RGBcolor):
    set_device_mode(device)
    logger.debug(f"Setting single color for {device.name}")
    for zone in device.zones:
        logger.debug(f"                         {zone.name}")
        for led in zone.leds:
            logger.debug(f"                         {led.name}")
            led.set_color(RGBcolor)

###############################################################################


def set_device_to_bespoke_lighting(device, device_led_color_scheme):

    try:
        logger.debug(f"Setting bespoke lighting for device {device.name}")

        for zone in device.zones:

            logger.debug(f"                                    {zone.name}")

            zone_led_color_scheme = device_led_color_scheme.get(zone.name)

            if len(zone.leds) != len(zone_led_color_scheme):
                raise IndexError("No. of LEDs in zone does not match no. "
                                 "of entries in the zone color scheme!")

            for led_index, led in enumerate(zone.leds):
                logger.debug(f"Setting color for LED # {led_index} , "
                             f"{led.name}")
                color = zone_led_color_scheme[led_index]
                led.set_color(color)

    except IndexError as e:
        logger.exception("Error", e)

###############################################################################


def set_spectrum_colors(device, zone_leds_color_map):

    set_device_mode(device, DIRECT)

    for zone in device.zones:

        try:
            RGBcolors = zone_leds_color_map[zone.name]

        except KeyError:
            logger.exception(f"Zone {zone.name} not found in RGBColors map. "
                             "Cannot set LEDs. Aborting")

        try:
            RGBcolor_count = len(RGBcolors)
            led_count = len(zone.leds)

            assert RGBcolor_count == led_count

        except AssertionError:
            logger.exception(f"Number of LEDs ({led_count}) "
                             f"in zone {zone.name} does not match "
                             f"number of RGBColors ({RGBcolor_count}) "
                             "in RGBColors map. Cannot set LEDs. Aborting")

        logger.info(f"Setting Device {device.name}, "
                    f"Zone {zone.name} to spectrum.")

        for index in range(led_count):

            logger.debug(f"{zone.leds[index]} set to RGBcolor : "
                         f"{RGBcolors[index]}")
            zone.leds[index].set_color(RGBcolors[index])
            index = index + 1

###############################################################################


def set_mode(device, mode):

    allowed_modes = ["Direct", "Off", "Breathing"]

    if mode in allowed_modes:
        logger.debug(f"Setting Device {device.name} to mode {mode}")
        device.set_mode(mode)
    else:
        logger.exception(f"Invalid set_mode : {mode} on {device.name}!")
