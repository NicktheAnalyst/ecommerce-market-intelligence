import time
from scraper.jumia_scraper import JumiaScraper
from utils.logger import logger

def main():
    scraper = JumiaScraper()
    
    # Step 10: Performance Monitoring Metric Timing Wrapper
    start = time.perf_counter()
    
    scraped_data = scraper.scrape()
    
    elapsed = time.perf_counter() - start
    
    # Log performance results to analytics stream
    logger.info(f"{scraper.__class__.__name__} completed in {elapsed:.2f} seconds.")
    
    print(f"\nSuccessfully collected {len(scraped_data)} structured entries.")
    print(f"Time Taken: {elapsed:.2f}s")

if __name__ == "__main__":
    main()