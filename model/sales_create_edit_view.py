import logging
from datetime import date

from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, QEvent, Qt, QRect, pyqtSignal

from model.custom_classes.custom_product_table import CustomTable, HideUserInput
from model.custom_classes.extended_combobox import ExtendedComboBox
from repository.customers_methods import get_customers_for_populate_tree_view, get_customer_by_id
from repository.products_methods import get_products, get_product_with_sale_id, get_product_by_id
from repository.sales_methods import create_sale, get_sale_by_number, edit_sale
from views.sales_create_view import Ui_Form


class SaleForm(QtWidgets.QWidget):
    save_signal = pyqtSignal()

    def __init__(self, form, sale=None):
        super().__init__()
        self.new_window = None
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.open_form = False
        self.form = form
        self.sale = sale
        self.ui.client_name_input.hide()
        self.data = None
        self.products_data = None
        self.creat_date_datetime_format = date.today()
        self.event_userinput = HideUserInput()
        self.customer_combobox = ExtendedComboBox(self)
        self.customer_combobox.setObjectName("ComboBox")
        self.customer_combobox.setGeometry(self.ui.client_name_input.geometry())
        self.customer_combobox.activated.connect(self.change_client_details)
        self.customer_combobox.setStyleSheet(self.ui.lb_client.styleSheet())
        self.customer_combobox.setMinimumWidth(250)
        self.customer_combobox.setMaximumWidth(250)
        self.ui.adress_label.setMinimumWidth(300)
        self.ui.order_date_value.setText(f"{self.creat_date_datetime_format}")

        self.base_x_order_date_lb = self.ui.lb_order_date.x()
        self.base_x_order_value = self.ui.order_date_value.x()
        self.populate_combobox()

        self.custom_table = CustomTable(self.ui.product_layout.x, self.ui.product_layout.y,
                                        self.ui.product_layout.width, self.ui.product_layout.height,
                                        self.ui.product_layout)

        self.set_custom_table()

        self.product_combobox = ExtendedComboBox(self)
        self.setupcombobox_product()
        self.product_combobox.activated.connect(self._add_product_to_table)
        self.check_form()
        self.ui.btn_close_sale.clicked.connect(self.close_form)
        self.ui.btn_edit_sale.clicked.connect(self.edit_sale)
        self.ui.btn_save_sale.clicked.connect(self.save_sale_method)

    def close_form(self):
        self.hide()

    def check_form(self):
        if self.form == "create":
            self.ui.btn_save_sale.show()
            self.ui.btn_edit_sale.hide()
            self.ui.lb_add_product.show()
            self.product_combobox.show()

        elif self.form == "view":
            self.ui.btn_edit_sale.show()
            self.product_combobox.hide()
            self.ui.lb_add_product.hide()

        elif self.form == "open_form":
            if self.sale:
                self.ui.btn_edit_sale.show()
                self.product_combobox.hide()
                self.ui.lb_add_product.hide()
                self.ui.btn_save_sale.hide()
                self.open_form = True
                self.populate_form()

        elif self.form == "edit":
            self.ui.btn_save_sale.show()
            self.ui.btn_edit_sale.hide()
            self.ui.lb_add_product.show()
            self.ui.lb_title.setText("Edit Sale")
            self.product_combobox.show()
            self.customer_combobox.setDisabled(False)

    def edit_sale(self):
        self.form = "edit"
        self.check_form()

    def save_sale_method(self):
        self.hide()

        customer_id = self.customer_combobox.currentData()
        creation_date = self.ui.order_date_value.text()
        total_sale = self.ui.total_value.text()

        product_list = []
        table_data = self.custom_table.data_id
        for row in self.products_data:
            for product_id in table_data:
                if row.id == product_id:
                    product_list.append(product_id)

        self.check_form_for_save(creation_date, total_sale, product_list, customer_id)

    def check_form_for_save(self, creation_date, total_sale, product_list, customer_id):
        continue_bool = False
        try:
            if self.open_form:
                edit_sale(self.sale, creation_date, total_sale, product_list)
                print('a')
            else:
                create_sale(customer_id, creation_date, total_sale, product_list)
                print('b')
            continue_bool = True
        except BaseException as e:
            logging.exception(e)

        if continue_bool:
            self.save_signal.emit()
            self.hide()

    def populate_form(self):
        try:

            sale = get_sale_by_number(self.sale)
            client = get_customer_by_id(sale.customer_id)
            products = get_product_with_sale_id(sale.id)

            self.customer_combobox.setCurrentIndex(client.id - 1)
            self.ui.order_date_value.setText(str(sale.creation_date))
            self.ui.client_adress.setText(f" {str(client.adress.street)} {str(client.adress.street_number)}")
            self.ui.client_country.setText(str(client.adress.country))

            self.populate_table_products(products)



        except BaseException as e:
            logging.exception(e)

    def setupcombobox_product(self):
        self.product_combobox.setGeometry(self.ui.add_product_cb.geometry())
        self.product_combobox.show()
        self.ui.add_product_cb.hide()

        data = get_products()
        for row in data:
            self.product_combobox.addItem(row.product_name)
            self.product_combobox.setItemData(self.product_combobox.count() - 1, row.id, Qt.UserRole)

        self.products_data = data
        self.product_combobox.setCurrentText("")

    def populate_table_products(self, products):
        for saleproduct in products:
            product = get_product_by_id(saleproduct.product_id)
            self.custom_table.add_row(
                [product.id, product.product_name, product.product_type, product.unit_of_measure, product.quantity,
                 product.price, product.tva]
            )
        self.calculate_sale_price()

        self.custom_table.draw_tree()

    def _add_product_to_table(self, index):
        product_id = self.customer_combobox.itemData(index, Qt.UserRole)
        try:
            for row in self.products_data:
                if row.id == product_id:
                    self.custom_table.add_row(
                        [row.id, row.product_name, row.product_type, row.unit_of_measure, row.quantity, row.price,
                         row.tva])
                    self.custom_table.draw_tree()

            self.calculate_sale_price()
        except BaseException as e:
            logging.exception(e)

    def update_price(self):
        try:

            total_without_taxes = 0
            total_taxes = 0
            # 3, 4 , 3 cantitate, 4 price, 5 - taxes
            for idx, row in enumerate(self.custom_table.data):
                quantity = 0
                price = 0
                taxes = 0
                for idx2, item in enumerate(row):
                    if idx2 == 3:
                        quantity = float(item.text())
                    elif idx2 == 4:
                        price = float(item.text())
                    elif idx2 == 5:
                        taxes = float(item.text())
                total_without_taxes += quantity * price
                total_taxes += quantity * (price * (taxes / 100))
            print(total_taxes)
            total_price = total_without_taxes + total_taxes

            self.ui.lb_amount_value.setText(str(float("{:.2f}".format(total_without_taxes))))
            self.ui.taxes_value.setText(str(float("{:.2f}".format(total_taxes))))
            self.ui.total_value.setText(str(float("{:.2f}".format(total_price))))
        except BaseException as e:
            logging.exception(e)

    def calculate_sale_price(self):
        total_without_taxes = 0
        taxes_price = 0
        table_data = self.custom_table.data_id
        for row in self.products_data:
            for product_id in table_data:
                if row.id == product_id:
                    print(row.tva, product_id)
                    taxes_price += row.quantity * (row.price * (row.tva / 100))
                    total_without_taxes += row.price * row.quantity

        total_price = total_without_taxes + taxes_price

        self.ui.lb_amount_value.setText(str(float("{:.2f}".format(total_without_taxes))))
        self.ui.taxes_value.setText(str(float("{:.2f}".format(taxes_price))))
        self.ui.total_value.setText(str(float("{:.2f}".format(total_price))))

    def change_client_details(self, index):
        try:
            client_id = self.customer_combobox.itemData(index, Qt.UserRole)

            for row in self.data:
                if row.id == client_id:
                    self.ui.client_adress.setText(f"Strada {row.adress.street}, Nr {row.adress.street_number}")
                    self.ui.client_country.setText(row.adress.country)

        except BaseException as e:
            logging.exception(e)

    def populate_combobox(self):
        try:
            data = get_customers_for_populate_tree_view()
            for row in data:
                self.customer_combobox.addItem(row.name)
                self.customer_combobox.setItemData(self.customer_combobox.count() - 1, row.id, Qt.UserRole)
            self.data = data
        except BaseException as e:
            logging.exception(e)

    def set_custom_table(self):

        try:
            header = [
                {"name": "Product Name", "width": 300},
                {"name": "Product Type", "width": 200},
                {"name": "UoM", "width": 175},
                {"name": "Quantity", "width": 150},
                {"name": "Price", "width": 175},
                {"name": "TVA", "width": 150}
            ]
            self.custom_table.header(header)
            self.custom_table.show()
            self.custom_table.header_objects.append({"idx": 3, "event": "editable"})
            self.installEventFilter(self.event_userinput)
            self.custom_table.installEventFilter(self.event_userinput)
            self.event_userinput.hide_user_input_signal.connect(self.hide_user_input)
            self.custom_table.update_values.connect(self.update_price)

        except BaseException as e:
            logging.exception(e)

    def hide_user_input(self):
        self.custom_table.edit_label(None)
        self.update_price()
