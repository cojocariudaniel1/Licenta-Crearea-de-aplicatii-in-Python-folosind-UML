import logging

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, QBuffer, QRect
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMessageBox, QFileDialog

from model.add_acount_form import AccountCreateForm
from model.custom_classes.custom_label_click import LabelClick
from model.custom_classes.custom_table_account import CustomTableAccount
from repository.customers_methods import save_customer, delete_customer, get_customer_by_id
from views.customer_edit_form import Ui_Form


class CustomerEditForm(QtWidgets.QWidget):
    window_closed = QtCore.pyqtSignal()
    def __init__(self, id_client):
        super().__init__()
        self.bank_acounts = []
        self.new_window = None
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.id_client = id_client
        self.client_icon_image_path = ""
        self.image_upload = False
        print(self.id_client)

        if self.id_client is not None:
            self.populate_data()
        self.ui.close_button.clicked.connect(self.close)
        self.ui.save_button.clicked.connect(self.save_button)
        self.ui.btn_upload_image.clicked.connect(self.upload_image)

        self.ui.btn_delete.clicked.connect(self.delete_client)
        self.account_tree_frame()
        self.add_account()
    def upload_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Upload a image", "",
                                                  "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if fileName:
            pixmap = QtGui.QPixmap(fileName)
            scaled_pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.ui.image.setPixmap(scaled_pixmap)
            self.client_icon_image_path = fileName



    def closeEvent(self, event):

        try:
            self.window_closed.emit()
            super().closeEvent(event)
        except BaseException as e:
            logging.exception(e)

    def save_button(self):
        try:
            if self.id_client is not None:
                name = self.ui.name_input.text()
                if self.ui.rb_fizica.isChecked():
                    type_client = "Fizica"
                else:
                    type_client = "Juridica"
                street = self.ui.street_input.text()
                street_number = self.ui.nr_street_input.text()
                city = self.ui.oras_input.text()
                district = self.ui.judet_input.text()
                country = self.ui.country_input.text()
                phone = self.ui.telefon_input.text()
                email = self.ui.email_input.text()
                zip_code = self.ui.zip_code_input.text()
                if self.image_upload:
                    with open(self.client_icon_image_path, "rb") as f:
                        image = f.read()
                else:
                    buffer = QBuffer()
                    buffer.open(QBuffer.ReadWrite)
                    self.ui.image.pixmap().save(buffer, "PNG")
                    image_binary_data = buffer.data()
                    image = image_binary_data
                save_customer(self.id_client, name, type_client, street, street_number, city, district, country, phone, email, zip_code, image)
                QMessageBox.information(self, "Client Modificat cu succes", "Datele au fost modificate cu succes si adaugate in baza de date")
                self.close()
        except BaseException as e:
            logging.exception(e)


    def account_tree_frame(self):
        try:

            self.tree2 = CustomTableAccount(self.ui.frame_accounting.x, self.ui.frame_accounting.y,
                                            self.ui.frame_accounting.width, self.ui.frame_accounting.height,
                                            self.ui.frame_accounting)
            header = [
                {"name": "Bank Name", "width": 300},
                {"name": "Account ID", "width": 300},
                {"name": "Send Money", "width": 285}
            ]
            self.tree2.header(header)

        except BaseException as e:
            logging.exception(e)


    def delete_client(self):
        delete_customer(self.id_client)

        QMessageBox.information(self, "Client Sters cu succes",
                                "Clientul a fost sters cu succes din baza de date")
        self.close()

    def populate_data(self):
        try:

            client = [get_customer_by_id(self.id_client)]

            for column in client:
                self.ui.name_input.setText(str(column.name))
                if column.type_client == "Fizica":
                    self.ui.rb_fizica.setChecked(True)
                else:
                    self.ui.rb_juridica.setChecked(True)
                self.ui.street_input.setText(str(column.adress.street))
                self.ui.nr_street_input.setText(str(column.adress.street_number))
                self.ui.oras_input.setText(str(column.adress.city))
                self.ui.judet_input.setText(str(column.adress.district))
                self.ui.country_input.setText(str(column.adress.country))
                self.ui.telefon_input.setText(str(column.adress.phone))
                self.ui.email_input.setText(str(column.adress.email))
                self.ui.zip_code_input.setText(str(column.adress.zip_code))

                binary_data = column.image
                qimage = QImage.fromData(binary_data, "PNG")
                pixmap = QPixmap.fromImage(qimage)
                scaled_pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.ui.image.setPixmap(scaled_pixmap)
        except BaseException as e:
            logging.exception(e)

    def add_bank(self, data):
        try:
            print(data)
            self.bank_acounts.append([len(self.bank_acounts), data])
            self.update_table()
        except BaseException as e:
            logging.exception(e)
    def open_add_acount(self):
        try:
            self.new_window = AccountCreateForm()
            self.new_window.show()
            self.new_window.save_signal.connect(self.add_bank)
        except BaseException as e:
            logging.exception(e)

    def update_table(self):
        self.tree2.deleteLater()
        self.account_tree_frame()
        self.tree2.populate_table(self.bank_acounts)
        self.tree2.show()

    def add_account(self):
        button_qlabel = LabelClick(self)
        button_qlabel.setText("+")
        button_qlabel.setGeometry(QRect(855, 495, 40, 40))
        button_qlabel.setStyleSheet("color: rgb(174, 120, 130); font-weight: bold; font-size: 20px")
        button_qlabel.clicked.connect(self.open_add_acount)
