from sqlalchemy import Column, String, Integer, LargeBinary, ForeignKey  # Import library sql
from sqlalchemy.orm import relationship
from bankaccount import BankAccount
from base import Base
from sales import SalesTable


class AdressTable(Base):
    __tablename__ = "adress"

    id = Column(Integer, primary_key=True)
    street = Column(String)
    street_number = Column(Integer)
    city = Column(String)
    district = Column(String)
    country = Column(String)
    phone = Column(Integer)
    web_site = Column(String)
    email = Column(String)
    zip_code = Column(Integer)
    customer = relationship("CustomersTable", back_populates="adress", uselist=False)

    customer_id = Column(Integer, ForeignKey("customer.id"))

    def __init__(self, street, street_number, city, district, country, phone, web_site, email,
                 zip_code):
        self.street = street
        self.street_number = street_number
        self.city = city
        self.district = district
        self.country = country
        self.phone = phone
        self.web_site = web_site
        self.email = email
        self.zip_code = zip_code
