"""Native window cursors from the supplied three-frame sheet.

Keep native mouse delivery and Qt Quick hit testing; only replace the cursor
pixmap, so preview layers and drag gestures never intercept extra events.
"""
from PySide6.QtCore import QObject, QEvent, Qt, QRect, QSize
from PySide6.QtGui import QCursor, QImage, QPixmap

from .content import ROOT

# Tight alpha bounds in the source sheet, including the click rays.
# Hotspots refer to the finger tip (normal/click) or grip center (grab).
FRAMES = {
    'normal': (QRect(153, 176, 387, 594), (49, 15)),
    'grab': (QRect(669, 280, 407, 484), (155, 174)),
    'click': (QRect(1184, 92, 503, 676), (147, 151)),
}
CURSOR_SCALE = 48 / 676  # One shared scale avoids resizing the hand between states.


def cursor_images():
    sheet = QImage(str(ROOT / 'cursor/cursor_spritesheet.png'))
    if sheet.isNull():
        raise RuntimeError('Missing cursor/cursor_spritesheet.png')
    result = {}
    for name, (rect, hotspot) in FRAMES.items():
        size = QSize(round(rect.width() * CURSOR_SCALE), round(rect.height() * CURSOR_SCALE))
        image = sheet.copy(rect).scaled(size, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        result[name] = (image, tuple(round(v * CURSOR_SCALE) for v in hotspot))
    return result


class GameCursor(QObject):
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.cursors = {name: QCursor(QPixmap.fromImage(image), *hotspot)
                        for name, (image, hotspot) in cursor_images().items()}
        self.base = 'normal'
        self.variant = ''
        self.pressed = False
        self.updating = False
        window.installEventFilter(self)
        self.apply()

    def apply(self):
        self.variant = 'click' if self.pressed and self.base != 'grab' else self.base
        self.updating = True
        try:
            self.window.setCursor(self.cursors[self.variant])
        finally:
            self.updating = False

    def eventFilter(self, watched, event):
        if self.updating:
            return False
        kind = event.type()
        if kind == QEvent.CursorChange:
            shape = self.window.cursor().shape()
            if shape == Qt.BitmapCursor:
                return False
            if shape in (Qt.OpenHandCursor, Qt.ClosedHandCursor, Qt.DragMoveCursor):
                self.base = 'grab'
            elif shape == Qt.PointingHandCursor:
                self.base = 'click'
            else:
                self.base = 'normal'
            self.apply()
        elif kind == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
            self.pressed = True
            self.apply()
        elif kind == QEvent.MouseButtonRelease and event.button() == Qt.LeftButton:
            self.pressed = False
            self.apply()
        elif kind in (QEvent.Enter, QEvent.Leave):
            self.pressed = False
            self.apply()
        return False
