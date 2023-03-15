from sqlalchemy import Column, String, Integer, LargeBinary, Date, ForeignKey, Float, Table
from sqlalchemy.orm import relationship
from base import Base
from datetime import date


class InvoicingTable(Base):
    __tablename__ = "invoice"

    id = Column(Integer, primary_key=True)
    sale_id = Column(Integer, ForeignKey('sale.id'))
    number = Column(String)
    creation_date = Column(Date)
    total_payment = Column(Float)

    sale = relationship("SalesTable", back_populates="invoice")

    def __init__(self, number, creation_date=date.today):
        self.number = number
        self.creation_date = creation_date

