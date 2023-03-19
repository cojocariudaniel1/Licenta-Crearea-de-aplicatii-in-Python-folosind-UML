from base import Session
from client import ClientTable
from sales import SalesTable
from SalesProduct import SaleProducts
from invoicing import InvoicingTable
from product import ProductTable
from bankaccount import BankAccount


def get_all_sales():
    data = []
    session = Session()
    sales = session.query(SalesTable).order_by(SalesTable.id).all()
    for row in sales:
        raw_data = []
        for product in row.product:
            raw_data.append(product)

        data.append([row.id, [row.number, row.creation_date, row.client_id, row.total]])
    session.close()

    return data
