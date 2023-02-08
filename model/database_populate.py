from base import Session, Base, engine
from client import Client
from account import Account


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

    client1 = Client("Fizica", "Maria Ion", "Strada Mihai Viteazu", 12, "Constanta", "Constanta", "Romania",
                     "0742111222", "", "maria.ion@email.com", 1001, image)

    client2 = Client("Juridic", "SC Compania SRL", "Strada Nicolae Balcescu", 22, "Bucuresti", "Bucuresti", "Romania",
                     "0758111222", "", "compania.srl@email.com", 1002, image)

    client3 = Client("Fizica", "Vasile Popescu", "Strada Aviatorilor", 17, "Cluj-Napoca", "Cluj", "Romania",
                     "0742111223", "", "vasile.popescu@email.com", 1003, image)

    client4 = Client("Juridic", "SA Compania Maritima", "Strada Portului", 1, "Constanta", "Constanta", "Romania",
                     "0758111223", "", "compania.maritima@email.com", 1004, image)

    client5 = Client("Fizica", "Elena Petrescu", "Strada Ion Creanga", 8, "Iasi", "Iasi", "Romania", "0742111224", "",
                     "elena.petrescu@email.com", 1005, image)

    client6 = Client("Juridic", "SC Compania IT", "Strada George Cosbuc", 15, "Bucuresti", "Bucuresti", "Romania",
                     "0758111224", "", "compania.it@email.com", 1006, image)

    client7 = Client("Fizica", "Andrei Stan", "Strada 1 Decembrie", 19, "Timisoara", "Timis", "Romania", "0742111225",
                     "", "andrei.stan@email.com", 1007, image)

    client8 = Client("Juridic", "SA Compania Constructii", "Strada Mihai Eminescu", 5, "Bucuresti", "Bucuresti",
                     "Romania", "0758111225", "", "compania.constructii@email.com", 1008, image)

    client9 = Client("Fizica", "Ana Maria Popescu", "Strada Carol I", 11, "Sibiu", "Sibiu", "Romania", "0742111226", "",
                     "ana.popescu@email.com", 1009, image)

    client10 = Client("Fizica", "Ana Alexa", "Strada Carol I", 11, "Sibiu", "Sibiu", "Romania", "0742111226", "",
                      "ana.popescu@email.com", 1009, image)
    #
    client11 = Client("Fizica", "Daniel Cojocariu", "Strada Carol I", 11, "Sibiu", "Sibiu", "Romania", "0742111226", "",
                      "ana.popescu@email.com", 1009, image)

    client12 = Client("Fizica", "Cosmin Hongu", "Strada Carol I", 11, "Sibiu", "Sibiu", "Romania", "0742111226", "",
                      "ana.popescu@email.com", 1009, image)

    client13 = Client("Fizica", "Danila Daniek", "Strada Carol I", 11, "Sibiu", "Sibiu", "Romania", "0742111226", "",
                      "ana.popescu@email.com", 1009, image)

    client14 = Client("Fizica", "Danila aaaaaa", "Strada Carol I", 11, "Sibiu", "Sibiu", "Romania", "0742111226", "",
                      "ana.popescu@email.com", 1009, image)

    client15 = Client("Fizica", "Danila bbbbb", "Strada Carol I", 11, "Sibiu", "Sibiu", "Romania", "0742111226", "",
                      "ana.popescu@email.com", 1009, image)

    client16 = Client("Fizica", "Danila cccc", "Strada Carol I", 11, "Sibiu", "Sibiu", "Romania", "0742111226", "",
                      "ana.popescu@email.com", 1009, image)
    session.add_all([client9, client8, client7, client6, client5])
    session.add_all([client1, client4, client3, client2, client10])
    session.add_all([client11, client13,client12, client14, client16, client15])
    for i in range(30):
        session.add(Client("Fizica", f"{i}0000 ", "Strada Carol I", 11, "Sibiu", "Sibiu", "Romania", "0742111226", "",
                      "ana.popescu@email.com", 1009, image))
    session.commit()
    session.close()


if __name__ == "__main__":
    delete_db()
    populate_database()
