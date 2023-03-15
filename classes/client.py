from sqlalchemy import Column, String, Integer, LargeBinary  # Import library sql
from sqlalchemy.orm import relationship
from bankaccount import BankAccount
from base import Base
from sales import SalesTable


class ClientTable(Base):
    __tablename__ = "client"

    id = Column(Integer, primary_key=True)
    type_client = Column(String)
    name = Column(String, nullable=False)
    street = Column(String)
    street_number = Column(Integer)
    city = Column(String)
    district = Column(String)
    country = Column(String)
    phone = Column(Integer)
    web_site = Column(String)
    email = Column(String)
    zip_code = Column(Integer)
    image = Column(LargeBinary)
    account = relationship("BankAccount", back_populates="client", uselist=False)
    sale = relationship("SalesTable", back_populates="client")

    def __init__(self, type_client, name, street, street_number, city, district, country, phone, web_site, email,
                 zip_code, image ):
        self.type_client = type_client
        self.name = name
        self.street = street
        self.street_number = street_number
        self.city = city
        self.district = district
        self.country = country
        self.phone = phone
        self.web_site = web_site
        self.email = email
        self.zip_code = zip_code
        self.image = image
