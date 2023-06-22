import logging

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from model.add_acount_form import AccountCreateForm
from model.custom_classes.custom_label_click import LabelClick
from model.custom_classes.custom_table_account import CustomTableAccount
from views.create_client_view import Ui_CreateClientForm
from repository.customers_methods import create_customer


class CustomerCreateForm(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.tree2 = None
        self.new_window = None
        self.ui = Ui_CreateClientForm()
        self.ui.setupUi(self)
        self.bank_acounts = []
        # Default icon
        self.client_icon_image = QtGui.QPixmap("./images/default_icon_customer.png")
        self.client_icon_image_path = "./images/default_icon_customer.png"
        self.ui.image.setPixmap(self.client_icon_image.scaled(100, 100))
        self.ui.btn_upload_image.clicked.connect(self.upload_image)
        self.type_customer = None
        self.name = None
        self.street = None
        self.street_number = None
        self.city = None
        self.district = None
        self.country = None
        self.phone = None
        self.web_site = None
        self.email = None
        self.zip_code = None

        self.ui.save_button.clicked.connect(self.add_client_to_database)
        self.ui.close_button.clicked.connect(self.close_window)
        self.ui.frame_accounting.setStyleSheet('border: 1px gray')
        # self.tree = CustomTreeFrame(0, 10, 500, 200, ('button_icons', 'button_icons', 'button_icons'), self.ui.frame_accounting)

        # self.tree.hide()
        self.account_tree_frame()
        self.add_account()
        # self.ui.delete_accounting.clicked.connect(self.delete_account)

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

    def close_window(self):
        self.close()

    # Seteaza o imagine pentru client.
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

    def add_client_to_database(self):
        try:
            if self.ui.rb_fizica.isChecked():
                type_customer = "Fizica"
            elif self.ui.rb_juridica.isChecked():
                type_customer = "Juridica"
            else:
                QMessageBox.warning(self, f"Tip persoana neselectat",
                                    f"Selecteaza tipul de persoana: Fizica sau Juridica")
                return

            name = self.ui.name_input.text()
            street = self.ui.street_input.text()
            street_number = self.ui.nr_street_input.text()
            city = self.ui.oras_input.text()
            country = self.ui.country_input.text()
            district = self.ui.judet_input.text()
            zip_code = self.ui.zip_code_input.text()
            web_site = self.ui.web_site_input.text()
            phone = self.ui.telefon_input.text()
            email = self.ui.email_input.text()

            with open(self.client_icon_image_path, "rb") as f:
                image = f.read()

            if not all([name, street, street_number, city, district, country, zip_code]):
                QMessageBox.warning(self, f"Campuri necompletate", f"Completati toate campurile obligatorii")
                return

            create_customer(type_customer, name, street, street_number, city, district, country, phone, web_site, email,
                          zip_code, image, [])

            QMessageBox.information(self, "Client adaugat", "Clientul a fost adaugat cu succes in baza de date")
        except BaseException as e:
            logging.exception(e)

    def update_table(self):
        self.tree2.deleteLater()
        self.account_tree_frame()
        self.tree2.populate_table_products(self.bank_acounts)
        self.tree2.show()

    def add_account(self):
        button_qlabel = LabelClick(self)
        button_qlabel.setText("+")
        button_qlabel.setGeometry(QRect(855, 495, 40, 40))
        button_qlabel.setStyleSheet("color: rgb(174, 120, 130); font-weight: bold; font-size: 20px")
        button_qlabel.clicked.connect(self.open_add_acount)

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
