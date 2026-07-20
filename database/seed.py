from database.base import Base, engine
from database.crud import (
    create_competitor,
    create_product,
    create_price
)
# Make sure your models are imported here so SQLAlchemy detects the tables!
# from database import models 

def seed_database():
    # 1. Create the tables first
    Base.metadata.create_all(bind=engine)
    
    try:
        print("Seeding database...")
        
        # 2. Seed Competitor (No 'session' argument needed here)
        amazon = create_competitor(
            "Amazon",
            "https://amazon.com",
            "USA"
        )

        # 3. Seed Product
        iphone = create_product(
            "iPhone 16",
            "Apple",
            "Smartphones",
            "APL-IP16"
        )

        # 4. Seed Price linked to both
        create_price(
            iphone.id,
            amazon.id,
            135000,
            "KES",
            10
        )

        print("Database successfully seeded with product and price data!")
        
    except Exception as e:
        print(f"An error occurred while seeding: {e}")

if __name__ == "__main__":
    seed_database()