from sqlalchemy.orm import joinedload

from adress import AdressTable
from base import Session
from customer import CustomersTable
from repository.bank_account_methods import create_bank
from sales import SalesTable
from SalesProduct import SaleProducts
from product import ProductTable
from bankaccount import BankAccount


def get_customers_for_kanban():
    session = Session()
    customers = session.query(CustomersTable).order_by(CustomersTable.id).limit(12).all()
    customers_page = len(session.query(CustomersTable).order_by(CustomersTable.id).all())
    session.close()
    return customers, customers_page


def get_customers_for_populate_tree_view():
    session = Session()
    customers = session.query(CustomersTable).order_by(CustomersTable.id).options(joinedload(CustomersTable.adress)).all()
    session.close()
    return customers


def get_customers_with_offset(offset, filter=None):
    session = Session()
    if filter is None:
        customers = session.query(CustomersTable).order_by(CustomersTable.id).offset(offset).limit(12).all()
    else:
        customers = session.query(CustomersTable).filter(CustomersTable.name.ilike(f"%{filter}%")).order_by(
            CustomersTable.id).offset(offset).limit(12).all()
    session.close()
    return customers


def get_customers():
    session = Session()
    customers = session.query(CustomersTable).all()
    session.close()
    return customers


def create_customer(type_customer, name, street, street_number, city, district, country, phone, web_site, email, zip_code,
                  image, banks):
    customer = CustomersTable(type_customer=type_customer, name=name, image=image)
    adress = AdressTable(street, street_number, city, district, country, phone, web_site, email, zip_code)
    banks_list = []
    for row in banks:
        banks_list.append(create_bank(row))
    customer.account = banks_list
    customer.adress = adress
    session = Session()
    session.add(customer)
    session.commit()
    session.close()


def filter_customers_kanban(customer_name):
    session = Session()
    customers = session.query(CustomersTable).filter(CustomersTable.name.ilike(f"%{customer_name}%")).order_by(
        CustomersTable.id).limit(12).all()
    customers_page = len(session.query(CustomersTable).filter(CustomersTable.name.ilike(f"%{customer_name}%")).order_by(CustomersTable.id).all())
    session.close()

    return customers, customers_page


def get_customers_for_populate_tree_view_filter(customer_name):
    session = Session()
    customers = session.query(CustomersTable).filter(CustomersTable.name.ilike(f"%{customer_name}%")).order_by(
        CustomersTable.id).options(joinedload(CustomersTable.adress)).all()
    session.close()
    return customers


def get_customer_by_id(id_customer):
    session = Session()
    customer = session.query(CustomersTable).filter(CustomersTable.id == id_customer).options(
        joinedload(CustomersTable.adress)).first()
    return customer


def save_customer(id_customer, name, type_customer, street, street_number, city, district, country, phone, email, zip_code,
                image):
    session = Session()

    customer = session.query(CustomersTable).filter(CustomersTable.id == id_customer).first()
    customer.name = name
    customer.type_customer = type_customer
    customer.image = image
    customer.adress.street = street
    customer.adress.street_number = street_number
    customer.adress.city = city
    customer.adress.district = district
    customer.adress.country = country
    customer.adress.phone = phone
    customer.adress.email = email
    customer.adress.zip_code = zip_code

    session.commit()
    session.close()


def delete_customer(id_customer):
    session = Session
    customer = session.query(CustomersTable).filter(CustomersTable.id == id_customer).first()
    session.delete(customer)
    session.commit()
    session.close()


if __name__ == "__main__":
    k = get_customers_for_populate_tree_view()
    for j in k:
        print(j.adress)
