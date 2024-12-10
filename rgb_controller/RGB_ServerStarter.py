import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCloseEvent, QIcon
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu
from psutil import Process
from logging import (getLogger, Logger)
from typing import Dict

from common_lib.config import (MAIN, CLOSE_SCRIPT_WAIT_SECS)
from common_lib.utils import start_script, close_script
from common_lib.translator import translate

from system_lib.utils import (get_proc_dict, is_process_running)
from system_lib.config import PROCESS_ID

from rgb_lib.open_RGB_utils import (start_openRGB_server,
                                    is_openrgb_server_running,
                                    is_openrgb_server_available)

# Create a logger for this module
logger: Logger = getLogger(__name__)  # __name__ gives "package.module"


class RGBServerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("StartOpenRGB")
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

        # Central widget
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)

        # Buttons
        self.restart_button = QPushButton("Restart Server", self)
        self.terminate_button = QPushButton("Terminate Server", self)
        self.restart_button.clicked.connect(self.restart_server)
        self.terminate_button.clicked.connect(self.terminate_server)

        layout.addWidget(self.restart_button)
        layout.addWidget(self.terminate_button)
        self.setCentralWidget(central_widget)

        # System tray
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("icon.png"))  # Replace "icon.png" with a valid path
        self.tray_icon.setToolTip("OpenRGB Server")

        tray_menu = QMenu()
        open_action = tray_menu.addAction("Open")
        open_action.triggered.connect(self.show)

        quit_action = tray_menu.addAction("Quit")
        quit_action.triggered.connect(self.quit_application)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.show_from_tray)
        self.tray_icon.show()

        self.server_proc = None  # Process for OpenRGB server

    def start_server(self):
        try:
            ProcDict: Dict = get_proc_dict()
            if not is_openrgb_server_running(ProcDict):
                self.server_proc = start_openRGB_server()
                if not is_process_running(self.server_proc.pid):
                    raise RuntimeError(translate("TEXT_ServerStartFailed"))

            if not is_openrgb_server_available():
                raise RuntimeError(translate("TEXT_ServerNotAvailable"))
        except Exception as e:
            logger.exception(str(e))
            QMessageBox.critical(self, "Error", str(e))

    def terminate_server(self):
        if self.server_proc:
            self.server_proc.terminate()
            self.server_proc = None
            QMessageBox.information(self, "Terminate Server", "Server process terminated.")

    def restart_server(self):
        self.terminate_server()
        self.start_server()

    def show_from_tray(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.show()

    def quit_application(self):
        self.terminate_server()
        QApplication.quit()

    def closeEvent(self, event: QCloseEvent):
        """Minimize to tray instead of closing."""
        event.ignore()
        self.hide()
        self.tray_icon.showMessage("OpenRGB Server", "Application minimized to tray.")


if __name__ == MAIN:
    app = QApplication(sys.argv)
    gui = RGBServerGUI()
    gui.start_server()
    gui.show()
    sys.exit(app.exec_())
