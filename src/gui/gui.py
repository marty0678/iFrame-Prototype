import os
from PySide6.QtCore import QThreadPool, QUrl, QSize
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebChannel import QWebChannel

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

    def signals(self):
        """Watches for button pushes."""

        self.ui.launchFrame.clicked.connect(lambda: self.launch_frame())

    def launch_frame(self):
        """Launches the frame."""

        self.frame.show()


class FrameWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.view = QWebEngineView(self)

        self.setup_ui()
        self.setup_websocket()
        self.show_frame()

    def setup_ui(self):
        self.view.setMinimumSize(QSize(800, 600))
        self.view.resize(QSize(800, 600))

        self.setMinimumSize(QSize(800, 600))
        self.resize(QSize(800, 600))

    def setup_websocket(self):
        self.backend = Backend()

        self.channel = QWebChannel()

        self.view.page().setWebChannel(self.channel)
        self.channel.registerObject("backend", self.backend)

    def show_frame(self):
        """Launches the frame."""

        path = os.path.abspath("src\\web\\index.html")

        self.view.load(QUrl.fromLocalFile(path))
        self.view.show()
