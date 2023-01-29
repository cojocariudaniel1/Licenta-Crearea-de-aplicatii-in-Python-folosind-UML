import logging

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from base import Session
from client import Client
from account import Account
from views.client_create_form_view import Ui_Form


class ClientCreateForm(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.new_window = None
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # Default icon
        self.client_icon_image = QtGui.QPixmap("./sprites/img.png")
        self.client_icon_image_path = "./sprites/img.png"
        self.ui.image.setPixmap(self.client_icon_image.scaled(100, 100))
        self.ui.btn_upload_image.clicked.connect(self.upload_image)
        self.type_client = None
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
            self.ui.image.setPixmap(pixmap.scaled(100, 100))
            self.client_icon_image_path = fileName

    def add_client_to_database(self):
        try:
            if self.ui.rb_fizica.isChecked():
                type_client = "Fizica"
            elif self.ui.rb_juridica.isChecked():
                type_client = "Juridica"
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

            client = Client(type_client=type_client, name=name, street=street, street_number=street_number,
                            city=city, district=district, country=country, phone=phone, web_site=web_site, email=email,
                            zip_code=zip_code, image=image)

            session = Session()
            session.add(client)
            session.commit()
            session.close()

            QMessageBox.information(self, "Client adaugat", "Clientul a fost adaugat cu succes in baza de date")
        except BaseException as e:
            logging.exception(e)
