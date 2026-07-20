from analysis.models import ProductRecord
from analysis.validators import DataValidator
from api.exchange_rate import ExchangeRateClient
from api.shipping import ShippingClient
from api.category import CategoryClient
from api.cache import cache
from utils.logger import logger

class ETLProcessor:
    def __init__(self):
        self.exchange_client = ExchangeRateClient()
        self.shipping_client = ShippingClient()
        self.category_client = CategoryClient()

    def _get_rates(self) -> dict:
        """Fetches from API with a fallback matrix if the external endpoint fails."""
        if "rates" not in cache:
            rates = self.exchange_client.get_rates()
            # Step 12: Fallback handling if API is down or unavailable
            if not rates:
                logger.warning("Exchange rate API unavailable! Utilizing fallback rate (1.0).")
                rates = {"USD": 1.0, "KES": 150.0}
            cache["rates"] = rates
        return cache["rates"]

    def enrich(self, product: ProductRecord) -> ProductRecord:
        """Executes the full pipeline: Validation -> Transformation -> Enrichment."""
        # Step 10: Run structural gate validation checks first
        DataValidator.validate(product)

        # Step 9 & 12: Business logic calculation and API failure handling
        rates = self._get_rates()
        
        # Determine exchange rates cleanly
        base_currency = "KES"
        target_rate = float(rates.get(base_currency, 150.0))
        source_rate = float(rates.get(product.currency, 1.0))
        
        product.exchange_rate = round(target_rate / source_rate, 4)
        product.price_kes = round(product.price * product.exchange_rate, 2)

        # Calculate discount rules safely
        if product.original_price and product.original_price > product.price:
            discount = ((product.original_price - product.price) / product.original_price) * 100
            product.discount_percentage = int(round(discount))

        # Enforce fallbacks for downstream shipping and categorization modules
        raw_shipping = self.shipping_client.get_shipping_cost("Kenya")
        product.shipping_cost = raw_shipping if raw_shipping is not None else 0.0

        raw_category = self.category_client.get_category(product.product_name)
        product.category = raw_category if raw_category else "Unclassified"

        return product