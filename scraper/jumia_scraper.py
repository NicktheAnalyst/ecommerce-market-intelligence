import time
from scraper.base_scraper import BaseScraper
from scraper.selectors import SELECTORS
from utils.logger import logger

class JumiaScraper(BaseScraper):
    URL = "https://www.jumia.co.ke/catalog/?q=laptop"
    MAX_RETRIES = 3

    def __init__(self):
        super().__init__()
        # Step 6: Map site-specific configurations
        self.config = SELECTORS["jumia"]

    def clean_price(self, price_str: str) -> float:
        try:
            cleaned = price_str.replace("KSh", "").replace(",", "").strip()
            return float(cleaned)
        except (ValueError, TypeError):
            return 0.0

    # Step 7: Validate Scraped Data helper
    def validate_record(self, record: dict) -> bool:
        if not record.get("product_name"):
            return False
        if record.get("price", 0) <= 0:
            return False
        return True

    # Step 8 & 9: Isolated Extraction Sequence
    def extract_product(self, product_element) -> dict:
        name = product_element.locator(self.config["name"]).inner_text()
        
        raw_price = product_element.locator(self.config["price"]).inner_text()
        price = self.clean_price(raw_price)
        
        badge = product_element.locator(self.config["discount"]).first
        discount = badge.inner_text() if badge.count() else None

        return {
            "product_name": name,
            "price": price,
            "discount": discount,
            "competitor": "Jumia"
        }

    def scrape(self):
        logger.info("Launching browser session...")
        self.start()
        
        for attempt in range(self.MAX_RETRIES):
            try:
                self.page.goto(self.URL, timeout=60000)
                break
            except Exception as e:
                if attempt == self.MAX_RETRIES - 1:
                    logger.critical(f"Failed to navigate: {e}")
                    self.close()
                    raise e
                time.sleep(attempt + 1)

        results = []
        page_num = 1

        while True:
            self.page.wait_for_load_state("networkidle")
            self.page.locator(self.config["product"]).first.wait_for()

            products = self.page.locator(self.config["product"]).all()

            for product in products:
                # Step 8: Handle Website-Specific Errors at individual item levels
                try:
                    record = self.extract_product(product)
                    
                    # Step 7: Data Integrity Validation layer check
                    if self.validate_record(record):
                        results.append(record)
                    else:
                        logger.warning(f"Skipping corrupt structural record payload: {record}")
                        
                except Exception as error:
                    logger.warning(f"Skipping single product card parse exception: {error}")

            next_button = self.page.locator("a[aria-label='Next']")
            if next_button.count() == 0:
                break
            
            next_button.first.click()
            page_num += 1

        self.close()
        return results