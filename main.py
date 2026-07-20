# main.py
import json
from analysis.models import ProductRecord
from analysis.etl import ETLProcessor
from utils.logger import logger

def main():
    # Initialize the centralized ETL Engine
    processor = ETLProcessor()

    # Simulated raw data payload extracted from a Playwright browser instance
    raw_scraped_items = [
        ProductRecord(
            product_name="iPhone 16", 
            price=899.0, 
            original_price=1200.0, 
            currency="USD", 
            competitor="Amazon",
            rating=4.7,
            review_count=142
        ),
        ProductRecord(
            product_name="Invalid Price Item", 
            price=-5.0, 
            currency="USD", 
            competitor="eBay Store"
        )
    ]

    print("--- Running ETL Pipeline Flow ---")
    enriched_results = []
    
    for item in raw_scraped_items:
        try:
            # The first item will trigger the API lookup, the subsequent ones reuse the cache!
            enriched_item = processor.enrich(item)
            print(f"✅ Success: {enriched_item.product_name} | Price KES: {enriched_item.price_kes}")
            
            # Convert the enriched dataclass object to a dict for previewing
            enriched_results.append(enriched_item.__dict__)
            
        except ValueError as val_err:
            # Catches Step 10 validation failures before they hit dashboards/databases
            logger.error(f"❌ Skipping bad record: {val_err}")

    print("\n--- Processed Output Sample ---")
    if enriched_results:
        print(json.dumps(enriched_results[0], indent=4))

if __name__ == "__main__":
    main()