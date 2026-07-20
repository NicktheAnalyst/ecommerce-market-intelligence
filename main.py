# main.py
from decimal import Decimal
from analysis.models import ProductRecord
from analysis.etl import ETLProcessor
from analysis.database import DatabaseLoader
from utils.logger import logger

def main():
    # 1. Initialize our ETL Engine and Database Pipeline Components
    processor = ETLProcessor()
    
    # Adjust connection string credentials to match your local setup
    db_loader = DatabaseLoader("postgresql://postgres:postgres@localhost:5432/market_intelligence")

    # 2. Emulate an active raw scraper production stream using Decimals
    raw_scraped_items = [
        ProductRecord(
            product_name="iPhone 16 Pro Max", 
            price=Decimal("1199.00"), 
            original_price=Decimal("1400.00"), 
            currency="USD", 
            competitor="Amazon Global",
            rating=4.8,
            review_count=940
        ),
        ProductRecord(
            product_name="MacBook Air M3", 
            price=Decimal("999.00"), 
            original_price=Decimal("999.00"), 
            currency="USD", 
            competitor="BestBuy US",
            rating=4.6,
            review_count=210
        )
    ]

    # 3. Process, Clean, and Enrich Records
    processed_batch = []
    print("\n--- Running End-to-End ETL Processing Pipeline ---")
    
    for item in raw_scraped_items:
        try:
            enriched_item = processor.enrich(item)
            processed_batch.append(enriched_item)
            print(f"✅ Processed: {enriched_item.product_name} | Price: {enriched_item.price_kes} KES | ID: {enriched_item.product_id[:8]}...")
        except ValueError as val_err:
            logger.error(f"❌ Record Rejected: {val_err}")

    # 4. Save safely to the PostgreSQL layer using batch transactions
    if processed_batch:
        print("\n--- Initiating Transactional Database Loading ---")
        try:
            db_loader.upsert_batch(processed_batch)
            print("🚀 Pipeline Execution Completed Successfully!")
        except Exception as db_err:
            print(f"💥 Critical Pipeline Halt: {db_err}")

if __name__ == "__main__":
    main()