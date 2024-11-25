from openrgb import OpenRGBClient
import os
import time
import socket
import subprocess
import logging
from .config import (EXE,
                     LOGLEVEL,
                     LOGLEVEL_ARG,
                     PATH,
                     SERVER_ARG,
                     STARTUP_WAIT_SECS,
                     TERMINATE_WAIT_SECS,
                     LOCAL_HOST,
                     PORT)

# Create a logger for this module
logger = logging.getLogger(__name__)  # __name__ gives "package.module"

###############################################################################


def is_openrgb_server_running(host, port):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(10)  # 10 seconds timeout
        return sock.connect_ex((host, port)) == 0

###############################################################################


def start_openRGB_server():

    try:

        # Construct the full path for OpenRGB
        open_rgb_full_path = os.path.join(PATH,
                                          EXE)

        logger.info("Starting subprocess: "
                    f"{open_rgb_full_path} "
                    f"{SERVER_ARG} "
                    f"{LOGLEVEL_ARG} "
                    f"{LOGLEVEL}")

        try:
            OpenRGBServerProcess = subprocess.Popen(
                [open_rgb_full_path,
                 SERVER_ARG,
                 LOGLEVEL_ARG,
                 LOGLEVEL])

        except Exception as exception_msg:
            logger.exception(f"Failed to start OpenRGB: {exception_msg}")

        logger.info(f"Waiting {STARTUP_WAIT_SECS} "
                    "seconds for OpenRGB Server to start.")

        time.sleep(STARTUP_WAIT_SECS)  # Wait b4 check

        if is_openrgb_server_running(LOCAL_HOST,
                                     PORT):
            logger.info("OpenRGB server is running and reachable.")
        else:
            raise RuntimeError("OpenRGB server failed to start in "
                               f"{STARTUP_WAIT_SECS}"
                               " seconds.")

        return (OpenRGBServerProcess)

    except Exception as exception_msg:
        logger.exception(f"Server Start Error: {exception_msg}")

###############################################################################


def connect_openRGB_client(numberOfDevices):

    try:

        # Connect to OpenRGB server
        client = OpenRGBClient(LOCAL_HOST,
                               PORT)

        if len(client.devices) == numberOfDevices:

            logger.info("Connected to OpenRGBClient with "
                        f"{len(client.devices)} devices.")

        else:

            raise RuntimeError("OpenRGBClient couldn't connect with all "
                               f"{numberOfDevices} devices.")

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

        if is_openrgb_server_running(LOCAL_HOST,
                                     PORT):

            OpenRGB_server_process.terminate()

            logger.info("Waiting "
                        f"{TERMINATE_WAIT_SECS} "
                        "seconds for OpenRGB Server to terminate.")

            # Wait before checking
            time.sleep(TERMINATE_WAIT_SECS)

            if is_openrgb_server_running(LOCAL_HOST,
                                         PORT):
                raise RuntimeError("OpenRGB server failed to terminate.")
            else:
                logger.info("OpenRGB server process terminated.")

        else:

            raise RuntimeError("OpenRGB server not found / "
                               "already terminated.")

    except Exception as exception_msg:
        logger.error(f"{exception_msg}")
        raise
