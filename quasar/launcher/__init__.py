import pkg_resources

from AnyQt.QtCore import Qt
from AnyQt.QtGui import QColor, QIcon

from orangecanvas.gui.splashscreen import SplashScreen
from Orange.canvas import config, __main__ as main, mainwindow

from quasar.launcher.splash import splash_screen
from quasar.launcher.update_check import check_for_updates


def version():
    return pkg_resources.get_distribution("Quasar").version


class QuasarConfig(config.Config):
    ApplicationName = "Quasar"
    ApplicationVersion = version()

    @staticmethod
    def splash_screen():
        return splash_screen()

    @staticmethod
    def core_packages():
        # type: () -> List[str]
        return super(QuasarConfig, QuasarConfig).core_packages() + [
            "orange-spectroscopy",
        ]

    @staticmethod
    def application_icon():
        path = pkg_resources.resource_filename(
            __name__, "icons/quasar.svg")
        return QIcon(path)


class QuasarSplashScreen(SplashScreen):

    def showMessage(self, message, alignment=Qt.AlignLeft, color=Qt.black):
        super().showMessage(message, alignment=alignment, color=QColor("#ff6d00"))


class Launcher:
    def launch(self):
        config.Config = QuasarConfig
        self.fix_application_dirs()
        self.replace_update_check()
        self.replace_splash_screen()
        self.main()

    def fix_application_dirs(self):
        import os, sys
        from Orange.misc import environ

        def data_dir(versioned=True):
            """
            Return the platform dependent Orange data directory.

            This is ``data_dir_base()``/Orange/__VERSION__/ directory if versioned is
            `True` and ``data_dir_base()``/Orange/ otherwise.
            """
            base = environ.data_dir_base()
            if versioned:
                return os.path.join(base, "quasar", version())
            else:
                return os.path.join(base, "quasar")

        environ.data_dir = data_dir

        def cache_dir(*args):
            """
            Return the platform dependent Orange cache directory.
            """
            if sys.platform == "darwin":
                base = os.path.expanduser("~/Library/Caches")
            elif sys.platform == "win32":
                base = os.getenv("APPDATA", os.path.expanduser("~/AppData/Local"))
            elif os.name == "posix":
                base = os.getenv("XDG_CACHE_HOME", os.path.expanduser("~/.cache"))
            else:
                base = os.path.expanduser("~/.cache")

            base = os.path.join(base, "quasar", version())
            if sys.platform == "win32":
                # On Windows cache and data dir are the same.
                # Microsoft suggest using a Cache subdirectory
                return os.path.join(base, "Cache")
            else:
                return base

        environ.cache_dir = cache_dir

    def replace_splash_screen(self):
        main.SplashScreen = QuasarSplashScreen

    def replace_update_check(self):
        from Orange.canvas import __main__
        __main__.check_for_updates = check_for_updates

    def main(self):
        from Orange.canvas.__main__ import main
        main()
