from sqlalchemy.orm import Session
from database.models import (
    Product,
    Competitor,
    Price,
    DailySnapshot
)

class Repository:

    def __init__(self, session: Session):
        self.session = session

    def get_product_by_sku(self, sku: str):
        return (
            self.session.query(Product)
            .filter_by(sku=sku)
            .first()
        )

    def get_or_create_product(self, product_record):
        product = self.get_product_by_sku(product_record.sku)
        if product:
            return product
            
        product = Product(
            product_name=product_record.product_name,
            brand=product_record.brand,
            category=product_record.category,
            sku=product_record.sku
        )
        self.session.add(product)
        self.session.flush()
        return product

    def get_or_create_competitor(self, name: str, website: str, country: str):
        competitor = (
            self.session.query(Competitor)
            .filter_by(name=name)
            .first()
        )
        if competitor:
            return competitor
            
        competitor = Competitor(
            name=name,
            website=website,
            country=country
        )
        self.session.add(competitor)
        self.session.flush()
        return competitor

    def insert_price(self, product, competitor, record):
        price = Price(
            product_id=product.id,
            competitor_id=competitor.id,
            price=record.price,
            currency=record.currency,
            discount=record.discount
        )
        self.session.add(price)
        self.session.flush()
        return price

    def insert_snapshot(self, product, competitor, record):
        snapshot = DailySnapshot(
            product_id=product.id,
            competitor_id=competitor.id,
            rating=record.rating,
            reviews=record.reviews,
            stock_status=record.stock_status,
            shipping_cost=record.shipping_cost,
            exchange_rate=record.exchange_rate
        )
        self.session.add(snapshot)
        self.session.flush()
        return snapshot