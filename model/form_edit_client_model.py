import io
import logging

from PIL import Image
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, QBuffer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMessageBox, QFileDialog

from base import Session
from client import Client
from views.form_edit import Ui_Form


class ClientEditForm(QtWidgets.QWidget):
    window_closed = QtCore.pyqtSignal()
    def __init__(self, id_client):
        super().__init__()
        self.new_window = None
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.id_client = id_client
        self.client_icon_image_path = ""
        self.image_upload = False


        if self.id_client is not None:
            self.populate_data()
        self.ui.close_button.clicked.connect(self.close)
        self.ui.save_button.clicked.connect(self.save_button)
        self.ui.btn_upload_image.clicked.connect(self.upload_image)

        self.ui.btn_delete.clicked.connect(self.delete_client)

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
                session = Session()
                client = session.query(Client).filter(Client.id == self.id_client).first()

                client.name = self.ui.name_input.text()
                if self.ui.rb_fizica.isChecked():
                    client.type_client = "Fizica"
                else:
                    client.type_client = "Juridica"
                client.street = self.ui.street_input.text()
                client.street_number = self.ui.nr_street_input.text()
                client.city = self.ui.oras_input.text()
                client.district = self.ui.judet_input.text()
                client.country = self.ui.country_input.text()
                client.phone = self.ui.telefon_input.text()
                client.email = self.ui.email_input.text()
                client.zip_code = self.ui.zip_code_input.text()
                if self.image_upload:
                    with open(self.client_icon_image_path, "rb") as f:
                        client.image = f.read()
                else:
                    buffer = QBuffer()
                    buffer.open(QBuffer.ReadWrite)
                    self.ui.image.pixmap().save(buffer, "PNG")
                    image_binary_data = buffer.data()
                    client.image = image_binary_data
                session.commit()
                session.close()
                QMessageBox.information(self, "Client Modificat cu succes", "Datele au fost modificate cu succes si adaugate in baza de date")
                self.close()
        except BaseException as e:
            logging.exception(e)

    def delete_client(self):
        session = Session()

        try:
            client = session.query(Client).filter(Client.id == self.id_client).first()
            session.delete(client)
            session.commit()
            QMessageBox.information(self, "Client Sters cu succes",
                                    "Clientul a fost sters cu succes din baza de date")
            self.close()
        except BaseException as e:
            logging.exception(e)
    def populate_data(self):

        try:
            session = Session()
            client = session.query(Client).filter(Client.id == self.id_client).all()

            for column in client:
                self.ui.name_input.setText(str(column.name))
                if column.type_client == "Fizica":
                    self.ui.rb_fizica.setChecked(True)
                else:
                    self.ui.rb_juridica.setChecked(True)
                self.ui.street_input.setText(str(column.street))
                self.ui.nr_street_input.setText(str(column.street_number))
                self.ui.oras_input.setText(str(column.city))
                self.ui.judet_input.setText(str(column.district))
                self.ui.country_input.setText(str(column.country))
                self.ui.telefon_input.setText(str(column.phone))
                self.ui.email_input.setText(str(column.email))
                self.ui.zip_code_input.setText(str(column.zip_code))
                try:
                    binary_data = column.image
                    image = Image.open(io.BytesIO(binary_data))
                    qimage = QImage.fromData(binary_data, "PNG")
                    pixmap = QPixmap.fromImage(qimage)
                    scaled_pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    self.ui.image.setPixmap(scaled_pixmap)
                except BaseException as e:
                    session.close()
                    print(f"A avut loc o eroare: {e}")
            session.close()
        except BaseException as e:
            logging.exception(e)
