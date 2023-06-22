from sqlalchemy import Column, String, Integer, LargeBinary  # Import library sql
from sqlalchemy.orm import relationship
from bankaccount import BankAccount
from base import Base
from sales import SalesTable
from adress import AdressTable

class CustomersTable(Base):
    __tablename__ = "customer"

    id = Column(Integer, primary_key=True)
    type_client = Column(String)
    name = Column(String, nullable=False)
    image = Column(LargeBinary)
    account = relationship("BankAccount", back_populates="customer")
    sale = relationship("SalesTable", back_populates="customer")
    adress = relationship("AdressTable", back_populates="customer", uselist=False)
    def __init__(self, type_customer, name, image):
        self.type_client = type_customer
        self.name = name
        self.image = image
