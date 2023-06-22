from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import pyqtSignal
from model.custom_classes.custom_radio_button import CustomRadioButtonWidget
from views import add_bank_account_form
import sys

class AccountCreateForm(QtWidgets.QWidget):
    save_signal = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.new_window = None
        self.ui = add_bank_account_form.Ui_Dialog()
        self.ui.setupUi(self)

        font = QtGui.QFont("Arial", 11)
        font.setBold(True)

        self.ui.bank_name_header.setFont(font)
        self.ui.account_id_header.setFont(font)
        self.ui.send_money_header.setFont(font)

        self.ui.label.setObjectName("label1")
        self.ui.label.setStyleSheet("#label1 {background-color: rgb(239, 239, 239, 130);border: 1px solid gray;}")
        self.send_money_widget = CustomRadioButtonWidget(self.ui.label, 70, 6, True, True)
        self.send_money_widget.show()


        self.ui.save_btn.clicked.connect(self.save_button)
        self.ui.close_btn.clicked.connect(self.close)

    def save_button(self):
        data = [str(self.ui.bank_name_input.text()), str(self.ui.account_id_input.text()), self.send_money_widget.custom_radio_is_checked]
        print(data)
        self.save_signal.emit(data)
        self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    widget = AccountCreateForm()
    widget.show()
    sys.exit(app.exec_())