import logging

from PyQt5 import QtCore
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QTreeWidget, QFrame, QLabel

from model.form_edit_client_model import ClientEditForm

FRAME_LIST = []


class LabelClick(QLabel):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        QLabel.__init__(self, parent=parent)

    def mousePressEvent(self, event):
        self.clicked.emit()


class CustomFrame(QFrame):
    window_closed_2 = QtCore.pyqtSignal()

    def __init__(self, index):
        super().__init__()
        self.new_window = None
        self.index = index
        self.selected = False

        # Set default stylesheet
        self.setStyleSheet("background-color: rgb(249,249,249); border: 1px solid rgb(249,249,249);")

        # Connect the doubleClickEvent
        self.mousePressEvent = self.mousePressEvent
        self.mouseDoubleClickEvent = self.mouseDoubleClickEvent

    def mouseDoubleClickEvent(self, event):
        try:
            if self.index > 0:
                self.new_window = ClientEditForm(self.index)
                self.new_window.window_closed.connect(self.clientEditFormClosed)
                self.new_window.show()
        except BaseException as e:
            print(e)

    def clientEditFormClosed(self):
        try:
            self.window_closed_2.emit()
            print('test1')
        except BaseException as e:
            logging.exception(e)

    def mousePressEvent(self, event):
        # Change the stylesheet of all frames to default

        try:
            if self.index >= 0:
                for frame in FRAME_LIST:
                    if frame.index >= 0:
                        frame.setStyleSheet("background-color: rgb(249,249,249); border: 1px solid rgb(249,249,249);")
                        frame.selected = False

                # Change the stylesheet of the selected frame
                self.setStyleSheet("background-color: #F9F9F9; border: 1px solid #ae8b89;")
                self.selected = True
                layout = self.layout()
                for i in range(layout.count()):
                    child = layout.itemAt(i).widget()
                    child.setStyleSheet("background-color: rgb(249,249,249); border: 1px solid rgb(249,249,249);")
        except RuntimeError:
            pass


class CustomQTreeWidgetSortingModified(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.order = 0
        try:
            horizontalHeaders = self.header()
            horizontalHeaders.setSectionsClickable(True)
            horizontalHeaders.sectionClicked.connect(self.sortItems)
        except Exception as e:
            logging.exception(e)

    def sortItems(self, column, order=Qt.AscendingOrder):
        try:
            if self.headerItem().text(column) == "Id":
                int_values = []
                mapping = {}
                for i in range(self.topLevelItemCount()):
                    item = self.topLevelItem(i)
                    int_value = int(item.text(column))
                    int_values.append(int_value)
                    mapping[int_value] = item

                int_values.sort()
                if self.order == 0:
                    self.order = 1
                    int_values.reverse()
                else:
                    self.order = 0
                    int_values.sort()

                for i, value in enumerate(int_values):
                    item = mapping[value]
                    self.takeTopLevelItem(self.indexOfTopLevelItem(item))
                    self.insertTopLevelItem(i, item)
            else:
                if self.order == 0:
                    self.order = 1
                    super().sortItems(column, Qt.DescendingOrder)
                else:
                    self.order = 0
                    super().sortItems(column, Qt.AscendingOrder)
        except BaseException as e:
            logging.exception(e)
