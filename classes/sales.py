from sqlalchemy import Column, String, Integer, LargeBinary, Date, ForeignKey, Table, Float
from sqlalchemy.orm import relationship

from base import Base
from datetime import date

class SalesTable(Base):
    __tablename__ = "sale"


    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customer.id"))
    number = Column(String)
    creation_date = Column(Date)
    total = Column(Float)
    customer = relationship('CustomersTable', back_populates="sale")
    product = relationship("ProductTable", secondary='saleproducts')

    def __init__(self, number, creation_date = date.today()):
        self.number = number
        self.creation_date = creation_date

