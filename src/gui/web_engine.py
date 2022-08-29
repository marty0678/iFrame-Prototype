from PySide6.QtCore import Slot, QUrl, QTimer
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineProfile, QWebEnginePage
from PySide6.QtNetwork import QNetworkCookie

import src.config as config


class WebEngineView(QWebEngineView):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.timer = QTimer()

        self.cookie_store = self.page().profile().cookieStore()
        self.cookies = {}

        if config.PERSIST_SESSION:
            self.construct_profile()

        self.init_cookies()
        self.register_signals()

        self.timer.start(5000)

    def closeEvent(self, event) -> None:
        if config.PURGE_COOKIES_ON_CLOSE:
            # BUG: After the refactor this doesn't work.
            self.cookie_store.deleteAllCookies()
            self.cookies = {}

        self.timer.stop()

        event.accept()

    def construct_profile(self) -> None:
        """Construct custom profile and page so we may
        persist the session in a local DB."""

        # BUG: Disabling this as whenever this is active,
        # the persistance does work (after QT's 30 second delay)
        # but all navigation breaks in the browser, despite the
        # actions being enabled. I'm probably missing something.
        
        # BUG 2: After the refactor, the on_cookie_added signal
        # no longer is being being received
        self.profile = QWebEngineProfile("default", self)
        self.profile.setCachePath("./cache")
        self.profile.setPersistentStoragePath("./storage")

        self.web_page = QWebEnginePage(self.profile, self)

        self.setPage(self.web_page)

        self.page().profile().setPersistentCookiesPolicy(
            QWebEngineProfile.ForcePersistentCookies
        )

    def register_signals(self):
        self.cookie_store.cookieAdded.connect(self.on_cookie_added)

        self.timer.timeout.connect(self.on_tick)

    def init_cookies(self):
        """Registers a test cookie for demonstration purposes."""

        cookie = QNetworkCookie(
            "my_sample_cookie".encode(), "This is just a test cookie".encode()
        )
        cookie.setDomain("www.example.com")
        cookie.setPath("/")

        self.cookie_store.setCookie(cookie, QUrl())

    @Slot(QNetworkCookie)
    def on_cookie_added(self, cookie):
        print(f"Cookie added: {cookie.name()}")

        cookie_name = cookie.name().toStdString()
        self.cookies[cookie_name] = cookie

    @Slot()
    def on_tick(self):
        """Just to monitor the cookies for testing."""

        print("Cookies:")
        for cookie_name, cookie in self.cookies.items():
            print(cookie.toRawForm().toStdString())
