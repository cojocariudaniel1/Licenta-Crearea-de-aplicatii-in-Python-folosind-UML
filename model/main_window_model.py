import logging

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent, QPixmap, QImage
from PyQt5.QtWidgets import QLabel, QTreeWidgetItem, QHBoxLayout, QVBoxLayout, QWidget
from qtpy import QtCore

from base import Session
from client import Client
from model.custom_classes import FRAME_LIST, CustomFrame, CustomQTreeWidgetSortingModified, LabelClick
from model.form_create_model import ClientCreateForm
from model.form_edit_client_model import ClientEditForm
from views.main_window import Ui_Form


class MainWindow(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.new_window = None
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.tree_widget = CustomQTreeWidgetSortingModified(self)
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(10)
        self.widget_container = QWidget()
        self.container_layout = QVBoxLayout()
        self.container_layout.setSpacing(10)

        self.create_tree_widget()

        self.select_kanban_view()
        self.client_list = []
        self.kanban_page_nr = 1
        self.kanban_current_page = 1
        self.tree_widget.hide()

        self.ui.create_customer.clicked.connect(self.click_create_button)

        for frame in FRAME_LIST:
            if frame.index >= 0:
                frame.setStyleSheet(
                    "background-color: rgb(249,249,249); border: 1px solid rgb(249,249,249); font-family: 'Calibri'; font-size: 17px;")
                frame.selected = False
            else:
                frame.setStyleSheet(
                    "background-color: rgb(242,242,244); border: 1px solid rgb(242,242,244); font-family: 'Calibri'; font-size: 17px;")

        self.populate_tree_vew()
        self.populate_kanban_view()

        self.btn_next = LabelClick(self)
        self.btn_next.setText("Next Page")
        self.btn_next.setStyleSheet("background-color: rgb(174, 139, 137);\n"
                                    "color: rgb(255, 255, 255);\n"
                                    "border: 1px solid ;\n"
                                    "border-top-color:  rgba(0, 0, 0, 75);\n"
                                    "border-bottom-color: rgba(0, 0, 0, 75);\n"
                                    "border-right-color:  rgba(0, 0, 0, 75);\n"
                                    "border-left-color: rgba(255, 255, 255, 200);")
        self.btn_next.setAlignment(QtCore.Qt.AlignCenter)
        self.btn_next.setGeometry(QtCore.QRect(1075, 700, 91, 26))

        self.btn_previous_page = LabelClick(self)
        self.btn_previous_page.setText("Previous Page")
        self.btn_previous_page.setGeometry(QtCore.QRect(915, 700, 106, 26))
        self.btn_previous_page.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.btn_previous_page.setStyleSheet("background-color: rgb(174, 139, 137);\n"
                                             "color: rgb(255, 255, 255);\n"
                                             "border: 1px solid ;\n"
                                             "border-top-color:  rgba(0, 0, 0, 75);\n"
                                             "border-bottom-color:  rgba(0, 0, 0, 75);\n"
                                             "border-left-color: rgba(0, 0, 0, 75);\n"
                                             "border-right-color: rgba(255, 255, 255, 200);")
        self.btn_previous_page.setAlignment(QtCore.Qt.AlignCenter)

        self.btn_next.clicked.connect(self.kanban_next_page)
        self.btn_previous_page.clicked.connect(self.kanban_previous_page)

    def click_create_button(self):
        self.new_window = ClientCreateForm()
        self.new_window.show()

    def clientEditFormClosed(self):
        self.populate_kanban_view()
        self.populate_tree_vew()

    def create_tree_widget(self):
        columns = ["Id", "Type client", "Name", "Street", "Street Mr", "City", "District", "Country", "Zip code",
                   "Email", "Web Site"]
        self.tree_widget.setHeaderLabels(columns)
        self.tree_widget.setGeometry(QtCore.QRect(33, 145, 1140, 551))
        # self.tree_widget.setSortingEnabled(True)
        self.tree_widget.setGeometry(QtCore.QRect(33, 145, 1140, 551))
        self.tree_widget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tree_widget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tree_widget.setAutoScrollMargin(16)
        self.tree_widget.setAlternatingRowColors(False)
        self.tree_widget.setAnimated(True)
        self.tree_widget.setExpandsOnDoubleClick(False)
        self.tree_widget.setObjectName("tree_view_widget_client")
        self.tree_widget.header().setVisible(True)
        self.tree_widget.header().setCascadingSectionResizes(False)
        self.tree_widget.header().setHighlightSections(False)
        self.tree_widget.header().setSortIndicatorShown(True)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        event.accept()
        if event.button() == Qt.LeftButton:
            if self.parent is not None:
                click_pos = (event.pos().x(), event.pos().y())
                list_view_pos = self.ui.list_select.pos()
                list_view_pos_rect = (list_view_pos.x(), list_view_pos.y(),
                                      list_view_pos.x() + self.ui.list_select.width(),
                                      list_view_pos.y() + self.ui.list_select.height())

                kanban_view_pos = self.ui.kanban_select.pos()
                kanban_view_pos_rect = (kanban_view_pos.x(), kanban_view_pos.y(),
                                        kanban_view_pos.x() + self.ui.kanban_select.width(),
                                        kanban_view_pos.y() + self.ui.kanban_select.height())

                if click_pos[0] in range(kanban_view_pos_rect[0], kanban_view_pos_rect[2]):
                    if click_pos[1] in range(kanban_view_pos_rect[1], kanban_view_pos_rect[3]):
                        self.select_kanban_view()
                if click_pos[0] in range(list_view_pos_rect[0], list_view_pos_rect[2]):
                    if click_pos[1] in range(list_view_pos_rect[1], list_view_pos_rect[3]):
                        self.select_list_view()

    def select_kanban_view(self):
        self.ui.kanban_select.show()
        self.ui.list_select.hide()
        self.tree_widget.hide()
        self.ui.frame.show()

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

    def populate_kanban_view(self):
        session = Session()
        # clients = session.query(Client).limit(12).all()
        clients = session.query(Client).order_by(Client.id).limit(12).all()
        clients_page = session.query(Client).order_by(Client.id).all()
        session.close()

        self.kanban_page_nr = 1
        # get pages number
        counter_page_var = 0
        for i in clients_page:
            if counter_page_var < 12:

                counter_page_var += 1
            else:
                self.kanban_page_nr += 1
                counter_page_var = 0

        self.ui.page.setText(f"{self.kanban_current_page}/{self.kanban_page_nr}")

        self.generate_kanban_after_page_changed(clients)
    def kanban_previous_page(self):
        try:
            session = Session()
            if self.kanban_current_page == 1:
                generate_kanban_bool = False
                print('min page')
            else:
                generate_kanban_bool = True
                self.kanban_current_page -= 1
                self.ui.page.setText(f"{self.kanban_current_page}/{self.kanban_page_nr}")
                FRAME_LIST.clear()
            current_page = (self.kanban_current_page - 1) * 12
            print(current_page)
            if generate_kanban_bool:
                clients = session.query(Client).order_by(Client.id).offset(current_page).limit(12).all()
                self.generate_kanban_after_page_changed(clients)
            session.close()
        except BaseException as e:
            logging.exception(e)

    def kanban_next_page(self):
        try:
            logging.info("execute kanban_next_page")
            session = Session()
            if self.kanban_current_page == self.kanban_page_nr:
                generate_kanban_bool = False
            else:
                generate_kanban_bool = True
                self.kanban_current_page += 1
                self.ui.page.setText(f"{self.kanban_current_page}/{self.kanban_page_nr}")
                FRAME_LIST.clear()
            current_page = (self.kanban_current_page - 1) * 12
            print(current_page)
            if generate_kanban_bool:
                clients = session.query(Client).order_by(Client.id).offset(current_page).limit(12).all()
                logging.info("execute generate_kanban_after_page_changed")
                self.generate_kanban_after_page_changed(clients)
                session.close()
        except BaseException as e:
            logging.exception(e)

    def reset_layout(self, layout):
        try:
            while layout.layout().count():
                item = layout.takeAt(0)
                if item.widget() is not None:
                    item.widget().deleteLater()
                elif item.layout() is not None:
                    self.reset_layout(item.layout())
        except BaseException as e:
            logging.exception(e)

    def generate_kanban_after_page_changed(self, clients):
        self.clearLayout(self.container_layout.layout())
        try:
            element_count = 0
            if clients[0].id == 1:
                ID_CLIENT = clients[0].id - 1
            else:
                ID_CLIENT = clients[0].id

            for i in range(int(9 / 3) + 1):

                h_layout = QHBoxLayout()
                h_layout.setContentsMargins(20, 5, 20, 0)
                for j in range(3):
                    if ID_CLIENT > clients[-1].id:
                        # adaugă un widget gol
                        label_icon = QLabel("")
                        label_text = QLabel("")
                        kanban_view = QHBoxLayout()

                        kanban_view.addWidget(label_icon)
                        kanban_view.addWidget(label_text)

                        frame1 = CustomFrame(i * (-1) - 1)
                        frame1.setStyleSheet("background-color: transparent; border: none;")
                        FRAME_LIST.append(frame1)
                        frame1.setLayout(kanban_view)
                        h_layout.addWidget(frame1)
                    else:

                        label_icon = QLabel()
                        image = QImage.fromData(clients[element_count].image)
                        pixmap = QPixmap.fromImage(image)
                        scaled_pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                        label_icon.setPixmap(scaled_pixmap)
                        label_text = QLabel(str(clients[element_count].name))
                        label_text.setStyleSheet("font-family: 'Calibri'; font-size: 17px;")

                        frame1 = CustomFrame(clients[element_count].id)
                        frame1.window_closed_2.connect(self.clientEditFormClosed)
                        frame1.setStyleSheet(
                            "background-color: #F9F9F9; font-family: 'Calibri'; font-size: 17px; border: 1px solid rgb(249,249,249);")
                        kanban_view = QHBoxLayout()
                        kanban_view.addWidget(label_icon)
                        kanban_view.addWidget(label_text)

                        frame1.setLayout(kanban_view)
                        FRAME_LIST.append(frame1)
                        h_layout.addWidget(frame1)
                    element_count += 1
                    ID_CLIENT += 1

                self.container_layout.addLayout(h_layout)
            self.widget_container.setLayout(self.container_layout)
            self.main_layout.addWidget(self.widget_container)
            self.ui.frame.setLayout(self.main_layout)
            self.ui.frame.setStyleSheet(
                "background-color: #F2F2F4; font-family: 'Calibri'; font-size: 17px; border: 1px solid rgb(249,249,249);")
        except Exception as e:
            print(clients[0].id)
            logging.exception(e)

    def populate_tree_vew(self):
        session = Session()
        print("preread")
        try:
            self.client_list.clear()
            self.tree_widget.clear()
            clients = session.query(Client).order_by(Client.id).all()
            for i in clients:
                db_client = [i.id, i.type_client, i.name, i.street, i.street_number, i.city, i.district, i.country,
                             i.zip_code,
                             i.email, i.web_site]
                self.client_list.append(db_client)

            for index, row in enumerate(self.client_list):
                self.client_list[index] = [str(x) for x in row]

            self.client_list.sort(key=lambda x: int(x[0]))
            for row in self.client_list:
                self.tree_widget.addTopLevelItem(QTreeWidgetItem(row))
            session.close()
        except BaseException as e:
            logging.exception(e)
            session.close()

    def select_list_view(self):
        try:
            self.ui.list_select.show()
            self.ui.kanban_select.hide()
            self.tree_widget.show()
            self.ui.frame.hide()
        except BaseException as e:
            logging.exception(e)
