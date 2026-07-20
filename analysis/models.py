from dataclasses import dataclass, field
from typing import Optional

@dataclass
class ProductRecord:
    product_name: str
    price: float
    currency: str
    competitor: str
    original_price: Optional[float] = None
    rating: float = 0.0
    review_count: int = 0
    
    # Enrichment fields populated by ETL
    exchange_rate: Optional[float] = None
    price_kes: Optional[float] = None
    discount_percentage: int = 0
    shipping_cost: float = 0.0
    category: str = "Unclassified"