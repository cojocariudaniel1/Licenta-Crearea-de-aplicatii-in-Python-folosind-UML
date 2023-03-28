import logging

from PyQt5 import QtWidgets
from PyQt5.QtCore import QEvent, pyqtSignal, QObject

from model.custom_classes.custom_table_sales_view import CustomTable, HideUserInput
from model.sales_form_model import SaleCreateForm
from repository.sales_methods import get_all_sales
from views.sales_view import Ui_Form


class SalesForm(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.new_window = None
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.tableView = None
        self.make_table()

    def make_table(self):
        self.tableView = CustomTable(self.ui.sales_view_layout.x, self.ui.sales_view_layout.y,
                                     self.ui.sales_view_layout.width, self.ui.sales_view_layout.height,
                                     self.ui.sales_view_layout)
        self.tableView.setObjectName("tableView")
        header_list = [
            {"name": "Number", "width": 100},
            {"name": "Creation Date", "width": 150},
            {"name": "Client", "width": 200},
            {"name": "Total", "width": 100},

        ]
        self.tableView.header(header_list)
        self.data = get_all_sales()
        self.event_userinput = HideUserInput()
        self.installEventFilter(self.event_userinput)

        self.event_userinput.hide_user_input_signal.connect(self.hide_user_input)
        self.tableView.populate_table(self.data)

        self.ui.create_sale_btn.clicked.connect(self.create_sale)
        self.tableView.click_signal.connect(self.open_sale_form)


    def create_sale(self):
        self.new_window = SaleCreateForm("create")
        self.new_window.save_signal.connect(self.update_table)
        self.new_window.show()

    def hide_user_input(self):
        self.tableView.edit_label(None)

    def open_sale_form(self, sale_nr):
        self.new_window = SaleCreateForm("open_form", sale_nr)
        self.new_window.save_signal.connect(self.update_table)
        self.new_window.show()

    def update_table(self):
        self.tableView.deleteLater()
        self.make_table()
        self.tableView.show()
