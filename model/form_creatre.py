import logging
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor, QMouseEvent
from PyQt5.QtWidgets import QGridLayout, QLabel

from views.client_create_form_view import Ui_Form


class ClientCreateForm(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.new_window = None
        self.ui = Ui_Form()
        self.ui.setupUi(self)
