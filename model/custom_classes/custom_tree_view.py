import logging

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, Qt, QEvent
from PyQt5.QtWidgets import QLineEdit, QFrame

from bankaccount import BankAccount
from base import Session
from model.custom_classes.custom_radio_button import CustomRadioButtonWidget


class EditableLabel(QtWidgets.QLabel):
    change = pyqtSignal()

    def __init__(self, text, parent, row_id, column_id):
        super().__init__(parent)
        self.column = column_id
        self.row_id = row_id
        self.setText(text)

        self.setAlignment(Qt.AlignCenter)

    def mouseDoubleClickEvent(self, event):
        line_edit = QLineEdit(self.text(), self)
        print(self.text())

        self.setText("")
        if self.column == 0:
            line_edit.setGeometry(self.geometry().x() + 15, self.geometry().y() - 3, self.geometry().width(),
                                  self.geometry().height())
            print(self.geometry(), self.column)

        elif self.column == 1:
            line_edit.setGeometry(0, 3, 100, 27)
            print(self.geometry(), self.column)
        line_edit.selectAll()
        # line_edit.setFrame(False)

        line_edit.editingFinished.connect(self.finish_edit)
        line_edit.setFocus()
        line_edit.show()

    def finish_edit(self):
        sender = self.sender()
        self.setText(sender.text())
        sender.deleteLater()
        self.show()
        self.line_edit_text_changed()

    def line_edit_text_changed(self):
        session = Session()
        session.close()


class CostumRowFrame(QFrame):
    def __init__(self, id_frame, bank, account_number, send_money, widget_parent_width):
        super().__init__()
        self.send_money_radio_button = None
        self.label_bank = None
        self.label_account_number = None
        self.check_box = None
        self.id_frame = id_frame
        self.bank = bank
        self.account_number = account_number
        self.send_money = send_money
        self.setMinimumHeight(30)
        self.setMaximumHeight(30)
        self.check = False
        self.click = False
        self.widget_parent_width = widget_parent_width

        self.row_number = id_frame

        # Bank rect.
        self.default_column_height = 30
        self.bank_width = 155
        self.account_number_width = 120
        self.setObjectName("rowframe")
        if id_frame:
            self.set_pozition_row()
        self.default_y = 0

    def set_pozition_row(self):
        default_y = self.row_number * 30
        self.installEventFilter(self)
        self.setStyleSheet("#rowframe {background-color: rgb(255, 255, 255);}")

        self.columns()

    def default_column(self):

        label_bank = EditableLabel(str("Bank Name"), self, self.id_frame, 0)
        label_bank.setGeometry(30, 3, self.bank_width, 27)
        label_bank.setStyleSheet('font: 11pt "MS Shell Dlg 2";')
        label_bank.show()

        label_account_number = EditableLabel(str("Account number"), self, self.id_frame, 1)
        label_account_number.setGeometry(200 + 20, 3, 150, 27)
        label_account_number.setStyleSheet('font: 11pt "MS Shell Dlg 2";')
        label_account_number.show()

        send_money = CustomRadioButtonWidget(self, 420, 5, False)
        send_money.show()

    def change_check_box(self):
        if self.check:
            self.check = False
        else:
            self.check = True

    def columns(self):
        self.check_box = QtWidgets.QCheckBox(self)
        self.check_box.setGeometry(15, 8, 20, 20)
        self.check_box.stateChanged.connect(self.change_check_box)

        self.label_bank = EditableLabel(str(self.bank), self, self.id_frame, 0, )
        self.label_bank.setGeometry(40, 3, self.bank_width, 27)
        self.label_bank.setStyleSheet('font: 11pt "MS Shell Dlg 2";')

        self.label_account_number = EditableLabel(str("Account number"), self, self.id_frame, 1)
        self.label_account_number.setAlignment(Qt.AlignLeft)
        self.label_account_number.setGeometry(200 + 20, 3, self.account_number_width, 27)
        self.label_account_number.setStyleSheet('font: 11pt "MS Shell Dlg 2";')

        self.send_money_radio_button = CustomRadioButtonWidget(self, 420, 5, self.send_money)

    def eventFilter(self, object, event):
        if event.type() == QEvent.Enter:
            # acțiunea care se va executa la hover
            self.setStyleSheet("#rowframe {background-color: rgb(207, 207, 207);}")
        if event.type() == QEvent.Leave:
            if not self.click:
                self.setStyleSheet("#rowframe {background-color: rgb(255, 255, 255);}")
        if event.type() == QEvent.MouseButtonPress:
            self.click = True
            self.setStyleSheet("#rowframe {background-color: rgb(207, 207, 207);}")

        return super().eventFilter(object, event)


class CustomTreeFrame(QFrame):
    rows = []

    def __init__(self, x, y, width, height, _header, parent=None):
        super().__init__(parent)
        try:
            self.width = width
            self.height = height
            self.x = x
            self.y = y
            self.header = _header
            self.setObjectName("main_frame")
            self.setStyleSheet("#main_frame {background-color: green}")
            self.setGeometry(x + 2, y, width, 300)

            self.scroll_area = QtWidgets.QScrollArea(self)
            self.scroll_area.setGeometry(x, y - 10, width, 200)
            self.scroll_area.setWidgetResizable(True)

            self.central_widget = QtWidgets.QWidget()
            layout = QtWidgets.QVBoxLayout()
            layout.setSpacing(0)
            self.central_widget.setLayout(layout)

            self.scroll_area.setWidget(self.central_widget)
            self.central_widget.layout().setContentsMargins(0, 0, 0, 0)
            self.scroll_area.setContentsMargins(0, 0, 0, 0)

            self.setMouseTracking(True)
            self.draw_tree()
        except BaseException as e:
            logging.exception(e)

    def draw_tree(self):
        try:
            session = Session()
            account = session.query(BankAccount).all()
            self.rows.clear()

            for j in account:
                row = CostumRowFrame(j.id, {j.bank}, j.account_number,
                                     j.send_money,
                                     self.width)
                self.rows.append(row)
                self.central_widget.layout().addWidget(row)
        except BaseException as e:
            logging.exception(e)
