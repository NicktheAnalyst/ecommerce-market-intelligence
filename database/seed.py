from database.base import Base
from database.connection import engine, SessionLocal
from database.crud import (
    create_competitor,
    create_product,
    create_price
)
from database.models import DailySnapshot
import database.models

def seed_database():
    try:
        print("Recreating PostgreSQL schema...")
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        
        print("Seeding PostgreSQL database...")
        amazon = create_competitor("Amazon", "https://amazon.com", "USA")
        jumia = create_competitor("Jumia", "https://jumia.co.ke", "KE")
        
        iphone = create_product("iPhone 16", "Apple", "Smartphones", "APL-IP16")
        samsung = create_product("Galaxy S24", "Samsung", "Smartphones", "SAM-S24")

        # 1. Historical & Current Prices
        create_price(iphone.id, amazon.id, 140000, "KES", 0)   # Old price
        create_price(iphone.id, amazon.id, 135000, "KES", 10)  # Current price
        create_price(samsung.id, jumia.id, 110000, "KES", 15)

        # 2. Daily Snapshots (With required non-null fields)
        session = SessionLocal()
        snapshot1 = DailySnapshot(
            product_id=iphone.id,
            competitor_id=amazon.id,
            stock_status="out_of_stock",
            rating=4.5,
            reviews=120,
            shipping_cost=500.0,
            exchange_rate=1.0
        )
        snapshot2 = DailySnapshot(
            product_id=samsung.id,
            competitor_id=jumia.id,
            stock_status="out_of_stock",
            rating=4.8,
            reviews=85,
            shipping_cost=300.0,
            exchange_rate=1.0
        )
        session.add_all([snapshot1, snapshot2])
        session.commit()
        session.close()

        print("PostgreSQL database fully seeded with rich historical & snapshot data!")
        
    except Exception as e:
        print(f"An error occurred while seeding: {e}")

if __name__ == "__main__":
    seed_database()