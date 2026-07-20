# analysis/analytics_engine.py
import pandas as pd
from analysis.data_loader import DataLoader

class AnalyticsEngine:

    def __init__(self):
        # Initialize loader and pull data across the database layer once
        loader = DataLoader()
        
        self.products = loader.load_products()
        self.prices = loader.load_prices()
        self.snapshots = loader.load_snapshots()
        self.competitors = loader.load_competitors()

    def get_readable_prices(self) -> pd.DataFrame:
        """
        Joins raw prices with product names to make datasets readable.
        Converts 'product_id' columns into actual product names.
        """
        merged = self.prices.merge(
            self.products,
            left_on="product_id",
            right_on="id"
        )
        return merged

    def get_average_price(self, target_df: pd.DataFrame) -> float:
        """
        Demonstrates Step 2: Quickly calculating statistical aggregates
        like average means out of a Pandas DataFrame.
        """
        average = target_df["price"].mean()
        return average