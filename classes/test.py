from sqlalchemy import update

from SalesProduct import SaleProducts
from base import Session


def run():
    session = Session()

    stmt = (
        update(SaleProducts).
        where(SaleProducts.sales_id == 1, SaleProducts.product_id == 3).
        values(quantity=76)
    )
    session.execute(stmt)
    session.commit()
    session.close()


run()
