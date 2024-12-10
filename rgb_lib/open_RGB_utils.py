from typing import Dict
from openrgb import OpenRGBClient
import os
import time
import socket
from psutil import Process

from .config import (EXE,
                     LOGLEVEL,
                     LOGLEVEL_ARG,
                     PATH,
                     SERVER_ARG,
                     STARTUP_WAIT_SECS,
                     TERMINATE_WAIT_SECS,
                     HOST,
                     PORT,
                     SOCKET_TIMEOUT_SECS)

from common_lib.translator import translate
from system_lib.utils import start_process  # , get_process

# Create a logger for this module
import logging
logger = logging.getLogger(__name__)  # __name__ gives "package.module"

###############################################################################


def is_openrgb_server_running(ProcDict: Dict) -> bool:

    if EXE.lower() in ProcDict:
        logger.info(f"{translate("TEXT_OpenRGBServerRunning")}.")
        return True

    logger.warning(f"{translate("TEXT_OpenRGBServerNotRunning")}.")
    return False

###############################################################################


def is_openrgb_server_available() -> bool:

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(SOCKET_TIMEOUT_SECS)
        server = (HOST, PORT)
        serverTestResult = sock.connect_ex(server)
        if serverTestResult == 0:
            logger.info(f"{translate("TEXT_ServerAvailable")}: {EXE}, "
                        f"{translate("WORD_host")}: {HOST}, "
                        f"{translate("WORD_port")}: {PORT}.")

            return True

    logger.warning(f"{translate("TEXT_ServerNotAvailable")}: {EXE}, "
                   f"{translate("WORD_host")}: {HOST}, "
                   f"{translate("WORD_port")}: {PORT}.")

    return False

###############################################################################


"""DEPRECATED
def get_OpenRGB_server() -> Process:

    if (is_openrgb_server_running()):
        return get_process(EXE)

    return None
"""
###############################################################################


def start_openRGB_server() -> Process:

    open_rgb_full_path: str = os.path.join(PATH, EXE)
    args = [open_rgb_full_path, SERVER_ARG, LOGLEVEL_ARG, LOGLEVEL]

    logger.info(f"{translate("INFO_ServerStart")}: {args}")

    proc: Process = start_process(args)

    logger.info(f"{translate("INFO_ServerWait")}: {STARTUP_WAIT_SECS}")
    time.sleep(STARTUP_WAIT_SECS)  # Wait for server to start properly

    return proc

###############################################################################


def connect_openRGB_client(numberOfDevices):

    # Connect to OpenRGB server
    client = OpenRGBClient(HOST, PORT)

    if len(client.devices) == numberOfDevices:

        logger.info(f"{translate("INFO_Connected")}. "
                    f"{translate("INFO_Devices")}: "
                    f"{len(client.devices)}")
        return (client)

    raise RuntimeError(f"{translate("ERROR_FailedConnectDevices")}. "
                       f"{translate("WORD_Expected")} {numberOfDevices}, "
                       f"{translate("WORD_Found")} {(client.devices)}.")

###############################################################################


def disconnect_openRGB_client(OpenRGB_client):

    OpenRGB_client.disconnect()
    logger.info(f"{translate("INFO_ServerDisconnected")}.")

###############################################################################


def terminate_openRGB_server(OpenRGB_server_process):

    if is_openrgb_server_running():

        OpenRGB_server_process.terminate()

        logger.info(
            f"{translate("INFO_ServerStopWait")}: "
            f"{TERMINATE_WAIT_SECS}")

        # Wait before checking
        time.sleep(TERMINATE_WAIT_SECS)

        if is_openrgb_server_running():
            raise RuntimeError(
                f"{translate("ERROR_ServerStopFailed")}.")
        else:
            logger.info(f"{translate("INFO_ServerStopped")}.")

    else:

        raise RuntimeError(
            f"{translate("ERROR_ServerNotRunning")}.")
