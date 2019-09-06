import time
from unittest.mock import patch, Mock, call

from AnyQt.QtCore import QSettings
from AnyQt.QtTest import QTest
from Orange.widgets.tests.base import GuiTest

import quasar.launcher.update_check as update_check


MODULE = "quasar.launcher.update_check"
NEWEST = "99999.0.0"


class TestUpdateCheck(GuiTest):

    @patch(MODULE + ".GetLatestVersion.version", return_value=NEWEST)
    @patch(MODULE + ".compare_versions")
    def test_versions_compared(self, mock_compare, mock_version):
        QSettings().setValue('startup/last-update-check-time', 0)
        t = update_check.check_for_updates()
        QTest.qWait(1)  # run signals
        self.assertEqual(mock_compare.call_args, call(NEWEST))
        if t:
            t.wait()

    @patch(MODULE + ".GetLatestVersion.version", return_value=NEWEST)
    @patch(MODULE + ".compare_versions")
    def test_versions_compared_recently(self, mock_compare, mock_version):
        QSettings().setValue('startup/last-update-check-time', int(time.time()))
        t = update_check.check_for_updates()
        QTest.qWait(1)  # run signals
        self.assertEqual(mock_compare.call_args, None)
        if t:
            t.wait()

    def test_old_messagebox(self):
        update_check.compare_versions_messagebox(NEWEST)

    @patch("Orange.canvas.notification_server_instance")
    def test_new_notification(self, _):
        with patch("Orange.canvas.notification_server_instance."
                   "registerNotification") as rn:
            update_check.compare_versions_notification(NEWEST)
            notification = rn.call_args[0][0]
            self.assertEqual(notification.title, "Quasar Update Available")
