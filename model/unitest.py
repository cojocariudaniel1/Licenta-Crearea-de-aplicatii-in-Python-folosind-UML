import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel

app = QApplication(sys.argv)
w = QWidget()
glay = QGridLayout(w)
glay.addWidget(QLabel("1"), 0, 0)
glay.addWidget(QLabel("2"), 0, 1, 1, 3)
glay.addWidget(QLabel("3"), 1, 0, 1, 2)
glay.addWidget(QLabel("4"), 1, 2, 1, 2)

qsrand(QTime.currentTime().msec())

for label in w.findChildren(QLabel):
    color = QColor(qrand() % 256, qrand() % 256, qrand() % 256)
    label.setStyleSheet('.QLabel{{background: rgb({}, {}, {});}}'.format(color.red(), color.green(), color.blue()))

w.show()
sys.exit(app.exec_())