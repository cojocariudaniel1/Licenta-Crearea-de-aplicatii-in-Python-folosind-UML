from account import Account
from base import Session, Base, engine
from client import Client


def delete_db():
    session = Session()
    Base.metadata.reflect(bind=engine)  # To reflect any tables in the DB, but not in the current schema
    Base.metadata.drop_all(bind=engine)
    session.commit()


def populate_database():
    session = Session()

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with open("../sprites/img.png", "rb") as f:
        image = f.read()
    # Creare client
    client_1 = Client("Fizica", "Cojocariu Daniel", "Strada Libertatea", 15, "Iasi", 'Iasi', "Romania", "0748827495",
                      "", "emrys7daniel@gmail.com", 24444, image)
    account_1 = Account("Bank1", 231111, 1)
    client_1.account = account_1

    client_2 = Client("Fizica", "Florin Florin", "Strada Sperantei", 132, "Iasi", 'Iasi', "Romanai", "072321232", "",
                      "florin@gmail.com", 32323, image)
    account_2 = Account("Bank2", 234231, 1)
    client_2.account = account_2

    client_3 = Client("Juridica", "Andrei Maximilian", "Strada Sfantul Andrei", 103, "Vaslui", 'Vaslui', "Romanai",
                      "072321234", "",
                      "andrei@gmail.com", 2111, image)
    account_3 = Account("Bank3", 2423221, 0)
    client_3.account = account_3

    session.add_all([
        client_1, client_2, client_3, account_1, account_2, account_3
    ])
    session.commit()
    session.close()


if __name__ == "__main__":
    delete_db()
    populate_database()
