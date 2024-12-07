from openrgb import OpenRGBClient
import os
import time
import socket
import subprocess
from .config import (EXE,
                     LOGLEVEL,
                     LOGLEVEL_ARG,
                     PATH,
                     SERVER_ARG,
                     STARTUP_WAIT_SECS,
                     TERMINATE_WAIT_SECS,
                     LOCAL_HOST,
                     PORT)

from common_lib.translator import translate

# Create a logger for this module
import logging
logger = logging.getLogger(__name__)  # __name__ gives "package.module"

###############################################################################


def is_openrgb_server_running(host, port):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(10)  # 10 seconds timeout
        return sock.connect_ex((host, port)) == 0

###############################################################################


def start_openRGB_server():

    # Construct the full path for OpenRGB
    open_rgb_full_path = os.path.join(PATH, EXE)

    OpenRGBServerProcess = subprocess.Popen([open_rgb_full_path,
                                            SERVER_ARG,
                                            LOGLEVEL_ARG,
                                            LOGLEVEL])

    logger.info(f"{translate("INFO_ServerStart")}: "
                f"{open_rgb_full_path} "
                f"{SERVER_ARG} "
                f"{LOGLEVEL_ARG} "
                f"{LOGLEVEL}")
    logger.info(f"{translate("INFO_ServerWait")}: "
                f"{STARTUP_WAIT_SECS}")

    time.sleep(STARTUP_WAIT_SECS)  # Wait b4 check

    if is_openrgb_server_running(LOCAL_HOST, PORT):
        logger.info(f"{translate("INFO_ServerRunning")}.")
    else:
        raise RuntimeError(f"{translate("ERROR_ServerStartFailed")}.")

    return (OpenRGBServerProcess)

###############################################################################


def connect_openRGB_client(numberOfDevices):

    # Connect to OpenRGB server
    client = OpenRGBClient(LOCAL_HOST, PORT)

    if len(client.devices) == numberOfDevices:

        logger.info(f"{translate("INFO_Connected")}. "
                    f"{translate("INFO_Devices")}: "
                    f"{len(client.devices)}")

    else:

        raise RuntimeError(f"{translate("ERROR_FailedConnectDevices")}. "
                           f"{translate("WORD_Expected")} {numberOfDevices}, "
                           f"{translate("WORD_Found")} {(client.devices)}.")

    return (client)

###############################################################################


def disconnect_openRGB_client(OpenRGB_client):

    OpenRGB_client.disconnect()
    logger.info(f"{translate("INFO_ServerDisconnected")}.")

###############################################################################


def terminate_openRGB_server(OpenRGB_server_process):

    if is_openrgb_server_running(LOCAL_HOST, PORT):

        OpenRGB_server_process.terminate()

        logger.info(
            f"{translate("INFO_ServerStopWait")}: "
            f"{TERMINATE_WAIT_SECS}")

        # Wait before checking
        time.sleep(TERMINATE_WAIT_SECS)

        if is_openrgb_server_running(LOCAL_HOST, PORT):
            raise RuntimeError(
                f"{translate("ERROR_ServerStopFailed")}.")
        else:
            logger.info(f"{translate("INFO_ServerStopped")}.")

    else:

        raise RuntimeError(
            f"{translate("ERROR_ServerNotRunning")}.")
