from database.connection import SessionLocal
from database.models import Competitor


def create_competitor(name, website, country):
    session = SessionLocal()

    competitor = Competitor(
        name=name,
        website=website,
        country=country
    )

    session.add(competitor)
    session.commit()
    session.refresh(competitor)
    session.close()

    return competitor

from database.models import Product, Price
from database.base import SessionLocal  

def create_product(product_name, brand, category, sku):
    session = SessionLocal()
    product = Product(
        product_name=product_name,
        brand=brand,
        category=category,
        sku=sku
    )
    session.add(product)
    session.commit()
    session.refresh(product)
    session.close()
    return product

def create_price(product_id, competitor_id, price, currency, discount):
    session = SessionLocal()
    new_price = Price(
        product_id=product_id,
        competitor_id=competitor_id,
        price=price,
        currency=currency,
        discount=discount
    )
    session.add(new_price)
    session.commit()
    session.refresh(new_price)
    session.close()
    return new_price