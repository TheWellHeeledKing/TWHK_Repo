from openrgb import OpenRGBClient
import os
import time
import socket
import subprocess
import logging
import config

# Create a logger for this module
logger = logging.getLogger(__name__)

###############################################################################


def is_openrgb_server_running(host, port):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(10)  # 10 seconds timeout
        return sock.connect_ex((host, port)) == 0

###############################################################################


def start_openRGB_server():

    try:

        # Construct the full path for OpenRGB
        open_rgb_full_path = os.path.join(config.OPEN_RGB_PATH,
                                          config.OPEN_RGB_EXE)

        logger.info("Starting subprocess: "
                    f"{open_rgb_full_path} "
                    f"{config.OPEN_RGB_SERVER_ARG} "
                    f"{config.OPEN_RGB_LOGLEVEL_ARG} "
                    f"{config.OPEN_RGB_LOGLEVEL}")

        try:
            OpenRGBServerProcess = subprocess.Popen(
                [open_rgb_full_path,
                 config.OPEN_RGB_SERVER_ARG,
                 config.OPEN_RGB_LOGLEVEL_ARG,
                 config.OPEN_RGB_LOGLEVEL])

        except Exception as exception_msg:
            logger.exception(f"Failed to start OpenRGB: {exception_msg}")

        logger.info(f"Waiting {config.OPEN_RGB_STARTUP_WAIT_SECS} seconds "
                    "for OpenRGB Server to start.")

        time.sleep(config.OPEN_RGB_STARTUP_WAIT_SECS)  # Wait before checking

        if is_openrgb_server_running(config.LOCAL_HOST, config.PORT):
            logger.info("OpenRGB server is running and reachable.")
        else:
            raise RuntimeError("OpenRGB server failed to start in "
                               f"{config.OPEN_RGB_STARTUP_WAIT_SECS} seconds.")

        return (OpenRGBServerProcess)

    except Exception as exception_msg:
        logger.exception(f"Server Start Error: {exception_msg}")

###############################################################################


def connect_openRGB_client():

    try:

        # Connect to OpenRGB server
        client = OpenRGBClient(config.LOCAL_HOST, config.PORT)

        if len(client.devices) == config.NUMBER_OF_RGB_DEVICES:

            logger.info("Connected to OpenRGBClient with "
                        f"{len(client.devices)} devices.")

        else:

            raise RuntimeError("OpenRGBClient couldn't connect with all "
                               f"{config.NUMBER_OF_RGB_DEVICES} devices.")

        return (client)

    except Exception as exception_msg:

        logger.exception(f"OpenRGBClient connection failed: {exception_msg}:")

###############################################################################


def disconnect_openRGB_client(OpenRGB_client):

    try:

        OpenRGB_client.disconnect()
        logger.info("Disconnected from OpenRGB Server")

    except Exception as exception_msg:
        logger.exception(f"{exception_msg}")

###############################################################################


def terminate_openRGB_server(OpenRGB_server_process):

    try:

        if is_openrgb_server_running(config.LOCAL_HOST, config.PORT):

            OpenRGB_server_process.terminate()

            logger.info(f"Waiting {config.OPEN_RGB_TERMINATE_WAIT_SECS} "
                        "seconds for OpenRGB Server to terminate.")

            time.sleep(config.OPEN_RGB_TERMINATE_WAIT_SECS)  # Wait b4 checking

            if is_openrgb_server_running(config.LOCAL_HOST, config.PORT):
                raise RuntimeError("OpenRGB server failed to terminate.")
            else:
                logger.info("OpenRGB server process terminated.")

        else:

            raise RuntimeError("OpenRGB server not found / "
                               "already terminated.")

    except Exception as exception_msg:
        logger.error(f"{exception_msg}")
        raise
