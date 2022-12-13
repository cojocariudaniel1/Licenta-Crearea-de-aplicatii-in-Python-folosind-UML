import logging

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor, QMouseEvent
from PyQt5.QtWidgets import QGridLayout, QLabel, QTreeWidget, QTreeWidgetItem

from model.form_creatre import ClientCreateForm
from views.main_window import Ui_Form


class Label(QLabel):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        QLabel.__init__(self, parent=parent)

    def mousePressEvent(self, event):
        self.clicked.emit()


class LoginWindow(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.new_window = None
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.select_kanban_view()
        self.ui.tree_view_widget_client.hide()
        self.row_numbers = 4
        self.column_numbers = 4
        # self.box('1', '1')
        # self.box('2', '2')
        # self.box('3', '3')
        # self.box('4', '5')
        # Position: xy,  a0 rowspan a1 colspan (default 1)
        self.test()
        # self.box('test', 'test',0,0)

        self.ui.kanban.setHorizontalSpacing(30)
        self.set_grid_row_column(self.row_numbers, self.column_numbers)
        self.ui.create_customer.clicked.connect(self.click_create_button)
        self.populate_tree_vew()

    def click_create_button(self):
        self.new_window = ClientCreateForm()
        self.new_window.show()

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
        self.ui.tree_view_widget_client.hide()
        self.ui.gridLayoutWidget.show()

    # def populate_tree_vew(self):
    #     client_list = [
    #         ['3', "Fizica", 'razvan@gmail.com', '0723411932', 'Sperantei', '32', "Iasi", "Iasi", "Romania", 'd'],
    #         ['4', "Fizica", 'razvan@gmail.com', '0723411932', 'Sperantei', '32', "Iasi", "Iasi", "Romania", ''],
    #         ['5', "Fizica", 'razvan@gmail.com', '0723411932', 'Sperantei', '32', "Iasi", "Iasi", "Romania", 'd']
    #     ]
    #     for row in client_list:
    #         self.ui.tree_view_widget_client.addTopLevelItem(QTreeWidgetItem(row))


    def select_list_view(self):
        self.ui.list_select.show()
        self.ui.kanban_select.hide()
        self.ui.tree_view_widget_client.show()
        self.ui.gridLayoutWidget.hide()

    def test(self):
        name_list = ["Name1", "Name2", "Name3"]
        type_list = ["Type1", "Type2", "Type3"]
        x, y = 0, 0
        while x < self.row_numbers:
            while y < self.column_numbers:
                try:
                    if name_list[y] and type_list[y]:
                        self.box(name_list[y], type_list[y], x, y)
                except BaseException as e:
                    logging.exception(e)
                y += 1
            x += 1

    def empty_grid_element(self, name_v, type_v):
        glay = QGridLayout()
        image = QLabel("")
        name = QLabel(str(name_v))
        type_person = QLabel(str(type_v))
        glay.addWidget(image, 0, 0, 2, 1)
        glay.addWidget(name, 0, 1)

        glay.setRowMinimumHeight(0, 50)
        glay.setRowMinimumHeight(1, 50)

        return glay

    # 31
    def set_grid_row_column(self, row_len, column_len):
        for i in range(row_len):
            for k in range(column_len):
                self.ui.kanban.addLayout(self.empty_grid_element("", ""), i, k)
                print(i, k)

    def box(self, name_v, type_person_v, x, y):

        path = "./sprites/img.png"
        glay = QGridLayout()
        image = QLabel()
        name = QLabel(str(name_v))
        type_person = QLabel(str(type_person_v))
        pixmap = QtGui.QPixmap(path)
        image.setPixmap(pixmap.scaled(120, 100, Qt.KeepAspectRatio))

        glay.addWidget(image, 0, 0)
        glay.addWidget(name, 1, 0)

        glay.setRowMinimumHeight(0, 50)
        glay.setRowMinimumHeight(1, 50)
        glay.setColumnMinimumWidth(0, 100)
        glay.setColumnMinimumWidth(1, 100)

        for label in [name, type_person]:
            color = QColor(246, 247, 250)
            label.setStyleSheet(
                '.QLabel{{background: rgb({}, {}, {});}}'.format(color.red(), color.green(), color.blue()))

        self.ui.kanban.addLayout(glay, x, y)
