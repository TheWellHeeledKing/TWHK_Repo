import logging
from .config import DIRECT
from common_lib.class_utils import show_class_interface
from rgb_lib.colors import (get_spectrum_colors, set_color_level)
from rgb_lib.color_utils import (get_bespoke_zone_color_scheme)
from .config import COLOR_MAP

# Create a logger for this module
logger = logging.getLogger(__name__)  # __name__ gives "package.module"

##############################################################################


def set_devices_to_single_color(devices, color, level=None):

    try:

        if level is not None:
            rgb = set_color_level(COLOR_MAP.get(color), int(level))
        else:
            rgb = COLOR_MAP.get(color)

        logger.info(f"Setting every device to {color}, level {level}")

        for device in devices:
            logger.debug(f"Setting {color} on {device.name}")

            set_single_color(device, rgb)

    except Exception as e:

        logger.error(f"Error occurred while setting devices to {color}: {e}")
        raise

###############################################################################


def set_devices_to_spectrum(devices):

    try:

        logger.info("Setting each device to a spectrum "
                    "depending on the number of LEDs")

        for device in devices:

            logger.debug(f"Setting spectrum on {device.name} "
                         f"which has {len(device.zones)} zones "
                         f"and {len(device.leds)} LEDs in total")

            zone_leds_color_map = get_spectrum_colors(device)
            set_spectrum_colors(device, zone_leds_color_map)

    except Exception as e:

        logger.error(f"Error occurred while setting devices to spectrum: {e}")
        raise


###############################################################################


def set_devices_mode(devices, mode):

    try:

        logger.info(f"Setting each device to mode: {mode}")

        for device in devices:
            logger.debug(f"Setting mode on {device.name} to {mode}")
            device.set_mode(mode)

    except Exception as e:

        logger.error(f"Error occurred while trying to set devices modes: {e}")
        raise

###############################################################################


def set_devices_to_bespoke_lighting(devices):

    try:

        logger.info("Setting devices to bespoke lighting")

        for device in devices:

            logger.debug(f"Setting {device.name} to bespoke lighting")

            device_lighting_scheme = {}
            set_device_mode(device)
            zones = device.zones

            for zone in zones:

                logger.debug(f"Getting {zone.name} lighting scheme")

                zone_lighting_scheme = get_bespoke_zone_color_scheme(
                    device.name,
                    zone.name,
                    len(zone.leds))

                device_lighting_scheme[zone.name] = zone_lighting_scheme

            set_device_to_bespoke_lighting(device, device_lighting_scheme)

    except Exception as e:

        logger.error(f"Error occurred trying to set bespoke lighting: {e}")
        raise

###############################################################################


def set_devices_colors_by_mode(client, mode):

    try:

        if mode == "Clear":
            # Turn off all LEDs
            client.clear()
        elif mode == "Spectrum":
            set_devices_to_spectrum(client.devices)
        elif mode == "Breathing":
            set_devices_mode(client.devices, mode)
        elif mode == "Bespoke":
            set_devices_to_bespoke_lighting(client.devices)

    except Exception as e:
        logger.error(f"Error occurred while trying to set the colors: {e}")
        raise

###############################################################################


def show_devices_info(devices):

    try:

        for device_index, device in enumerate(devices):

            if device_index == 0:
                show_device_interface(device)

            logger.info(f"\nDevice {device_index} : {device.name}")

            print_attributes(device, "Device")

            # Zone details
            for i, zone in enumerate(device.zones):
                print_attributes(zone, f"Zone {i}")

            # LED details
            for i, led in enumerate(device.leds):
                print_attributes(led, f"LED {i}")

            # show_device_info(device)

    except Exception as e:
        logger.error(f"{e}")
        raise

###############################################################################


def test_all_devices(devices):

    try:

        show_devices_info(devices)

    except Exception as e:
        logger.error(f"{e}")

###############################################################################


def set_device_mode(device, mode=None):
    if mode is None:
        mode = DIRECT
    logger.debug(f"Setting device {device.name} to mode {mode}")
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

        logger.debug(f"Setting Device {device.name}, "
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
