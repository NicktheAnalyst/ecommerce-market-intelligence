from analysis.models import ProductRecord

class DataValidator:
    @staticmethod
    def validate(product: ProductRecord) -> bool:
        """Runs integrity validation checks on raw scraped product frames."""
        if not product.product_name or not product.product_name.strip():
            raise ValueError("Invalid Data: Missing product name.")
            
        if product.price <= 0:
            raise ValueError("Invalid Data: Invalid price.")
            
        if not product.competitor or not product.competitor.strip():
            raise ValueError("Invalid Data: Missing competitor info.")
            
        if product.rating < 0:
            raise ValueError("Invalid Data: Negative ratings encountered.")
            
        if product.review_count < 0:
            raise ValueError("Invalid Data: Invalid review counts.")
            
        return True