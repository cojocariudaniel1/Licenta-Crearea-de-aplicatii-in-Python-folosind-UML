import logging
import sys

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, QEvent, QRect, QObject, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFrame, QLabel, QLineEdit, QPushButton

from base import Session
from model.custom_classes.custom_radio_button import CustomRadioButtonWidget
from views.sales_view import Ui_Form
import qtmodern.styles
import qtmodern.windows

"""
item header =
{
    "name": value -> string,
    "sortable": value -> bool,
    "width": valeu -> int (pixels)
    ""
}

With the widht of value all column values wiill have the same width
                
"""
class LabelEvent(QObject):
    end_of_line_signal = pyqtSignal(bool, int)
    def __init__(self, column, idx, parent=None):
        super().__init__(parent)
        self.idx = idx
        self.column = column

    def eventFilter(self, obj, event):
        try:
            if event.type() == QEvent.Enter:
                print(obj.objectName())
                # acțiunea care se va executa la hover
                obj.setStyleSheet("#%s {background-color: #dde0e3;border-bottom: 0.5x solid gray; }" % self.column)
                self.end_of_line_signal.emit(True, self.idx)

                return True
            if event.type() == QEvent.Leave:
                obj.setStyleSheet(
                    "#%s {background-color: #e9ecef; border-bottom: 0.5px solid gray;}" % self.column)
                self.end_of_line_signal.emit(False, self.idx)
                return True
            return False
        except BaseException as e:
            logging.exception(e)


class CustomTable(QFrame):

    def __init__(self, x, y, width, height, parent=None):
        super().__init__(parent)
        self.header_columns = []
        self.data = []
        self.end_of_label_header = []


        self.width = width
        self.height = height
        self.x = x
        self.y = y

        self.default_height_row = 50

        self.header_frame = QFrame(self)
        self.header_frame.setObjectName("rowframe")
        self.header_frame.setGeometry(QRect(0, 0, self.width(), self.default_height_row))
        self.header_frame.setStyleSheet("background-color: #e9ecef")
        # self.header_frame.installEventFilter(MyEventFilter(self.header_frame))
        self.header_span = 5
        self.setUpHeader()

    def QLabelHeader(self, name, x, y, width, height, idx):
        try:
            item = QLabel(f"{name}", self.header_frame)
            item.setObjectName(f"{name}")
            item.setGeometry(QRect(x, y, width, height))
            item.setAlignment(Qt.AlignCenter)

            # font = QtGui.QFont("Lucida Bright", 14)
            # sorting_label = QLabel("\u2191", item)
            # sorting_label.setGeometry(QRect(x+ 30, y, 45, height))
            # sorting_label.setAlignment(QtCore.Qt.AlignCenter)
            # sorting_label.setFont(font)


            label_end_line = QLabel(self.header_frame)
            label_end_line.setObjectName(f"{name}end_line")
            label_end_line.setGeometry(QRect(x + width -3, y, 3, height,))
            style1 = "background-color: black"
            label_end_line.setStyleSheet(style1)
            event = LabelEvent(name, idx, item)
            item.installEventFilter(event)
            event.end_of_line_signal.connect(self.change_end_line_style)
            self.end_of_label_header.append(label_end_line)
        except BaseException as e:
            logging.exception(e)

    def change_end_line_style(self, value, idx):
        try:
            if value:
                self.end_of_label_header[idx].setStyleSheet("background-color: #c1c4c7;border-bottom: 0.5px solid #c1c4c7;")
            else:
                self.end_of_label_header[idx].setStyleSheet("background-color: #e9ecef;border-bottom: 0.5px solid gray;")
        except BaseException as e:
            logging.exception(e)

    """ column [0] idx , [1] name"""
    def header(self, _header: list):
        try:
            countinue = True
            for element in _header:
                if len(element) != 2:
                    logging.exception(msg="Format of the Header is incorect eg: name: value, width: value")
                else:
                    try:
                        k = element["name"]
                        j = element["width"]
                    except BaseException as e:
                        countinue = False
                        logging.exception(e)

            if countinue:
                for idx, item in enumerate(_header):
                    self.header_columns.append([item["name"], item["width"]])
                self.setUpHeader()
        except BaseException as e:
            logging.exception(e)

    def add_item(self):
        pass

    def setUpTable(self):
        pass

    def setUpHeader(self):
        # column[0] -> name of the column, column[1] -> width of the column
        try:
            if len(self.header_columns) > 0:

                for idx, column in enumerate(self.header_columns):
                    if idx != 0:
                        x_pos = 0
                        for i in range(int(idx)):
                            x_pos += self.header_columns[i][1]
                        print(x_pos)
                        self.QLabelHeader(column[0], x_pos, 0, column[1], self.default_height_row, idx)
                    else:
                        self.QLabelHeader(column[0], 0, 0, column[1], self.default_height_row, idx)
        except BaseException as e:
            logging.exception(e)


class SalesForm(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.new_window = None
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.tableView = CustomTable(self.ui.sales_view_layout.x, self.ui.sales_view_layout.y,
                                     self.ui.sales_view_layout.width, self.ui.sales_view_layout.width,
                                     self.ui.sales_view_layout)
        self.tableView.setObjectName("tableView")
        header_list = [
            {"name": "Number", "width": 200},
            {"name": "Customer", "width": 150},
            {"name": "Customer", "width": 150},
            {"name": "Customer", "width": 150},

        ]
        self.tableView.header(header_list)


if __name__ == "__main__":
    try:
        app = QtWidgets.QApplication(sys.argv)
        qtmodern.styles.light(app)
        widget = SalesForm()
        widget.show()
    except BaseException as e:
        logging.exception(e)

    # add the frame to a scroll area

    sys.exit(app.exec_())
