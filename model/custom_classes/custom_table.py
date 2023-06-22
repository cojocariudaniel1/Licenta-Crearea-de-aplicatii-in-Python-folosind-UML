import logging
import random
import sys

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, QEvent, QRect, QObject, pyqtSignal, QPoint
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFrame, QLabel, QLineEdit, QPushButton

from base import Session
from customer import CustomersTable
from model.custom_classes.custom_radio_button import CustomRadioButtonWidget
from repository.sales_methods import get_all_sales
from todoo import ExtendedComboBox
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


class HideUserInput(QObject):
    hide_user_input_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def eventFilter(self, obj, event):
        try:
            if event.type() == QEvent.MouseButtonPress:
                self.hide_user_input_signal.emit()
                return True
            return False
        except BaseException as e:
            logging.exception(e)


class RowEvent(QObject):
    def __init__(self, row, idx, parent=None):
        super().__init__(parent)
        self.row = row
        self.idx = idx

    def eventFilter(self, obj, event):
        try:
            if event.type() == QEvent.Enter:
                obj.setStyleSheet("#%s {background-color: #f1f1f1; ;border-bottom: 1px solid #e9ecef;}" % self.row)
                return True
            if event.type() == QEvent.Leave:
                if self.idx % 2 == 0:
                    obj.setStyleSheet("#%s {background-color: #fcfcfc ;border-bottom: 1px solid #e9ecef;} " % self.row)
                else:
                    obj.setStyleSheet("#%s {background-color: #ffffff ;border-bottom: 1px solid #e9ecef;} " % self.row)

                return True
            if event.type() == QEvent.MouseButtonPress:
                return True
            return False
        except BaseException as e:
            logging.exception(e)


class ClickableLabel(QObject):
    click_label_signal = pyqtSignal(str)

    def __init__(self, main_parent=None, parent=None):
        super().__init__(parent)
        self.main_parent = main_parent

    def eventFilter(self, obj, event):
        try:
            if event.type() == QEvent.MouseButtonPress:
                self.click_label_signal.emit(obj.objectName())
                return True

            return False
        except BaseException as e:
            logging.exception(e)


class EditableLabel(QObject):
    signal_edit_label = pyqtSignal(list)

    def __init__(self, main_parent=None, parent=None):
        super().__init__(parent)
        self.main_parent = main_parent

    def eventFilter(self, obj, event):
        try:
            if event.type() == QEvent.MouseButtonPress:
                self.signal_edit_label.emit(
                    [obj.text(), [obj.x(), obj.y(), obj.width(), obj.height()], self.main_parent, obj.objectName()])
                return True

            return False
        except BaseException as e:
            logging.exception(e)


