import sys
from config import (DEBUG_LEVEL, MAX_ARGS, MODE_ARG,
                    COLOR_ARG, LEVEL_ARG, LEVEL_MAX, COLOR_MAP)
from system_utils import get_args
from open_RGB_utils import (
    start_openRGB_server,
    connect_openRGB_client,
    disconnect_openRGB_client,
    terminate_openRGB_server)
from color_utils import (
    get_bespoke_zone_color_scheme,
    get_RGB_color_spectrum)
from device_manager import (
    set_single_color,
    set_spectrum_colors,
    set_device_to_bespoke_lighting,
    set_device_mode,
    show_device_info)
import requests
import time
import logging
import config

##############################################################################


def set_color_level(rgb, level):

    try:

        rgb_levelled = rgb

        rgb_levelled.red = level if rgb.red == LEVEL_MAX else rgb.red
        rgb_levelled.green = level if rgb.green == LEVEL_MAX else rgb.green
        rgb_levelled.blue = level if rgb.blue == LEVEL_MAX else rgb.blue

        return rgb_levelled

    except Exception as e:

        logger.error(f"Error occurred setting color level to {level}: {e}")
        raise


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


def get_spectrum_colors(device):

    try:

        zone_leds_color_map = {}

        for zone in device.zones:

            led_count = len(zone.leds)
            color_count = led_count

            if (device.name == "ASUS TUF GAMING B650-PLUS" and
                    zone.name == "Aura Addressable 1"):

                logger.debug(f"Zone {zone.name}, the Arctic Liquid-Freezer III, "
                            "has {led_count} addressable LEDs. "
                            "1st 12 : CPU Fan and Front Radiator Fan, "
                            "2nd 12 : Back Radiator Fan")

                color_count = len(zone.leds)//2
                logger.debug(f"Get the first {color_count} colours.")
                spectrum_colors = get_RGB_color_spectrum(color_count)
                logger.debug(f"Repeat colours for second {color_count} colours.")

                for color_index in range(color_count):
                    spectrum_colors.append(spectrum_colors[color_index])
                    logger.debug(f"RGBcolors[{12+color_index}]: "
                                f"Mapped to {spectrum_colors[12+color_index]}")

            else:
                logger.debug(f"Zone {zone.name} has {led_count} addressable LEDs")
                color_count = len(zone.leds)
                spectrum_colors = get_RGB_color_spectrum(color_count)

            zone_leds_color_map[zone.name] = spectrum_colors

        return (zone_leds_color_map)

    except Exception as e:

        logger.error(f"Error occurred while getting spectrum colors: {e}")
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

        logger.error(f"Error occurred while trying to set bespoke lighting: {e}")
        raise

###############################################################################


def show_i2c_interfaces(client):

    try:
        response = requests.get('http://localhost:6742/i2c')
        response.raise_for_status()  # Raise an error for bad responses
        interfaces = response.json()  # Parse the JSON response

        if interfaces:
            logger.info("I2C Interfaces:")
            for interface in interfaces:
                logger.info(f"  - {interface}")
        else:
            logger.info("No I2C interfaces found.")

    except requests.exceptions.RequestException as e:
        logger.error(f"Error accessing I2C interfaces: {e}")
        raise

###############################################################################


def set_colors_by_mode(client, mode):

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
            logger.info(f"{device_index} Device {device.name}")
            show_device_info(device)

    except Exception as e:
        logger.error(f"Error occurred while showing device info: {e}")
        raise

###############################################################################


if __name__ == config.MAIN:

    logging.basicConfig(level=DEBUG_LEVEL)
    logger = logging.getLogger(__name__)

    try:

        try:

            args = get_args(sys.argv)
            server_process = start_openRGB_server()

        except Exception:
            logger.error("Startup Error. Exiting")
            raise

        try:

            client = connect_openRGB_client()

            if args[MODE_ARG] == "Info":
                show_devices_info(client.devices)
                # show_i2c_interfaces(client)
            elif args[MODE_ARG] == "Single":

                level = args[LEVEL_ARG] if len(args) == MAX_ARGS else None
                set_devices_to_single_color(client.devices, args[COLOR_ARG], level)

            else:
                set_colors_by_mode(client, args[MODE_ARG])

            disconnect_openRGB_client(client)

        except Exception as e:
            logger.exception(f"Processing Error: {e}. Exiting")

        finally:
            terminate_openRGB_server(server_process)
            raise

    except Exception as e:
        logger.exception(f"{e}: Terminating Script")

    finally:

        logger.error(f"Script terminates in {config.CLOSE_SCRIPT_WAIT_SECS} "
                     "seconds....")

        time.sleep(config.CLOSE_SCRIPT_WAIT_SECS)  # Wait before closing
