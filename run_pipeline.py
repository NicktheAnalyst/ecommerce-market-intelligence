import pandas as pd
from analysis.analytics_engine import AnalyticsEngine
from analysis.exporter import Exporter

def main():
    print("🚀 Initializing end-to-end data pipeline extraction...")
    
    # 1. Spin up the processing layers (Extracts via SQL -> loads into Pandas)
    engine = AnalyticsEngine()
    exporter = Exporter()
    
    print("📊 Executing analytical engine business logic transformations...")
    # 2. Extract calculations
    price_changes = engine.analyze_price_changes()
    inventory_risk = engine.check_inventory_risk()
    discount_opportunities = engine.get_discount_opportunities()
    competitor_ranking = engine.get_competitor_ranking()
    kpi_dict = engine.get_kpi_summary()
    
    # Format structural data objects neatly for export targets
    kpis_df = pd.DataFrame([kpi_dict])
    
    # Reset tracking index fields on ranking metrics to output clean tabular columns
    competitor_ranking_df = competitor_ranking.reset_index()
    competitor_ranking_df.columns = ["Competitor", "Avg Price"]
    
    print("💾 Exporting clean output layers to target directory 'data/analytics/'...")
    # 3. Save datasets down cleanly to their specific target dashboard locations
    exporter.save(competitor_ranking_df, "competitor_ranking.csv")
    exporter.save(inventory_risk, "inventory_risk.csv")
    exporter.save(discount_opportunities, "discount_report.csv")
    exporter.save(kpis_df, "kpis.csv")
    
    # Optional handler for dynamic name mapping matching output requirements
    price_changes.rename(columns={"today_price": "cheapest_price"}, inplace=True, errors="ignore")
    exporter.save(price_changes, "cheapest_competitors.csv")
    
    print("✨ Pipeline ran successfully. Data assets ready for Power BI consumption.")

if __name__ == "__main__":
    main()