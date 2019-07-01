from quasar.launcher.splash import splash_screen
from quasar.launcher.update_check import check_for_updates


def version():
    import pkg_resources
    return pkg_resources.get_distribution("Quasar").version


class Launcher:
    def launch(self):
        self.fix_application_name()
        self.fix_application_dirs()
        self.fix_application_icon()
        self.replace_update_check()
        self.replace_splash_screen()
        self.main()

    def fix_application_name(self):
        from PyQt5.QtCore import QCoreApplication, QSettings
        from Orange.canvas import config

        def init():
            """
            Initialize the QCoreApplication.organizationDomain, applicationName,
            applicationVersion and the default settings format. Will only run once.

            .. note:: This should not be run before QApplication has been initialized.
                      Otherwise it can break Qt's plugin search paths.

            """
            QCoreApplication.setOrganizationDomain("Quasars")
            QCoreApplication.setApplicationName("Quasar")
            QCoreApplication.setApplicationVersion(version())
            QSettings.setDefaultFormat(QSettings.IniFormat)

            # Make it a null op.
            config.init = lambda: None
        config.init = init

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

    def fix_application_icon(self):
        import pkg_resources
        from Orange.canvas import config
        from AnyQt.QtGui import QIcon

        def application_icon():
            path = pkg_resources.resource_filename(
                __name__, "icons/quasar.svg")
            return QIcon(path)
        config.application_icon = application_icon

    def replace_splash_screen(self):
        from AnyQt.QtCore import Qt
        from AnyQt.QtGui import QColor
        from Orange.canvas import config
        try:
            from orangecanvas.gui.splashscreen import SplashScreen
        except ImportError:
            from Orange.canvas.gui.splashscreen import SplashScreen

        config.splash_screen = splash_screen

        sm = SplashScreen.showMessage

        # showing currently loading widget
        def showMessage(self, message, alignment=Qt.AlignLeft, color=Qt.black):
            sm(self, message, alignment=alignment, color=QColor("#ff6d00"))

        SplashScreen.showMessage = showMessage

    def replace_update_check(self):
        from Orange.canvas import __main__
        __main__.check_for_updates = check_for_updates

    def main(self):
        from Orange.canvas.__main__ import main
        main()
