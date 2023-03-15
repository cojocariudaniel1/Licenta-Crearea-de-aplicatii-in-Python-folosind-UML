from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLabel


class LabelClick(QLabel):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        QLabel.__init__(self, parent=parent)

    def mousePressEvent(self, event):
        self.clicked.emit()



