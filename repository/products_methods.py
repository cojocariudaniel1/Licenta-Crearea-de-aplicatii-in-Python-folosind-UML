from base import Session
from customer import CustomersTable
from sales import SalesTable
from SalesProduct import SaleProducts
from product import ProductTable
from bankaccount import BankAccount


def get_products():
    session = Session()
    products = session.query(ProductTable).order_by(ProductTable.id).all()

    session.close()
    return products

def get_products_with_id():
    data = []
    session = Session()
    products = session.query(ProductTable).order_by(ProductTable.id).all()
    for product in products:
        data.append([product.id, [product.product_name, product.product_type, product.unit_of_measure, product.quantity, product.price, product.deposit, product.tva]])

    return data

def get_product_by_id(product_id):
    session = Session()
    product = session.query(ProductTable).filter(ProductTable.id == product_id).first()
    session.close()
    return product

def get_product_with_sale_id(sale_id):
    session = Session()
    products_list = []
    products= session.query(SaleProducts).filter(SaleProducts.sales_id == sale_id).all()
    for product in products:
        products_list.append(product)

    session.close()

    return products_list