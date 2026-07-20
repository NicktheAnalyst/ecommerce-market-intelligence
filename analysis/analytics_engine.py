import pandas as pd
from analysis.data_loader import DataLoader

class AnalyticsEngine:

    def __init__(self):
        loader = DataLoader()
        
        self.products = loader.load_products()
        self.prices = loader.load_prices()
        self.snapshots = loader.load_snapshots()
        self.competitors = loader.load_competitors()

    def get_readable_prices(self) -> pd.DataFrame:
        """
        Step 4: Joins raw prices with product names to make datasets readable.
        """
        merged = self.prices.merge(
            self.products,
            left_on="product_id",
            right_on="id"
        )
        return merged

    def analyze_price_changes(self) -> pd.DataFrame:
        """
        Step 6: Price Change Analysis
        Compares the latest two prices for each product to find value drift.
        """
        # Ensure prices are sorted by date to accurately identify yesterday vs today
        sorted_prices = self.prices.sort_values(by=["product_id", "date"])
        
        # Grab the last two historical records per product group
        latest_two = sorted_prices.groupby("product_id").tail(2).copy()
        
        # Create a shift to compare today's row against yesterday's row directly
        latest_two["yesterday_price"] = latest_two.groupby("product_id")["price"].shift(1)
        
        # Drop rows that don't have a previous day's price to compare against
        analysis_df = latest_two.dropna(subset=["yesterday_price"]).copy()
        analysis_df.rename(columns={"price": "today_price"}, inplace=True)
        
        # Calculations: Find difference and percentage delta
        analysis_df["difference"] = analysis_df["today_price"] - analysis_df["yesterday_price"]
        analysis_df["percentage"] = (analysis_df["difference"] / analysis_df["yesterday_price"]) * 100
        
        return analysis_df

    def check_inventory_risk(self, consecutive_threshold: int = 3) -> pd.DataFrame:
        """
        Step 7: Inventory Risk Analysis
        Flags products that consistently present 'Out of Stock' trends.
        """
        # Sort chronologically to preserve consecutive snapshot days
        sorted_snapshots = self.snapshots.sort_values(by=["product_id", "date"])
        
        # Identify rows that are out of stock (1 if out, 0 if in stock)
        is_out = (sorted_snapshots["status"].str.lower() == "out").astype(int)
        
        # Group consecutive occurrences together
        consecutive_groups = (is_out != is_out.shift()).cumsum()
        
        # Calculate size of blocks where status remains 'Out'
        sorted_snapshots["days_out"] = sorted_snapshots.groupby(["product_id", consecutive_groups])["status"].transform("count")
        # Reset to 0 if the actual status for that block isn't 'Out'
        sorted_snapshots.loc[sorted_snapshots["status"].str.lower() != "out", "days_out"] = 0
        
        # Pick out peak consecutive run values per product
        risk_df = sorted_snapshots.groupby("product_id")["days_out"].max().reset_index()
        
        # Assign Risk Category Flag based on threshold
        risk_df["risk"] = risk_df["days_out"].apply(
            lambda x: "High" if x >= consecutive_threshold else ("Medium" if x > 0 else "Low")
        )
        
        # Join with products for human-readable output
        return risk_df.merge(self.products, left_on="product_id", right_on="id")

    def get_discount_opportunities(self) -> pd.DataFrame:
        """
        Step 8: Discount Opportunities
        Finds and sorts the deepest current price slashes.
        """
        merged = self.get_readable_prices()
        
        # Safety Check: If a pre-calculated column doesn't exist, generate it dynamically
        if "discount" not in merged.columns and "original_price" in merged.columns:
            merged["discount"] = ((merged["original_price"] - merged["price"]) / merged["original_price"]) * 100
            
        top_discounts = merged.sort_values(by="discount", ascending=False)
        return top_discounts

    def get_competitor_ranking(self) -> pd.Series:
        """
        Step 9: Competitor Ranking
        Ranks your marketplace peers by sorting their aggregate mean price points.
        """
        # Merge price structures against competitor tracking contexts
        comp_merged = self.prices.merge(self.competitors, on="product_id", suffixes=('', '_comp'))
        
        ranking = comp_merged.groupby("competitor")["price"].mean().sort_values()
        return ranking

    def get_kpi_summary(self) -> dict:
        """
        Step 10: KPI Summary Dashboard Dictionary
        Compiles structural macro metrics optimized for downstream Power BI reporting.
        """
        kpis = {
            "products": len(self.products),
            "competitors": len(self.competitors),
            "average_price": self.prices["price"].mean(),
            "highest_price": self.prices["price"].max(),
            "lowest_price": self.prices["price"].min()
        }
        return kpis