from sqlalchemy import Column, String, Integer, ForeignKey  # Import library sql
from sqlalchemy.orm import relationship
from base import Base


class BankAccount(Base):
    __tablename__ = "account"

    id = Column(Integer, primary_key=True)
    bank = Column(String)
    account_number = Column(Integer)
    send_money = Column(Integer)

    customer_id = Column(Integer, ForeignKey("customer.id"))
    customer = relationship("CustomersTable", back_populates="account")

    def __init__(self, bank, account_number, send_money):
        self.bank = bank
        self.account_number = account_number
        self.send_money = send_money

