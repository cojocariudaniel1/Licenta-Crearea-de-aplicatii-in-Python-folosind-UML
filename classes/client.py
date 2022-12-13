from sqlalchemy import Column, String, Integer  # Import library sql

from base import Base


class Client(Base):
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

    def __init__(self, type_client, name, street, street_number, city, district, country, phone, web_site, email):
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
