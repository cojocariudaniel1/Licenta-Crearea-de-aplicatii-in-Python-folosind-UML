import logging

from PyQt5 import QtWidgets

from model.custom_classes.custom_table import CustomTable
from repository.products_methods import get_products_with_id
from views.products_view import Ui_Form


class ProductFormView(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.new_window = None
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setup_product_table()

    def setup_product_table(self):
        header = [
            {"name": "Nume Produs", "width": 265},
            {"name": "Tip Produs", "width": 185},
            {"name": "UoM", "width": 135},
            {"name": "Cantitate", "width": 145},
            {"name": "Pret", "width": 145},
            {"name": "Depozit", "width": 150},
            {"name": "TVA", "width": 100}
        ]
        self.tree_view = CustomTable(self.ui.product_layout.x, self.ui.product_layout.y,
                                         self.ui.product_layout.width,
                                         self.ui.product_layout.height, self.ui.product_layout)

        self.tree_view.header(header)
        data = get_products_with_id()
        try:
            self.tree_view.populate_table(data)
        except BaseException as e:
            logging.exception(e)
