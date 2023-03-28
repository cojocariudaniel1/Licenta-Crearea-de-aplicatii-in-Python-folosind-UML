from sqlalchemy import insert, update

from base import Session, Base, engine
from client import ClientTable
from invoicing import InvoicingTable
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
    session = Session()
    products_class = []

    products = [("Laptop Dell", "Electronics", "piece", 10, 2500, "Deposit2", 20),
                ("Carte de colorat", "Consumabil", "buc", 50, 12, "Deposit1", 9),
                ("Tricou alb", "Vestimentar", "buc", 100, 30, "Deposit3", 5),
                ("Scaun de birou", "Mobila", "buc", 20, 500, "Deposit2", 15),
                ("Apa minerala", "Bauturi", "litru", 500, 3, "Deposit1", 10),
                ("Monitor Samsung", "Electronics", "piece", 5, 1800, "Deposit2", 20),
                ("Pantaloni negri", "Vestimentar", "buc", 30, 50, "Deposit3", 5),
                ("Mouse wireless", "Electronics", "piece", 15, 80, "Deposit2", 10),
                ("Pasta de dinti", "Ingrijire personala", "buc", 50, 15, "Deposit1", 5),
                ("Fier de calcat", "Electrocasnice", "buc", 5, 200, "Deposit2", 20),
                ("Cana de cafea", "Ustensile bucatarie", "buc", 25, 40, "Deposit1", 7),
                ("Set de periute de dinti", "Ingrijire personala", "set", 20, 30, "Deposit1", 5),
                ("Pisica de jucarie", "Jucarie", "buc", 100, 10, "Deposit1", 5),
                ("Bomboane", "Dulciuri", "kg", 2, 50, "Deposit1", 15),
                ("Rucsac negru", "Accesorii", "buc", 5, 100, "Deposit3", 10),
                ("Cizme de iarna", "Incaltaminte", "buc", 10, 300, "Deposit3", 10),
                ("Gel de dus", "Ingrijire personala", "buc", 30, 25, "Deposit1", 5),
                ("Cana cu infuzor", "Ustensile bucatarie", "buc", 20, 35, "Deposit1", 7),
                ("Caiet de matematica", "Papetarie", "buc", 50, 7, "Deposit1", 5),
                ("Rama foto", "Decoratiuni", "buc", 15, 20, "Deposit3", 5)]
    for row in products:
        products_class.append(ProductTable(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
    sale1 = SalesTable("S1001")
    sale2 = SalesTable("S1002")
    sale3 = SalesTable("S1003")

    sale1.client = ClientTable("Individual", "Cojocariu Daniel", "Libertatea", 5, "Iasi", "Iasi", "Romania", 74213211,
                               "None", "daniel@gmail.com", 343123, None)
    sale1.product = [products_class[0], products_class[1]]
    price = 0
    for i in sale1.product:
        price += i.price * i.quantity
    sale1.total = price
    sale2.client = ClientTable("Fizica", "Danila Daniel", "Sperantei", 5, "Iasi", "Iasi", "Romanai", 72313131, "None",
                               "danila@gmail.com", 331213, None)
    sale2.product = [products_class[2], products_class[3]]
    price = 0
    for i in sale2.product:
        price += i.price * i.quantity
    sale2.total = price

    sale3.client = ClientTable("Fizica", "Danila Daniel", "Sperantei", 5, "Iasi", "Iasi", "Romanai", 72313131, "None",
                               "danila@gmail.com", 331213, None)
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
    with open("../sprites/img.png", "rb") as f:
        image = f.read()

    bankaccount1 = BankAccount("BRD", 52322400, 1)

    client1 = ClientTable("Fizica", "Maria Ion", "Strada Mihai Viteazu", 12, "Constanta", "Constanta", "Romania",
                          "0742111222", "", "maria.ion@email.com", 1001, image)

    client1.account = bankaccount1

    client2 = ClientTable("Juridic", "SC Compania SRL", "Strada Nicolae Balcescu", 22, "Bucuresti", "Bucuresti",
                          "Romania",
                          "0758111222", "", "compania.srl@email.com", 1002, image)

    client3 = ClientTable("Fizica", "Vasile Popescu", "Strada Aviatorilor", 17, "Cluj-Napoca", "Cluj", "Romania",
                          "0742111223", "", "vasile.popescu@email.com", 1003, image)

    client4 = ClientTable("Juridic", "SA Compania Maritima", "Strada Portului", 1, "Constanta", "Constanta", "Romania",
                          "0758111223", "", "compania.maritima@email.com", 1004, image)

    client5 = ClientTable("Fizica", "Elena Petrescu", "Strada Ion Creanga", 8, "Iasi", "Iasi", "Romania", "0742111224",
                          "",
                          "elena.petrescu@email.com", 1005, image)

    client6 = ClientTable("Juridic", "SC Compania IT", "Strada George Cosbuc", 15, "Bucuresti", "Bucuresti", "Romania",
                          "0758111224", "", "compania.it@email.com", 1006, image)

    client7 = ClientTable("Fizica", "Andrei Stan", "Strada 1 Decembrie", 19, "Timisoara", "Timis", "Romania",
                          "0742111225",
                          "", "andrei.stan@email.com", 1007, image)

    client8 = ClientTable("Juridic", "SA Compania Constructii", "Strada Mihai Eminescu", 5, "Bucuresti", "Bucuresti",
                          "Romania", "0758111225", "", "compania.constructii@email.com", 1008, image)

    client9 = ClientTable("Fizica", "Ana Maria Popescu", "Strada Carol I", 11, "Sibiu", "Sibiu", "Romania",
                          "0742111226", "",
                          "ana.popescu@email.com", 1009, image)

    client10 = ClientTable("Fizica", "Ana Alexa", "Strada Carol I", 11, "Sibiu", "Sibiu", "Romania", "0742111226", "",
                           "ana.popescu@email.com", 1009, image)
    #
    client11 = ClientTable("Fizica", "Daniel Cojocariu", "Strada Carol I", 11, "Sibiu", "Sibiu", "Romania",
                           "0742111226", "",
                           "ana.popescu@email.com", 1009, image)

    client12 = ClientTable("Fizica", "Cosmin Hongu", "Strada Carol I", 11, "Sibiu", "Sibiu", "Romania", "0742111226",
                           "",
                           "ana.popescu@email.com", 1009, image)

    client13 = ClientTable("Fizica", "Danila Daniek", "Strada Carol I", 11, "Sibiu", "Sibiu", "Romania", "0742111226",
                           "",
                           "ana.popescu@email.com", 1009, image)

    client14 = ClientTable("Fizica", "Danila aaaaaa", "Strada Carol I", 11, "Sibiu", "Sibiu", "Romania", "0742111226",
                           "",
                           "ana.popescu@email.com", 1009, image)

    client15 = ClientTable("Fizica", "Danila bbbbb", "Strada Carol I", 11, "Sibiu", "Sibiu", "Romania", "0742111226",
                           "",
                           "ana.popescu@email.com", 1009, image)

    client16 = ClientTable("Fizica", "Danila cccc", "Strada Carol I", 11, "Sibiu", "Sibiu", "Romania", "0742111226", "",
                           "ana.popescu@email.com", 1009, image)
    session.add_all([client9, client8, client7, client6, client5])
    session.add_all([client1, client4, client3, client2, client10])
    session.add_all([client11, client13, client12, client14, client16, client15])
    for i in range(30):
        session.add(
            ClientTable("Fizica", f"{i}0000 ", "Strada Carol I", 11, "Sibiu", "Sibiu", "Romania", "0742111226", "",
                        "ana.popescu@email.com", 1009, image))
    sale()
    session.commit()
    session.close()


if __name__ == "__main__":
    delete_db()
    populate_database()
