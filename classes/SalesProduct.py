from sqlalchemy import Column, String, Integer, LargeBinary, ForeignKey  # Import library sql
from sqlalchemy.orm import relationship
from product import ProductTable
from base import Base


class SaleProducts(Base):
    __tablename__ = "saleproducts"
    id = Column(Integer, primary_key = True)
    sales_id = Column(Integer, ForeignKey('sale.id'))
    product_id = Column(Integer, ForeignKey('product.id'))
    quantity = Column(Integer)


