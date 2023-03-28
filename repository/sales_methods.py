from sqlalchemy import update, delete

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
    for idx, i in enumerate(data):
        client = session.query(ClientTable).filter(ClientTable.id == i[1][2]).first()
        if client:
            data[idx][1][2] = client
    session.close()
    return data

def edit_sale(sale_number, creation_date, sale_total, products):
    session = Session()

    sale = session.query(SalesTable).filter(SalesTable.number == sale_number).first()
    saleproducts = session.query(SaleProducts).filter(SaleProducts.sales_id == sale.id)
    for row in saleproducts:
        session.execute(
            delete(SaleProducts).where(SaleProducts.id == row.id)
        )
    product_class_list = []

    for product_id in products:
        product = session.query(ProductTable).filter(ProductTable.id == product_id).first()
        product_class_list.append(product)

    sale.product = product_class_list
    sale.total = sale_total
    sale.creation_date = creation_date

    for product in product_class_list:
        session.execute(
            (
                update(SaleProducts).
                where(SaleProducts.sales_id == sale.id, SaleProducts.product_id == product.id).
                values(quantity=product.quantity)
            )
        )
    session.commit()
    session.close()

def get_sale_by_number(sale):
    session = Session()
    sale_query = session.query(SalesTable).filter(SalesTable.number == sale).first()

    session.close()
    return sale_query


def create_sale(client_id, creation_date, sale_total, products):
    session = Session()
    product_class_list = []

    for product_id in products:
        product = session.query(ProductTable).filter(ProductTable.id == product_id).first()
        product_class_list.append(product)

    last_sale_number = int(session.query(SalesTable).all()[-1].number.replace("S", "")[1:])
    number = f"S00{last_sale_number + 1}"
    sale = SalesTable(number, creation_date)

    sale.product = product_class_list
    sale.total = sale_total
    sale.client_id = client_id

    session.add(sale)
    session.commit()

    for product in product_class_list:
        session.execute(
            (
                update(SaleProducts).
                where(SaleProducts.sales_id == sale.id, SaleProducts.product_id == product.id).
                values(quantity=product.quantity)
            )
        )
    session.commit()
    session.close()


