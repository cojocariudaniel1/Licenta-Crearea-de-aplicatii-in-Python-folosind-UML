import logging
import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, pyqtSignal, QEvent, QRect
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFrame, QLabel, QLineEdit, QPushButton

from base import Session
from model.custom_classes.custom_radio_button import CustomRadioButtonWidget

app = QtWidgets.QApplication(sys.argv)

class CostumRowFrame(QFrame):
    emit_last_row = QtCore.pyqtSignal()
    delete_row = QtCore.pyqtSignal()

    def __init__(self, data, parent=None):
        super(CostumRowFrame, self).__init__(parent)

        try:
            self.data = data
            self.edit_window = None

            self.clicked = False

            # Set the frame properties
            self.setFixedSize(800, 30)
            # Add the labels to the row
            self.installEventFilter(self)

            self.id_account = data[0]
            self.setObjectName("rowframe")
            self.setStyleSheet("#rowframe {background-color: rgb(255, 255, 255); border-bottom: 0.5px solid gray; }")

            self.bank_label = QtWidgets.QLabel(data[1], self)
            self.bank_label.setGeometry(10, 5, 100, 20)
            self.bank_label.setStyleSheet('font: 11pt "MS Shell Dlg 2";')

            self.account_label = QtWidgets.QLabel(data[2], self)
            self.account_label.setGeometry(170, 5, 100, 20)
            self.account_label.setStyleSheet('font: 11pt "MS Shell Dlg 2";')

            self.send_money_label = CustomRadioButtonWidget(self, 330, 5)
            self.send_money_label.set_radio_button(data[3])

            self.ddd = QtWidgets.QLabel(self)
            self.ddd.setPixmap(QPixmap("sprites/dd.png").scaled(15, 20))
            self.ddd.setGeometry(450, 0, 30, 30)
            self.ddd.enterEvent = self.enterEventBin
            self.ddd.leaveEvent = self.leaveEventBin
            self.ddd.mousePressEvent = self.mousePressEventBin
        except BaseException as e:
            logging.exception(e)

    def mousePressEventBin(self, event):
        super().mousePressEvent(event)
        self.delete_row.emit()

    def enterEventBin(self, event):
        super().enterEvent(event)
        self.setCursor(QtCore.Qt.PointingHandCursor)

    def leaveEventBin(self, event):
        super().leaveEvent(event)
        self.unsetCursor()

    def open_edit_window(self):

        try:
            font = 'font: 11pt "MS Shell Dlg 2";'
            button_stlye = ("background-color: rgb(174, 139, 137);\n"
                            "color: rgb(255, 255, 255);\n"
                            "font: 75 14pt \"MS Shell Dlg 2\";")
            self.edit_window = QFrame()
            self.edit_window.setWindowTitle("Edit row")
            self.edit_window.setGeometry(QRect(500, 200, 600, 150))

            bank_header = QLabel("Bank Name", self.edit_window)
            account_number_header = QLabel("Account Number", self.edit_window)
            send_money_header = QLabel("Send Money", self.edit_window)

            bank_header.setStyleSheet(font)
            account_number_header.setStyleSheet(font)
            send_money_header.setStyleSheet(font)

            bank_header.setGeometry(QRect(80, 20, 150, 20))
            account_number_header.setGeometry(QRect(230, 20, 150, 20))
            send_money_header.setGeometry(QRect(380, 20, 150, 20))

            bank_input = QLineEdit(self.edit_window)
            bank_input.setText(self.bank_label.text())
            bank_input.setStyleSheet(font)
            bank_input.setGeometry(QRect(80, 45, 120, 20))

            account_number_input = QLineEdit(self.edit_window)
            account_number_input.setText(self.account_label.text())
            account_number_input.setStyleSheet(font)
            account_number_input.setGeometry(QRect(230, 45, 120, 20))

            send_money_widget = CustomRadioButtonWidget(self.edit_window, 380, 45)
            send_money_widget.set_radio_button(self.send_money_label.custom_radio_is_checked)

            send_money_widget.show()



            button_save = QPushButton("Save", self.edit_window)
            button_save.setStyleSheet(button_stlye)
            button_save.setGeometry(QRect(175, 90, 115, 35))

            button_close = QPushButton("Close", self.edit_window)
            button_close.setStyleSheet(button_stlye)
            button_close.setGeometry(QRect(300, 90, 115, 35))


            self.edit_window.show()
            def save_edit_window():
                self.bank_label.setText(str(bank_input.text()))
                self.account_label.setText(str(account_number_input.text()))
                self.send_money_label.set_radio_button(send_money_widget.custom_radio_is_checked)
                self.edit_window.deleteLater()

            def close_edit_window():
                self.edit_window.deleteLater()

            button_save.clicked.connect(save_edit_window)
            button_close.clicked.connect(close_edit_window)
        except BaseException as e:
            logging.exception(e)



    def eventFilter(self, object, event):
        try:
            if event.type() == QEvent.Enter:
                # acțiunea care se va executa la hover
                self.setStyleSheet("#rowframe {background-color: rgb(207, 207, 207);border-bottom: 0.5x solid gray; }")
            if event.type() == QEvent.Leave:
                if not self.clicked:
                    self.setStyleSheet(
                        "#rowframe {background-color: rgb(255, 255, 255); border-bottom: 0.5px solid gray;}")
            if event.type() == QEvent.MouseButtonPress:
                self.clicked = True
                self.setStyleSheet("#rowframe {background-color: rgb(207, 207, 207);border-bottom: 0.5x solid gray; }")
                self.emit_last_row.emit()
            if event.type() == QEvent.MouseButtonDblClick:
                self.open_edit_window()
            return super().eventFilter(object, event)
        except BaseException as e:
            logging.exception(e)


