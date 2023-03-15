from sqlalchemy import Column, String, Integer, LargeBinary, Date, Table, ForeignKey
from sqlalchemy.orm import relationship

from base import Base


class ProductTable(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True)
    product_name = Column(String)
    product_type = Column(String)
    unit_of_measure = Column(String)
    quantity = Column(Integer)
    price = Column(Integer)
    deposit = Column(String)

    def __init__(self, product_name, product_type, unit_of_measure, quantity, price, deposit):
        self.product_name = product_name
        self.product_type = product_type
        self.unit_of_measure = unit_of_measure
        self.quantity = quantity
        self.price = price
        self.deposit = deposit




