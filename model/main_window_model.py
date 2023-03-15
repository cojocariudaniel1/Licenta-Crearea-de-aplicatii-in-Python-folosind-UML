import io
import logging
from functools import partial

from PIL import Image
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, QBuffer, QSize, QRect
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QPushButton

from base import Session
from client import Client
from model.client_view_model import ClientWindow
from views.main_window import Ui_Form


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.new_window = None
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setup_btn_icons()

    def sales_btn_click(self):
        pass

    def planning_btn_click(self):
        pass

    def email_marketing_btn_click(self):
        pass

    def point_of_sales_btn_click(self):
        pass

    def project_btn_click(self):
        pass

    def web_site_btn_click(self):
        pass

    def product_btn_click(self):
        pass

    def clients_btn_click(self):
        self.new_window = ClientWindow()
        self.new_window.show()

    def invoicing_btn_click(self):
        # TODO invoicing interface.
        pass

    def setup_btn_icons(self):
        try:
            self.set_icon("sales_icon.png", self.ui.sales_btn, self.sales_btn_click)
            self.set_icon("clients_icon.png", self.ui.clients_btn, self.clients_btn_click)
            self.set_icon("email_marketing_icon.png", self.ui.email_marketing_btn)
            self.set_icon("invoicing_icon.png", self.ui.invoicing_btn)
            self.set_icon("point_of_sales_icon.png", self.ui.point_of_sales_btn)
            self.set_icon("product_icon.png", self.ui.products_btn)
            self.set_icon("accounting_icon.png", self.ui.accounting_btn)
            self.set_icon("projects_icon.png", self.ui.projects_btn)
            self.set_icon("web_site_icon.png", self.ui.web_site_btn)
            self.set_icon("planning_icon.png", self.ui.planning_btn)
            self.set_icon("purchase_icon.png", self.ui.purchase_btn)
        except BaseException as e:
            logging.exception(e)

    def button_mousePressEvent_effect(self, event, button):
        super().mousePressEvent(event)
        button.setStyleSheet(
            "border-top: 1px solid black; border-left: 1px solid black; border-right: 1px; border-bottom: 1px")

    def mouseReleaseEvent_effect(self, event, button, function=None):
        super().mouseReleaseEvent(event)
        button.setStyleSheet(
            "border-top: 0px solid black; border-left: 0px solid black; border-right: 1px solid black; border-bottom: 1px solid black")
        if function:
            function()

    def set_icon(self, icon_path, button, function=None):
        try:
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(f"./sprites/button_icons/{icon_path}"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            button.setIcon(icon)
            button.setIconSize(QtCore.QSize(100, 100))
            button.mousePressEvent = partial(self.button_mousePressEvent_effect, button=button)
            button.mouseReleaseEvent = partial(self.mouseReleaseEvent_effect, button=button, function=function)
            button.setStyleSheet(
                "border-top: 0px solid black; border-left: 0px solid black; border-right: 1px solid black; border-bottom: 1px solid black")

        except BaseException as e:
            logging.exception(e)
