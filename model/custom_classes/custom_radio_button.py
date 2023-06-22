from PyQt5 import QtWidgets, QtCore, Qt as Qt_timer
from PyQt5.QtWidgets import QLabel


class CustomRadioButton(QtWidgets.QRadioButton):
    on = QtCore.pyqtSignal()
    off = QtCore.pyqtSignal()
    return_value = QtCore.pyqtSignal(bool)

    def __init__(self, parent, x, y):
        super().__init__(parent)
        self.default_x = x + 4
        self.default_y = y + 1
        self.x_pos = x
        self.default_width = 30
        self.default_height = 30
        self.setGeometry(self.default_x, self.default_y - 5, self.default_width, self.default_height)
        self.timer1 = Qt_timer.QTimer(self)
        self.count = 0
        self.clicked.connect(self.timer)

    def timer(self):
        self.setDisabled(True)  # seteaza butonul radio ca fiind dezactivat

        self.return_value.emit(self.isChecked())
        self.timer1.timeout.connect(self.showTime)
        self.timer1.start(1)

    def showTime(self):
        if self.isChecked():
            if self.x_pos >= self.default_x + 14:  # a ajuns la capatul dreapta
                self.timer1.stop()
                self.x_pos = self.default_x + 14
                self.setDisabled(False)  # seteaza butonul radio ca fiind activat din nou
                self.on.emit()
                # self.setStyleSheet(
                #     "background-color: rgba(0, 168, 252, 100);border: 1px solid rgb(224,224,224, 220); border-radius: 10px;")
            else:
                self.x_pos += 1
                self.setGeometry(self.x_pos, self.default_y, 45, 20)

        else:
            if self.x_pos <= self.default_x:  # a ajuns la capatul stanga
                self.timer1.stop()
                self.x_pos = self.default_x
                self.off.emit()
                self.setDisabled(False)  # seteaza butonul radio ca fiind activat din nou


            else:
                self.x_pos -= 1
                self.setGeometry(self.x_pos, self.default_y, 45, 20)


class CustomRadioButtonWidget(QLabel):
    # For creating a Custom
    def __init__(self, parent, x, y, state=False, p = False):
        super().__init__(parent)

        self.custom_radio_is_checked = state
        self.default_x_pos = x
        self.default_y_pos = y
        self.x_pos = x

        self.custom_radioButton = CustomRadioButton(parent, self.default_x_pos, self.default_y_pos)
        self.custom_radioButton.on.connect(self.radio_button_on)
        self.custom_radioButton.off.connect(self.radio_button_off)
        self.custom_radioButton.show()
        self.custom_radioButton.setObjectName("RB")

        if p:
            self.custom_radioButton.setStyleSheet("#RB {background-color: rgba(255, 255, 255, 0)}")
        self.custom_radioButton.return_value.connect(self.radioBtn_is_checked)
        self.setObjectName("LabelRB")
        self.setStyleSheet(
            "#LabelRB {background-color: rgba(255, 255, 255);border: 1px solid rgb(224,224,224, 220); border-radius: 10px;}")
        self.setGeometry(self.default_x_pos, self.default_y_pos, 37, 20)
        self.set_radio_button(self.custom_radio_is_checked)

    def set_radio_button(self, state):
        if state:
            self.custom_radio_is_checked = state
            self.custom_radioButton.setChecked(True)
            self.custom_radioButton.timer()
        else:
            self.custom_radio_is_checked = state
            self.custom_radioButton.setChecked(False)
            self.custom_radioButton.timer()

    def radio_button_on(self):
        self.setStyleSheet(
            "background-color: rgba(0, 168, 252, 100);border: 1px solid rgb(224,224,224, 220); border-radius: 10px;")

    def radio_button_off(self):
        self.setStyleSheet(
            "background-color: rgba(255, 255, 255);border: 1px solid rgb(224,224,224, 220); border-radius: 10px;")

    def radioBtn_is_checked(self, checked):
        if checked:
            self.custom_radio_is_checked = True
        else:
            self.custom_radio_is_checked = False


