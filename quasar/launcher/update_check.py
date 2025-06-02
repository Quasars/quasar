import logging
import time
import sys
from packaging.version import Version

from AnyQt.QtCore import QSettings, QThread, pyqtSignal, Qt, QUrl
from AnyQt.QtGui import QDesktopServices, QIcon
from AnyQt.QtWidgets import QMessageBox
from urllib.request import urlopen, Request

from orangecanvas.utils.overlay import Notification

from Orange import canvas
from Orange.version import version as current_orange
from Orange.util import resource_filename


log = logging.getLogger(__name__)


def current_version():
    from quasar.launcher import version as quasar_version
    return quasar_version()


def ua_string():
    is_anaconda = 'Continuum' in sys.version or 'conda' in sys.version
    return ('Quasar{quasar_version}:Orange{orange_version}:Python{py_version}'
            ':{platform}:{conda}:{uuid}').format(
        quasar_version=current_version(),
        orange_version=current_orange,
        py_version=sys.version.split()[0],
        platform=sys.platform,
        conda='Anaconda' if is_anaconda else '',
        uuid=QSettings().value("error-reporting/machine-id", "", str)
    )


def check_for_updates():
    settings = QSettings()
    check_updates = settings.value('startup/check-updates', True, type=bool)
    last_check_time = settings.value('startup/last-update-check-time', 0, type=int)
    ONE_DAY = 86400

    if check_updates and time.time() - last_check_time > ONE_DAY:
        settings.setValue('startup/last-update-check-time', int(time.time()))

        class GetLatestVersion(QThread):
            resultReady = pyqtSignal(str)

            def run(self):
                try:
                    request = Request('https://quasar.biolab.si/version/',
                                      headers={
                                          'Accept': 'text/plain',
                                          'Accept-Encoding': 'identity',
                                          'Connection': 'close',
                                          'User-Agent': ua_string()})
                    contents = urlopen(request, timeout=10).read().decode()
                # Nothing that this fails with should make Orange crash
                except Exception:  # pylint: disable=broad-except
                    log.exception('Failed to check for updates')
                else:
                    self.resultReady.emit(contents)

        def compare_versions(latest):
            skipped = settings.value('startup/latest-skipped-version', "", type=str)
            if Version(latest) <= Version(current_version()) or \
                    latest == skipped:
                return

            notif = Notification(title='Quasar Update Available',
                                 text='Current version: <b>{}</b><br>'
                                      'Latest version: <b>{}</b>'.format(current_version(), latest),
                                 accept_button_label="Download",
                                 reject_button_label="Skip this Version",
                                 icon=QIcon(resource_filename("canvas/icons/update.png")))

            def handle_click(role):

                if role == notif.RejectRole:
                    settings.setValue('startup/latest-skipped-version', latest)
                if role == notif.AcceptRole:
                    QDesktopServices.openUrl(QUrl("https://quasar.codes/download/"))

            notif.clicked.connect(handle_click)
            canvas.notification_server_instance.registerNotification(notif)

        thread = GetLatestVersion()
        thread.resultReady.connect(compare_versions)
        thread.start()
        return thread
    return None