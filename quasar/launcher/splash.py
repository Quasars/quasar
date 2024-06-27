import pkg_resources
from AnyQt.QtCore import QCoreApplication, QPoint, Qt, QRect
from AnyQt.QtGui import QPixmap, QFont, QFontMetrics, QPainter, QColor


def splash_screen():
    """
    """
    pm = QPixmap(
        pkg_resources.resource_filename(
            __name__, "icons/splash.png")
    )

    version = QCoreApplication.applicationVersion()
    size = 21 if len(version) < 6 else 16
    font = QFont("Arial")
    font.setPixelSize(size)
    metrics = QFontMetrics(font)
    br = metrics.boundingRect(version).adjusted(-5, 0, 5, 0)
    br.moveBottomLeft(QPoint(216, 82))

    p = QPainter(pm)
    p.setRenderHint(QPainter.Antialiasing)
    p.setRenderHint(QPainter.TextAntialiasing)
    p.setFont(font)
    p.setPen(QColor("#ff6d00"))
    p.drawText(br, Qt.AlignCenter, version)
    p.end()
    return pm, QRect(60, 101, 250, 328)
