from psutil import (Process, process_iter,
                    NoSuchProcess, AccessDenied, ZombieProcess)
from sys import platform
import os
from subprocess import Popen, DETACHED_PROCESS, CREATE_NO_WINDOW
from typing import Dict

from .config import (WINDOWS,
                     PROCESS_ID,
                     PROCESS_NAME)

from common_lib.translator import translate

# Create a logger for this module
import logging
logger = logging.getLogger(__name__)  # __name__ gives "package.module"

###############################################################################


def start_process(args: list[str]) -> Process:

    # Start a process. args must be prevalidated

    try:
        proc: Process

        if platform == WINDOWS:
            proc = Popen(args,
                         creationflags=DETACHED_PROCESS | CREATE_NO_WINDOW)
        else:
            proc = Popen(args, preexec_fn=os.setsid)

        return proc

    except Exception as e:

        logger.exception(f"{translate('TEXT_ProcessStartError')}: {str(e)}")


###############################################################################

def is_process_running(proc_id: int) -> bool:

    logger.debug(f"{translate("TEXT_CheckProcessRunning")}: {proc_id}.")

    for proc in process_iter([PROCESS_ID, PROCESS_NAME]):

        if proc_id == proc.info[PROCESS_ID]:
            return True

    return False


###############################################################################


# Function to get a dictionary of all currently running processes

def get_proc_dict() -> Dict[str, Process]:

    logger.debug(f"{translate("TEXT_GettingProcessDictionary")}.")

    process_dict: Dict[str, Process] = {}

    try:

        dupl_proc_set: set[str] = set()

        for proc in process_iter([PROCESS_ID, PROCESS_NAME]):

            pid: int = proc.info[PROCESS_ID]
            pname: str = proc.info[PROCESS_NAME].lower()

            if not isinstance(pid, int):
                raise RuntimeError(f"{translate("TEXT_InvalidProcIdType")}: "
                                   f"{pid}")
            if not isinstance(pname, str):
                raise RuntimeError(f"{translate("TEXT_InvalidProcNameType")}: "
                                   f"{pname}")

            if not isinstance(proc, Process):
                raise RuntimeError(f"{translate("TEXT_InvalidProcObject")}: "
                                   f"{pid} {pname}")

            if pname in process_dict:
                logger.debug(f"{translate("TEXT_DuplProcessName")}: "
                             f"{pid} {pname}")
                dupl_proc_set.add(pname)
            else:
                process_dict[pname] = proc
                logger.debug(f"{translate("TEXT_AddedProcToDict")}: "
                             f"{pname}, {pid}.")

        for procname in dupl_proc_set:
            duplproc: Process = process_dict.pop(procname)
            logger.debug(f"{translate("TEXT_PoppedDuplProcFromDict")} :"
                         f"{duplproc.info[PROCESS_ID]} "
                         f"{duplproc.info[PROCESS_NAME]}")

        return process_dict

    except (NoSuchProcess, AccessDenied, ZombieProcess,
            RuntimeError) as e:
        logger.exception(f"{translate('TEXT_ProcessAccessError')}: {str(e)}")


###############################################################################
""" DEPRECATED

def get_process(process_name: str) -> Process:

    logger.debug(f"{translate("WORD_Getting")}: {process_name}.")

    process_dict: Dict[int, Process] = get_process_dict()
    pid_list: list[int] = []
    process_name_lower: str = process_name.lower()

    for pid, proc in process_dict.items():
        name: str = proc.info[PROCESS_NAME].lower()
        if name == process_name_lower:
            pid_list.append(pid)

    if len(pid_list) == 1:
        proc = process_dict.get(pid_list[0])
        logger.info(f"{translate("WORD_Process")} "
                    f"{proc.info[PROCESS_NAME]}, "
                    f"{proc.info[PROCESS_ID]}. *** "
                    f"{translate("WORD_Found")} ***")
        return (proc)

    logger.warning(f"{translate("WORD_Process")} {process_name} *** "
                   f"{translate("WORD_Not")} {translate("WORD_Found")} ***")

    return None
"""
