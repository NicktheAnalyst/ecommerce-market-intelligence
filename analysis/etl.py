# analysis/etl.py
from decimal import Decimal, ROUND_HALF_UP
from analysis.models import ProductRecord
from analysis.validators import DataValidator
from api.exchange_rate import ExchangeRateClient
from api.cache import cache
from utils.logger import logger

class ETLProcessor:
    def __init__(self):
        self.exchange_client = ExchangeRateClient()

    def _get_rates(self) -> dict:
        if "rates" not in cache:
            rates = self.exchange_client.get_rates()
            if not rates:
                logger.warning("Exchange API down. Using default USD/KES baseline mappings.")
                rates = {"USD": 1.0, "KES": 150.0}
            # Convert rates to Decimals for exact arithmetic
            cache["rates"] = {k: Decimal(str(v)) for k, v in rates.items()}
        return cache["rates"]

    def _determine_category(self, name: str) -> str:
        """Mentor Recommendation: Internal rules map instead of network calls."""
        name_lower = name.lower()
        if "iphone" in name_lower or "galaxy" in name_lower or "phone" in name_lower:
            return "Smartphones"
        if "macbook" in name_lower or "laptop" in name_lower:
            return "Laptops"
        return "Electronics"

    def _calculate_mock_shipping(self, category: str) -> Decimal:
        """Mentor Recommendation: Reproducible developer mock calculation rules."""
        shipping_table = {
            "Smartphones": Decimal("15.00"),
            "Laptops": Decimal("35.00"),
            "Electronics": Decimal("20.00")
        }
        return shipping_table.get(category, Decimal("10.00"))

    def enrich(self, product: ProductRecord) -> ProductRecord:
        # Step 10: Validation
        DataValidator.validate(product)

        # Step 6 & 12: Currency Transformation using Decimals
        rates = self._get_rates()
        base_currency = "KES"
        
        target_rate = rates.get(base_currency, Decimal("150.0"))
        source_rate = rates.get(product.currency, Decimal("1.0"))
        
        product.exchange_rate = (target_rate / source_rate).quantize(Decimal("1.0000"))
        product.price_kes = (product.price * product.exchange_rate).quantize(Decimal("1.00"), rounding=ROUND_HALF_UP)

        # Step 7: Precision Discount Math
        if product.original_price and product.original_price > product.price:
            discount = ((product.original_price - product.price) / product.original_price) * 100
            product.discount_percentage = int(discount.quantize(Decimal("1"), rounding=ROUND_HALF_UP))

        # Internal Lookups
        product.category = self._determine_category(product.product_name)
        product.shipping_cost = self._calculate_mock_shipping(product.category)

        return product