import os
from PySide6.QtCore import QThreadPool, QSize, QUrl, Slot
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtGui import QShortcut, QKeySequence

import src.config as config
from src.enums.operation_modes import OperationModes
from src.gui.web_engine import WebEngineView
from src.network.backend import Backend
from src.gui.compiled.main_window import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.threadpool = QThreadPool.globalInstance()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.frame = FrameWindow()

        self.signals()

    def closeEvent(self, event) -> None:
        self.frame.close()
        del self.frame

        event.accept()

    def signals(self):
        """Watches for button pushes."""

        self.ui.launchFrame.clicked.connect(lambda: self.launch_frame())
        QShortcut(QKeySequence("F12"), self, lambda: self.close_frame())

    @Slot()
    def launch_frame(self):
        """Launches the frame."""

        self.frame.show()

    @Slot()
    def close_frame(self):
        self.frame.close()


class FrameWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setup_websocket()
        self.setup_ui()

    def showEvent(self, event) -> None:
        self.view = WebEngineView(self)

        self.setup_frame_ui()

        self.show_frame()
        event.accept()

    def closeEvent(self, event) -> None:
        self.view.close()
        del self.view

        event.accept()

    def setup_ui(self):
        self.setMinimumSize(QSize(800, 600))
        self.resize(QSize(800, 600))

    def setup_frame_ui(self):
        self.view.setMinimumSize(QSize(800, 600))
        self.view.resize(QSize(800, 600))

    def setup_websocket(self):
        self.backend = Backend()

        self.channel = QWebChannel()

        self.channel.registerObject("backend", self.backend)

    def show_frame(self):
        """Launches the frame."""

        self.view.page().setWebChannel(self.channel)

        path = os.path.abspath("src\\web\\index.html")

        match config.OPERATION_MODE:
            case OperationModes.LOCAL:
                self.view.load(QUrl.fromLocalFile(path))
            case OperationModes.EXTERNAL:
                self.view.load(QUrl(config.WEBSITE_URL))

        self.view.show()
