from bankaccount import BankAccount
from base import Session



def create_bank(data):

    new_bank = BankAccount(data[0], data[1], data[2])

    return new_bank
