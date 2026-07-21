# analysis/analytics_engine.py
import pandas as pd
import logging
from analysis.data_loader import DataLoader
from config import INVENTORY_RISK_THRESHOLD, MINIMUM_EXPECTED_PRICE

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class AnalyticsEngine:

    def __init__(self):
        loader = DataLoader()
        self.products = loader.load_products()
        self.prices = loader.load_prices()
        self.snapshots = loader.load_snapshots()
        self.competitors = loader.load_competitors()
        
        # Step 4 Improvement: Automatically validate data quality upon initialization
        self.validate_data_quality()

    def validate_data_quality(self):
        """
        Step 4: Automated Data Quality Checks.
        Flags missing values, duplicate SKUs, or unexpected negative prices.
        """
        # Check for missing prices
        missing_prices = self.prices["price"].isna().sum()
        if missing_prices > 0:
            logging.warning(f"⚠️ Data Quality Warning: Found {missing_prices} rows with missing prices.")
            self.prices = self.prices.dropna(subset=["price"])

        # Check for negative values
        negative_prices = (self.prices["price"] < MINIMUM_EXPECTED_PRICE).sum()
        if negative_prices > 0:
            logging.error(f"❌ Data Quality Alert: Found {negative_prices} rows with negative or invalid prices!")
            # Filter out corrupt entries
            self.prices = self.prices[self.prices["price"] >= MINIMUM_EXPECTED_PRICE]

        # Check for duplicate SKUs / products
        if "sku" in self.products.columns:
            duplicate_skus = self.products.duplicated(subset=["sku"]).sum()
            if duplicate_skus > 0:
                logging.warning(f"⚠️ Data Quality Warning: Found {duplicate_skus} duplicate SKUs in products table.")

    def get_readable_prices(self) -> pd.DataFrame:
        merged = self.prices.merge(self.products, left_on="product_id", right_on="id")
        return merged

    def analyze_price_changes(self) -> pd.DataFrame:
        sorted_prices = self.prices.sort_values(by=["product_id", "captured_at"])
        latest_two = sorted_prices.groupby("product_id").tail(2).copy()
        latest_two["yesterday_price"] = latest_two.groupby("product_id")["price"].shift(1)
        
        analysis_df = latest_two.dropna(subset=["yesterday_price"]).copy()
        analysis_df.rename(columns={"price": "today_price"}, inplace=True)
        analysis_df["difference"] = analysis_df["today_price"] - analysis_df["yesterday_price"]
        analysis_df["percentage"] = (analysis_df["difference"] / analysis_df["yesterday_price"]) * 100
        return analysis_df

    def check_inventory_risk(self) -> pd.DataFrame:
        sorted_snapshots = self.snapshots.sort_values(by=["product_id", "capture_date"])
        is_out = (sorted_snapshots["stock_status"].str.lower() == "out").astype(int)
        consecutive_groups = (is_out != is_out.shift()).cumsum()        
        sorted_snapshots["days_out"] = sorted_snapshots.groupby(["product_id", consecutive_groups])["stock_status"].transform("count")
        sorted_snapshots.loc[sorted_snapshots["stock_status"].str.lower() != "out", "days_out"] = 0
        
        risk_df = sorted_snapshots.groupby("product_id")["days_out"].max().reset_index()
        
        # Using config threshold here instead of hardcoded numbers
        risk_df["risk"] = risk_df["days_out"].apply(
            lambda x: "High" if x >= INVENTORY_RISK_THRESHOLD else ("Medium" if x > 0 else "Low")
        )
        return risk_df.merge(self.products, left_on="product_id", right_on="id")

    def get_discount_opportunities(self) -> pd.DataFrame:
        merged = self.get_readable_prices()
        if "discount" not in merged.columns and "original_price" in merged.columns:
            merged["discount"] = ((merged["original_price"] - merged["price"]) / merged["original_price"]) * 100
        return merged.sort_values(by="discount", ascending=False)

    def get_competitor_ranking(self) -> pd.DataFrame:
        comp_merged = self.prices.merge(
    self.competitors, 
    left_on="competitor_id", 
    right_on="id", 
    suffixes=('', '_comp')
)
        ranking = comp_merged.groupby("name")["price"].mean().sort_values().reset_index()
        ranking.columns = ["competitor", "avg_price"]
        return ranking

    def get_kpi_summary(self) -> dict:
        return {
            "products": len(self.products),
            "competitors": len(self.competitors),
            "average_price": float(self.prices["price"].mean()),
            "highest_price": float(self.prices["price"].max()),
            "lowest_price": float(self.prices["price"].min())
        }