from api.cache import cache
from api.exchange_rate import ExchangeRateClient
from api.shipping import ShippingClient
from api.category import CategoryClient
from utils.logger import logger

class DataTransformer:
    def __init__(self):
        self.exchange_client = ExchangeRateClient()
        self.shipping_client = ShippingClient()
        self.category_client = CategoryClient()

    def get_cached_rates(self):
        """Fetches exchange rates once and caches them for the entire run."""
        if "rates" not in cache:
            logger.info("Cache miss: Fetching fresh exchange rates from API...")
            cache["rates"] = self.exchange_client.get_rates()
        return cache["rates"]

    def calculate_discount_percentage(self, original_price: float, current_price: float) -> int:
        """Calculates relative price drops cleanly as a whole percentage integer."""
        if not original_price or original_price <= 0 or current_price >= original_price:
            return 0
        discount = ((original_price - current_price) / original_price) * 100
        return int(round(discount))

    def enrich_record(self, raw_record: dict, base_currency: str = "KES") -> dict:
        """Transforms currencies, calculates discounts, and merges metadata metrics."""
        try:
            rates = self.get_cached_rates()
            product_name = raw_record.get("product_name", "")
            
            # Step 6: Multi-Currency Normalization/Data Transformation
            input_currency = raw_record.get("currency", "USD")
            raw_price = float(raw_record.get("price", 0))
            
            if input_currency == base_currency:
                exchange_rate = 1.0
                price_normalized = raw_price
            else:
                # Calculate cross-rate relative to USD base matrix values
                target_rate = float(rates.get(base_currency, 150.0))
                source_rate = float(rates.get(input_currency, 1.0))
                exchange_rate = target_rate / source_rate
                price_normalized = raw_price * exchange_rate

            # Step 7: Discount Calculation
            original_price = float(raw_record.get("original_price", 0))
            current_price = raw_price
            discount_pct = self.calculate_discount_percentage(original_price, current_price)

            # Context-Aware External API Enrichment Lookups
            shipping_cost = self.shipping_client.get_shipping_cost("Kenya") or 0.0
            category = self.category_client.get_category(product_name) or "Unclassified"

            # Step 8: Return Enriched Product Records Data Structure
            return {
                "product_name": product_name,
                "price": current_price,
                "currency": input_currency,
                "exchange_rate": round(exchange_rate, 4),
                "price_kes": round(price_normalized, 2),
                "discount_percentage": discount_pct,
                "shipping_cost": shipping_cost,
                "category": category,
                "competitor": raw_record.get("competitor", "Unknown")
            }
        except Exception as err:
            logger.error(f"Failed to enrich record line item: {err}")
            return raw_record