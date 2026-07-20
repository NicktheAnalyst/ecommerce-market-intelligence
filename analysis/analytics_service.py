from analysis.analytics_engine import AnalyticsEngine

class AnalyticsService:
    """
    Step 1 Improvement: Coordinates all metrics pipelines into a 
    single, structured result payload wrapper.
    """
    def __init__(self):
        self.engine = AnalyticsEngine()

    def run_all_analyses(self) -> dict:
        """Runs computations across all domains and collects results."""
        results = {
            "price_changes": self.engine.analyze_price_changes(),
            "inventory_risk": self.engine.check_inventory_risk(),
            "discount_opportunities": self.engine.get_discount_opportunities(),
            "competitor_ranking": self.engine.get_competitor_ranking(),
            "kpis": self.engine.get_kpi_summary()
        }
        return results