class LabelEvent(QObject):
    end_of_line_signal = pyqtSignal(bool, int)

    def __init__(self, column, idx, parent=None):
        super().__init__(parent)
        self.idx = idx
        self.column = column

    def eventFilter(self, obj, event):
        try:
            if event.type() == QEvent.Enter:
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
    click_signal = pyqtSignal(str)

    def __init__(self, x, y, width, height, parent=None):
        super().__init__(parent)
        self.header_columns = []
        self.header_objects = []
        self.data = []
        self.data_id = []
        self.row_frames = []
        self.end_of_label_header = []
        self.edit_label_temp = None
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.setObjectName("table")
        self.default_height_row = 37
        # [1,37], [2, 37*2], [3,37*3]
        self.number_of_rows = [[1, self.default_height_row]]

        self.scroll_area = QtWidgets.QScrollArea(self)
        self.scroll_area.setObjectName("scroll_area")
        self.scroll_area.setGeometry(QRect(0, 0, self.width(), self.height()))
        self.scroll_widget = QtWidgets.QWidget()
        self.scroll_widget.setGeometry(0, 0, self.width(), self.height())
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_widget.setObjectName("scroll_widget")
        self.scroll_area.setStyleSheet("#scroll_area {background-color: white}")
        self.scroll_widget.setStyleSheet("#scroll_widget {background-color: white}")

        self.header_frame = QFrame(self.scroll_widget)
        self.header_frame.setObjectName("rowframe")
        self.header_frame.setGeometry(QRect(0, 0, self.width(), self.default_height_row))
        self.header_frame.setStyleSheet("#rowframe {background-color: #e9ecef;")
        # self.header_frame.installEventFilter(MyEventFilter(self.header_frame))
        self.header_span = 5
        self.setUpHeader()
        self.test = False

    def hide_user_input(self):
        if self.edit_label_temp is not None:
            self.edit_label_temp.hide()
            self.edit_label_temp = None

    def change_end_line_style(self, value, idx):
        try:
            if value:
                self.end_of_label_header[idx].setStyleSheet(
                    "background-color: #c1c4c7;border-bottom: 0.5px solid #e9ecef;")
            else:
                self.end_of_label_header[idx].setStyleSheet(
                    "background-color: #e9ecef;border-bottom: 0.5px solid gray;")
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

    def setUpTable(self):
        # self.data = [[]]
        if len(self.data) > 0:
            for row in self.data:
                if len(row) != len(self.header_columns):
                    logging.exception(msg="Data is not matching the header")
                    sys.exit()

    def QLabelHeader(self, name, x, y, width, height, idx):
        try:
            font = QtGui.QFont("Arial", 11)
            font.setBold(True)

            name_string = name.replace(" ", "")

            item = QLabel(f"{name}", self.header_frame)
            item.setObjectName(f"{name_string}")
            item.setGeometry(QRect(x, y, width, height))

            item.setStyleSheet("#%s {background-color: #e9ecef; border-bottom: 0.5px solid gray;}" % name_string)

            item.setAlignment(Qt.AlignCenter)
            item.setFont(font)

            label_end_line = QLabel(self.header_frame)
            label_end_line.setObjectName(f"{name}end_line")
            label_end_line.setGeometry(QRect(x + width - 3, y, 3, height, ))
            style1 = "background-color: #e9ecef; border-bottom: 0.5px solid gray;"
            label_end_line.setStyleSheet(style1)
            event = LabelEvent(name_string, idx, item)
            item.installEventFilter(event)
            event.end_of_line_signal.connect(self.change_end_line_style)
            self.end_of_label_header.append(label_end_line)

            return item
        except BaseException as e:
            logging.exception(e)

    def _QLabelRow(self, name, x, y, width, height, frame_row, idx):
        font = QtGui.QFont("Arial", 11)

        item = QLabel(str(name), frame_row)
        item.setObjectName(f"{name}")
        item.setGeometry(QRect(x, y, width, height))
        item.setAlignment(Qt.AlignCenter)
        item.setFont(font)

        return item

    def edit_label(self, value: list = None):
        if value:
            label_text = value[0]
            label_name = value[3]
            label_geometry = value[1]
            x, y, width, height = label_geometry
            main_parent = value[2]

            if self.edit_label_temp is not None:
                if self.edit_label_temp.objectName() != label_name:

                    for row in self.data:
                        for column in row:
                            if column.objectName() == self.edit_label_temp.objectName():
                                column.setText(self.edit_label_temp.text())

                self.edit_label_temp.hide()
                self.edit_label_temp = QLineEdit(f"{label_text}", main_parent)
                self.edit_label_temp.setObjectName(label_name)
                self.edit_label_temp.setGeometry(QRect(x, y, width, height))
                self.edit_label_temp.show()
                self.edit_label_temp.setFocus()

            else:
                self.edit_label_temp = QLineEdit(f"{label_text}", main_parent)
                self.edit_label_temp.setObjectName(label_name)
                self.edit_label_temp.setGeometry(QRect(x, y, width, height))
                self.edit_label_temp.show()
                self.edit_label_temp.setFocus()


        else:
            try:
                if self.edit_label_temp is not None:
                    for row in self.data:
                        for column in row:
                            if column.objectName() == self.edit_label_temp.objectName():
                                column.setText(self.edit_label_temp.text())
                    self.edit_label_temp.hide()
                self.edit_label_temp = None
            except BaseException as e:
                logging.exception(e)

    def _make_row(self, row, row_id):
        row_data = []
        last_id_of_row = self.number_of_rows[-1][0]
        current_row = [last_id_of_row + 1, last_id_of_row * self.default_height_row]
        self.number_of_rows.append(current_row)
        row_frame = QFrame(self.scroll_widget)
        row_frame.setObjectName(f"{row[0]}")
        row_frame.setGeometry(QRect(0, current_row[1], self.width(), self.default_height_row))
        row_frame.show()
        for idx, column in enumerate(row):
            if idx != 0:
                pos_x = 0
                for i in range(int(idx)):
                    pos_x += self.header_columns[i][1]
                if type(column) == CustomersTable:
                    k = self._QLabelRow(column.name, pos_x, 0, self.header_columns[idx][1],
                                        self.default_height_row, row_frame, idx)
                    k.setObjectName(str(row_id))
                    k.show()
                elif type(column) == bool:
                    k = CustomRadioButtonWidget(row_frame, pos_x, 8, True)
                    k.setObjectName(f"radio{row_id}")


                else:
                    k = self._QLabelRow(column, pos_x, 0, self.header_columns[idx][1],
                                        self.default_height_row, row_frame, idx)
                    k.setObjectName(str(row_id))
                row_data.append(k)
            else:
                k = self._QLabelRow(column, 0, 0, self.header_columns[idx][1], self.default_height_row,
                                    row_frame, idx)
                k.setObjectName(str(row_id))

                row_data.append(k)
        self.row_frames.append(row_frame)
        if last_id_of_row % 2 == 0:
            row_frame.setStyleSheet("#%s {background-color: #fcfcfc ;border-bottom: 1px solid #e9ecef;} " % row_id)

        else:
            row_frame.setStyleSheet("#%s {background-color: #ffffff; border-bottom: 1px solid #e9ecef;}" % row_id)
        row_frame.installEventFilter(RowEvent(row_id, last_id_of_row, row_frame))
        self.data.append(row_data)
        self.number_of_rows.append(current_row)

        event = ClickableLabel(self.scroll_widget, row_frame)
        row_frame.installEventFilter(event)
        event.click_label_signal.connect(self.open_sale)

    def open_sale(self, sale_nr):
        self.click_signal.emit(sale_nr)

    def add_row(self, row, row_id):
        if len(row) != 0:
            if len(row) != len(self.header_columns):
                logging.exception(msg="Data and columns don't match")
                sys.exit()
            else:
                self._make_row(row, row_id)
        else:
            logging.exception(msg="Incorect Data : len is 0")
            sys.exit()

    def populate_table(self, data):
        self.scroll_widget.setGeometry(0, 0, self.width(), (len(data) + 1) * self.default_height_row)
        for row in data:
            self.data_id.append(row[0])
            self.add_row(row[1], row[0])

    def print_data(self):
        print(self.data_id)

    def setUpHeader(self):
        # column[0] -> name of the column, column[1] -> width of the column
        try:
            if len(self.header_columns) > 0:

                for idx, column in enumerate(self.header_columns):
                    if idx != 0:
                        x_pos = 0
                        for i in range(int(idx)):
                            x_pos += self.header_columns[i][1]

                        item = self.QLabelHeader(column[0], x_pos, 0, column[1], self.default_height_row, idx)
                        self.header_objects.append({"idx": idx, "obj": item, "event": None})

                    else:
                        item = self.QLabelHeader(column[0], 0, 0, column[1], self.default_height_row, idx)
                        self.header_objects.append({"idx": idx, "obj": item, "event": None})

        except BaseException as e:
            logging.exception(e)