class CustomTreeFrame(QFrame):
    rows = []

    def __init__(self, x, y, width, height, _header, parent=None):
        super().__init__(parent)
        self.last_selected_row = None
        self.parent = parent
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.header = _header
        self.setObjectName("main_frame")
        self.setStyleSheet("#main_frame {background-color: white}")
        self.setGeometry(x, y, 1000, 600)

        self.button = QPushButton("test", self)
        self.button.setGeometry(0,0, 100, 50)
        self.number_of_rows = 8

        self.scroll_area = QtWidgets.QScrollArea(self)
        self.scroll_area.setGeometry(50, 100, 502, 300)

        # Add a widget to the scrollable area
        self.scroll_widget = QtWidgets.QWidget()

        for i in range(self.number_of_rows):
            row_data = [i, "Bank {}".format(i), str(10000 + i), i % 2 == 0]
            self.rows.append(row_data)
        self.scroll_widget.setGeometry(0, 0, 500, self.number_of_rows * 30)

        # Set the widget as the scrollable area's content widget
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_widget.setObjectName("scroll_area")
        self.scroll_widget.setStyleSheet("#scroll_area {background-color: white}")

        self.setMouseTracking(True)
        self.make_header(self.header)
        self.row_frames = []
        self.generate_data()

        self.draw_tree()
        self.button.clicked.connect(self.add_row)

    def delete_row_handler(self):
        sender = self.sender()
        for row_frame in self.row_frames:
            if row_frame is sender:
                self.row_frames.remove(row_frame)
                row_frame.deleteLater()
                self.draw_tree()

    def add_row(self):
        row_frame = CostumRowFrame([1, 'ddd', '1001', 0], self.scroll_widget)
        self.row_frames.append(row_frame)
        self.scroll_widget.setGeometry(self.scroll_widget.x(), self.scroll_widget.y(), self.scroll_widget.width(), self.scroll_widget.height() + 30)
        print(self.row_frames)
        self.draw_tree()

    def generate_data(self):
        for i in range(self.number_of_rows):
            row_data = [i, "Bank {}".format(i), str(10000 + i), i % 2 == 0]
            row_frame = CostumRowFrame(row_data, self.scroll_widget)
            print(row_frame.id_account)
            row_frame.hide()
            self.row_frames.append(row_frame)



    def row_clicked_handler(self):
        sender = self.sender()
        for row_frame in self.row_frames:
            if row_frame is not sender:
                row_frame.setStyleSheet(
                    "#rowframe {background-color: rgb(255, 255, 255); border-bottom: 0.5px solid gray;}")
                row_frame.clicked = False
            else:

                row_frame.setStyleSheet(
                    "#rowframe {background-color: rgb(220, 220, 220);border-bottom: 0.5x solid gray; }")


    def draw_tree(self):
        for i, frame in enumerate(self.row_frames):
            frame.move(0, i * 30)
            frame.emit_last_row.connect(self.row_clicked_handler)
            frame.delete_row.connect(self.delete_row_handler)
            frame.show()

    def make_header(self, _header):
        bank = QLabel(_header[0], self)
        bank.setStyleSheet('font: 11pt "MS Shell Dlg 2";')
        bank.setGeometry(85, 0, 100, 30)

        account_number = QLabel(_header[1], self)
        account_number.setStyleSheet('font: 11pt "MS Shell Dlg 2";')
        account_number.setGeometry(250, 0, 200, 30)


if __name__ == "__main__":
    header = ("Bank", "Account Number", "Send Money")

    frame1 = CustomTreeFrame(50, 50, 500, 200, header)
    frame1.show()


    # add the frame to a scroll area

    sys.exit(app.exec_())
