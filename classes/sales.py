from sqlalchemy import Column, String, Integer, LargeBinary, Date, ForeignKey, Table, Float
from sqlalchemy.orm import relationship

from base import Base
from datetime import date

class SalesTable(Base):
    __tablename__ = "sale"


    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("client.id"))
    number = Column(String)
    creation_date = Column(Date)
    total = Column(Float)
    client = relationship('ClientTable', back_populates="sale")
    invoice = relationship("InvoicingTable")
    product = relationship("ProductTable", secondary='saleproducts')

    def __init__(self, number, creation_date = date.today()):
        self.number = number
        self.creation_date = creation_date

