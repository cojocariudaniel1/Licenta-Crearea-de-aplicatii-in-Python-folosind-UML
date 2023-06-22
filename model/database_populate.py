from sqlalchemy import insert, update

from adress import AdressTable
from base import Session, Base, engine
from customer import CustomersTable
from product import ProductTable
from sales import SalesTable
from bankaccount import BankAccount
from SalesProduct import SaleProducts


def delete_db():
    session = Session()
    Base.metadata.reflect(bind=engine)  # To reflect any tables in the DB, but not in the current schema
    Base.metadata.drop_all(bind=engine)
    session.commit()


def update_quantity_sales(sale_id, products, session):
    """
    [
        [product1, 30], [product2, 50] ...
    ]

    """
    for product in products:
        session.execute(
            (
                update(SaleProducts).
                where(SaleProducts.sales_id == sale_id, SaleProducts.product_id == product.id).
                values(quantity=76)
            )
        )


def sale():
    with open("../images/default_icon_customer.png", "rb") as f:
        image = f.read()
    session = Session()
    products_class = []
    base_addres = AdressTable("Strada Carol I", 11, "Sibiu", "Sibiu", "Romania", "0742111226", "",
                              "ana.popescu@email.com", 1009)
    products = [("Laptop Dell", "Electronics", "piece", 10, 2500, "Deposit2", 5),
                ("Carte de colorat", "Consumabil", "buc", 50, 12, "Deposit1", 7),
                ("Tricou alb", "Vestimentar", "buc", 100, 30, "Deposit3", 7),
                ("Scaun de birou", "Mobila", "buc", 20, 500, "Deposit2", 9),
                ("Apa minerala", "Bauturi", "litru", 500, 3, "Deposit1", 5),
                ("Monitor Samsung", "Electronics", "piece", 5, 1800, "Deposit2", 10),
                ("Pantaloni negri", "Vestimentar", "buc", 30, 50, "Deposit3", 9),
                ("Mouse wireless", "Electronics", "piece", 15, 80, "Deposit2", 9),
                ("Pasta de dinti", "Ingrijire personala", "buc", 50, 15, "Deposit1", 9),
                ("Fier de calcat", "Electrocasnice", "buc", 5, 200, "Deposit2", 9),
                ("Cana de cafea", "Ustensile bucatarie", "buc", 25, 40, "Deposit1", 9),
                ("Set de periute de dinti", "Ingrijire personala", "set", 20, 30, "Deposit1", 9),
                ("Pisica de jucarie", "Jucarie", "buc", 100, 10, "Deposit1", 5),
                ("Bomboane", "Dulciuri", "kg", 2, 50, "Deposit1", 15),
                ("Rucsac negru", "Accesorii", "buc", 5, 100, "Deposit3", 9),
                ("Cizme de iarna", "Incaltaminte", "buc", 10, 300, "Deposit3", 9),
                ("Gel de dus", "Ingrijire personala", "buc", 30, 25, "Deposit1", 9),
                ("Cana cu infuzor", "Ustensile bucatarie", "buc", 20, 35, "Deposit1", 9),
                ("Caiet de matematica", "Papetarie", "buc", 50, 7, "Deposit1", 9),
                ("Rama foto", "Decoratiuni", "buc", 15, 20, "Deposit3", 9)]
    for row in products:
        products_class.append(ProductTable(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
    sale1 = SalesTable("S1001")
    sale2 = SalesTable("S1002")
    sale3 = SalesTable("S1003")
    client_sale_test = CustomersTable("Individual", "Cojocariu Daniel", image)
    client_sale_test.adress = base_addres
    sale1.client = client_sale_test
    sale1.product = [products_class[0], products_class[1]]

    price = 0
    for i in sale1.product:
        price += i.price * i.quantity
    sale1.total = price


    sale2.client = client_sale_test
    sale2.product = [products_class[2], products_class[3]]
    price = 0
    for i in sale2.product:
        price += i.price * i.quantity
    sale2.total = price

    sale3.client = client_sale_test

    sale3.product = [products_class[4], products_class[5]]
    price = 0
    for i in sale3.product:
        price += i.price * i.quantity
    sale3.total = price
    for i in products_class:
        session.add(i)
    session.add_all(
        [
            sale1, sale2, sale3
        ]
    )

    session.commit()
    session.close()


def populate_database():
    session = Session()

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with open("../images/default_icon_customer.png", "rb") as f:
        image = f.read()

    bankaccount1 = BankAccount("BRD", 52322400, 1)
    bankaccount2 = BankAccount("BRD2", 52322400, 1)

    client1 = CustomersTable("Fizica", "Maria Ion", image)

    adress1 = AdressTable("Strada Mihai Viteazu", 12, "Constanta", "Constanta", "Romania",
                          "0742111222", "", "maria.ion@email.com", 1001)


    client1.account = [bankaccount2, bankaccount1]

    client1.adress = adress1

    clients = [
        (CustomersTable("Fizic", "John Doe", image),
         AdressTable("Strada Mihai Eminescu", 10, "Cluj-Napoca", "Cluj", "România", "0722111222", "",
                     "john.doe@email.com", 1001)),
        (CustomersTable("Juridic", "ABC Company", image),
         AdressTable("Strada Victoriei", 15, "Brașov", "Brașov", "România", "0755333444", "", "contact@abccompany.com",
                     1002)),
        (CustomersTable("Fizic", "Alice Smith", image),
         AdressTable("Strada Aviatorilor", 8, "București", "București", "România", "0733444555", "",
                     "alice.smith@email.com", 1003)),
        (CustomersTable("Juridic", "XYZ Corporation", image),
         AdressTable("Strada Vasile Alecsandri", 5, "Iași", "Iași", "România", "0711222333", "", "info@xyzcorp.com",
                     1004)),
        (CustomersTable("Fizic", "Sarah Johnson", image),
         AdressTable("Strada Gheorghe Doja", 20, "Cluj-Napoca", "Cluj", "România", "0766777888", "",
                     "sarah.johnson@email.com", 1005)),
        (CustomersTable("Juridic", "123 Industries", image),
         AdressTable("Strada Fabricii", 30, "Timișoara", "Timiș", "România", "0744222333", "", "info@123industries.com",
                     1006)),
        (CustomersTable("Fizic", "Robert Brown", image),
         AdressTable("Strada Unirii", 12, "București", "București", "România", "0766333444", "",
                     "robert.brown@email.com", 1007)),
        (CustomersTable("Juridic", "Acme Corporation", image),
         AdressTable("Strada Ion Creangă", 7, "Iași", "Iași", "România", "0722333444", "", "contact@acmecorp.com",
                     1008)),
        (CustomersTable("Fizic", "Emma Wilson", image),
         AdressTable("Strada Republicii", 18, "Cluj-Napoca", "Cluj", "România", "0733555666", "",
                     "emma.wilson@email.com", 1009)),
        (CustomersTable("Fizic", "Emma Wilson", image),
         AdressTable("Strada Republicii", 18, "Cluj-Napoca", "Cluj", "România", "0733555666", "",
                     "emma.wilson@email.com", 1009)),
        (CustomersTable("Fizic", "Emma Wilson", image),
         AdressTable("Strada Republicii", 18, "Cluj-Napoca", "Cluj", "România", "0733555666", "",
                     "emma.wilson@email.com", 1009)),
        (CustomersTable("Fizic", "Emma Wilson", image),
         AdressTable("Strada Republicii", 18, "Cluj-Napoca", "Cluj", "România", "0733555666", "",
                     "emma.wilson@email.com", 1009)),
        (CustomersTable("Fizic", "Emma Wilson", image),
         AdressTable("Strada Republicii", 18, "Cluj-Napoca", "Cluj", "România", "0733555666", "",
                     "emma.wilson@email.com", 1009)),
        (CustomersTable("Fizic", "Emma Wilson", image),
         AdressTable("Strada Republicii", 18, "Cluj-Napoca", "Cluj", "România", "0733555666", "",
                     "emma.wilson@email.com", 1009)),
        (CustomersTable("Juridic", "Global Solutions", image),
         AdressTable("Strada Calea Dorobanților", 25, "București", "București", "România", "0711111222", "",
                     "contact@globalsolutions.com", 1010))
    ]
    for client_data in clients:
        client, address = client_data
        client.adress = address
        session.add(client)
        session.add(address)
    session.add(client1)
    sale()
    session.commit()
    session.close()


if __name__ == "__main__":
    delete_db()
    populate_database()
