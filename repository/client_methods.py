from base import Session
from client import ClientTable
from sales import SalesTable
from SalesProduct import SaleProducts
from invoicing import InvoicingTable
from product import ProductTable
from bankaccount import BankAccount

def get_clients_for_kanban():
    session = Session()
    clients = session.query(ClientTable).order_by(ClientTable.id).limit(12).all()
    clients_page = len(session.query(ClientTable).order_by(ClientTable.id).all())
    session.close()
    return clients, clients_page


def get_clients_for_populate_tree_view():
    session = Session()
    clients = session.query(ClientTable).order_by(ClientTable.id).all()
    session.close()
    return clients


def get_clients_with_offes(offset):
    session = Session()
    clients = session.query(ClientTable).order_by(ClientTable.id).offset(offset).limit(12).all()
    session.close()
    return clients


def get_clients():
    session = Session()
    clients = session.query(ClientTable).all()
    session.close()
    return clients


def create_client(type_client, name, street, street_number, city, district, country, phone, web_site, email, zip_code,
                  image):
    client = ClientTable(type_client=type_client, name=name, street=street, street_number=street_number,
                         city=city, district=district, country=country, phone=phone, web_site=web_site, email=email,
                         zip_code=zip_code, image=image)

    session = Session()
    session.add(client)
    session.commit()
    session.close()


def get_client_by_id(id_client):
    session = Session()
    client = session.query(ClientTable).filter(ClientTable.id == id_client).first()
    return client


def save_client(id_client, name, type_client, street, street_number, city, district, country, phone, email, zip_code,
                image):
    session = Session()

    client = session.query(ClientTable).filter(ClientTable.id == id_client).first()

    client.name = name
    client.type_client = type_client
    client.street = street
    client.street_number = street_number
    client.city = city
    client.district = district
    client.country = country
    client.phone = phone
    client.email = phone
    client.zip_code = zip_code
    client.image = image

    session.commit()
    session.close()


def delete_client(id_client):
    session = Session
    client = session.query(ClientTable).filter(ClientTable.id == id_client).first()
    session.delete(client)
    session.commit()
    session.close()
