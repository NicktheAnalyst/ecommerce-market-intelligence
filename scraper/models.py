from dataclasses import dataclass
from typing import Optional


@dataclass
class ProductRecord:
    competitor: str
    product_name: str
    brand: Optional[str]
    category: Optional[str]
    price: float
    currency: str
    rating: Optional[float]
    reviews: Optional[int]
    stock_status: str
    discount: Optional[float]
    product_url: str