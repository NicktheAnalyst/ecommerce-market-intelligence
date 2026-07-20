# analysis/models.py
from dataclasses import dataclass, field
from decimal import Decimal
import hashlib
from typing import Optional

@dataclass
class ProductRecord:
    product_name: str
    price: Decimal
    currency: str
    competitor: str
    original_price: Optional[Decimal] = None
    rating: float = 0.0
    review_count: int = 0
    
    # Enrichment fields
    exchange_rate: Optional[Decimal] = None
    price_kes: Optional[Decimal] = None
    discount_percentage: int = 0
    shipping_cost: Decimal = Decimal("0.00")
    category: str = "Unclassified"
    
    @property
    def product_id(self) -> str:
        """Generates a unique deterministic ID to handle upsert conflict matches."""
        unique_string = f"{self.product_name}_{self.competitor}_{self.currency}"
        return hashlib.md5(unique_string.encode('utf-8')).hexdigest()