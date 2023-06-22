import logging

from PyQt5 import QtWidgets
from PyQt5.QtCore import QEvent, pyqtSignal, QObject, Qt

from model.custom_classes.custom_table import CustomTable, HideUserInput
from model.custom_classes.extended_combobox import ExtendedComboBoxFilter
from model.sales_create_edit_view import SaleForm
from repository.sales_methods import get_all_sales, filter_sale
from views.sales_main_view import Ui_Form


class SalesForm(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.new_window = None
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.sales_filter = ExtendedComboBoxFilter(self)
        self.setup_filter()
        self.tableView = None
        self.make_table()

        try:
            self.sales_filter.setObjectName("ComboBox")
            self.sales_filter.setGeometry(self.ui.lineEdit.geometry())
            self.sales_filter.text_changed.connect(lambda text: self.search_sale(text))

        except BaseException as e:
            logging.exception(e)

    def make_table(self, data = None):
        self.tableView = CustomTable(self.ui.sales_view_layout.x, self.ui.sales_view_layout.y,
                                     self.ui.sales_view_layout.width, self.ui.sales_view_layout.height,
                                     self.ui.sales_view_layout)
        self.tableView.setObjectName("tableView")
        header_list = [
            {"name": "Number", "width": 200},
            {"name": "Creation Date", "width": 150},
            {"name": "Client", "width": 270},
            {"name": "Total", "width": 150},
        ]
        self.tableView.header(header_list)
        if data is not None:
            self.data = data
        else:
            self.data = get_all_sales()

        self.event_userinput = HideUserInput()
        self.installEventFilter(self.event_userinput)

        self.event_userinput.hide_user_input_signal.connect(self.hide_user_input)
        self.tableView.populate_table(self.data)

        self.ui.create_sale_btn.clicked.connect(self.create_sale)
        self.tableView.click_signal.connect(self.open_sale_form)



    def create_sale(self):
        self.new_window = SaleForm("create")
        self.new_window.save_signal.connect(self.update_table)
        self.new_window.show()

    def hide_user_input(self):
        self.tableView.edit_label(None)

    def open_sale_form(self, sale_nr):
        self.new_window = SaleForm("open_form", sale_nr)
        self.new_window.save_signal.connect(self.update_table)
        self.new_window.ui.lb_title.setText("View Sale")
        self.new_window.customer_combobox.setDisabled(True)
        self.new_window.show()

    def update_table(self, data = None):
        self.tableView.deleteLater()
        self.make_table(data)
        self.tableView.show()

    def search_sale(self, sale_number):
        print(f"sale number: {sale_number}")
        try:
            data = filter_sale(sale_number)
            self.update_table(data)
        except BaseException as e:
            logging.exception(e)

    def setup_filter(self):
        try:
            self.sales_filter.setGeometry(self.ui.lineEdit.geometry())
            self.sales_filter.show()
            self.ui.lineEdit.hide()

            data = get_all_sales()
            for row in data:
                self.sales_filter.addItem(row[1][0])
                self.sales_filter.setItemData(self.sales_filter.count() - 1, row[0], Qt.UserRole)

            self.sales_filter.setCurrentText("")
        except BaseException as e:
            logging.exception(e)
