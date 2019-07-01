import logging
import time
import sys
import pkg_resources

from AnyQt.QtCore import QSettings, QThread, pyqtSignal, Qt, QUrl
from AnyQt.QtGui import QDesktopServices
from AnyQt.QtWidgets import QMessageBox
from urllib.request import urlopen, Request
from Orange.version import version as current


log = logging.getLogger(__name__)
VERSION_URL = 'https://quasar.biolab.si/version/'
DOWNLOAD_URL = 'https://quasar.codes/download/'
USER_AGENT = 'Quasar{quasar_version}:Orange{orange_version}:Python{py_version}:{platform}:{conda}'
UPDATE_AVAILABLE_TITLE = 'Quasar Update Available'
UPDATE_AVAILABLE_MESSAGE = (
    'A newer version of Quasar is available.<br><br>'
    '<b>Current version:</b> {current_version}<br>'
    '<b>Latest version:</b> {latest_version}'
)


def check_for_updates():
    settings = QSettings()
    check_updates = settings.value('startup/check-updates', True, type=bool)
    last_check_time = settings.value('startup/last-update-check-time', 0, type=int)
    ONE_DAY = 86400

    if check_updates and time.time() - last_check_time > ONE_DAY:
        settings.setValue('startup/last-update-check-time', int(time.time()))

        thread = GetLatestVersion()
        thread.resultReady.connect(compare_versions)
        thread.start()
        return thread


class GetLatestVersion(QThread):
    resultReady = pyqtSignal(str)

    def version(self):
        request = Request(VERSION_URL,
                          headers={
                              'Accept': 'text/plain',
                              'Accept-Encoding': 'gzip, deflate',
                              'Connection': 'close',
                              'User-Agent': self.ua_string()})
        contents = urlopen(request, timeout=10).read().decode()
        return contents

    def run(self):
        try:
            contents = self.version()
        # Nothing that this fails with should make Orange crash
        except Exception:  # pylint: disable=broad-except
            log.exception('Failed to check for updates')
        else:
            self.resultReady.emit(contents)

    @staticmethod
    def ua_string():
        is_anaconda = 'Continuum' in sys.version or 'conda' in sys.version
        return USER_AGENT.format(
            quasar_version=current_version(),
            orange_version=current,
            py_version=sys.version.split()[0],
            platform=sys.platform,
            conda='Anaconda' if is_anaconda else '',
        )


def current_version():
    from quasar.launcher import version as quasar_version
    return quasar_version()


def compare_versions_messagebox(latest):
    current = current_version()
    version = pkg_resources.parse_version
    if version(latest) <= version(current):
        return
    question = QMessageBox(
        QMessageBox.Information,
        UPDATE_AVAILABLE_TITLE,
        UPDATE_AVAILABLE_MESSAGE.format(
            current_version=current,
            latest_version=latest),
        textFormat=Qt.RichText)
    ok = question.addButton('Download Now', question.AcceptRole)
    question.setDefaultButton(ok)
    question.addButton('Remind Later', question.RejectRole)
    question.finished.connect(
        lambda:
        question.clickedButton() == ok and
        QDesktopServices.openUrl(QUrl(DOWNLOAD_URL)))
    question.show()


def compare_versions_notification(latest):
    settings = QSettings()
    current = current_version()
    version = pkg_resources.parse_version
    skipped = settings.value('startup/latest-skipped-version', "", type=str)
    if version(latest) <= version(current) or \
            latest == skipped:
        return

    from Orange.canvas.utils.overlay import NotificationWidget, NotificationOverlay
    from Orange.widgets import gui
    from AnyQt.QtGui import QIcon

    questionButtons = NotificationWidget.Ok | NotificationWidget.Close
    question = NotificationWidget(icon=QIcon(gui.resource_filename('icons/Dlg_down3.png')),
                                  title=UPDATE_AVAILABLE_TITLE,
                                  text='Current version: <b>{}</b><br>'
                                       'Latest version: <b>{}</b>'.format(current, latest),
                                  textFormat=Qt.RichText,
                                  standardButtons=questionButtons,
                                  acceptLabel="Download",
                                  rejectLabel="Skip this Version")

    def handle_click(b):
        if question.buttonRole(b) == question.RejectRole:
            settings.setValue('startup/latest-skipped-version', latest)
        if question.buttonRole(b) == question.AcceptRole:
            QDesktopServices.openUrl(QUrl(DOWNLOAD_URL))

    question.clicked.connect(handle_click)

    NotificationOverlay.registerNotification(question)


def compare_versions(latest):
    """
    NotificationWidget is new in Orange 3.22.0. Replace with
    compare_versions_notification when we are sure it is stable enough.
    """
    try:
        return compare_versions_notification(latest)
    except:
        return compare_versions_messagebox(latest)
