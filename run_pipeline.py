# run_pipeline.py
import pandas as pd
from analysis.analytics_service import AnalyticsService
from analysis.exporter import Exporter

def main():
    print("🚀 Initializing Enhanced Analytics Pipeline...")
    
    # Run decoupled service coordinator
    service = AnalyticsService()
    payload = service.run_all_analyses()
    
    exporter = Exporter()
    
    # Export flat files for backup/Power BI local file source integration
    print("💾 Archiving snapshots to CSV filesystem...")
    exporter.save_to_csv(payload["inventory_risk"], "inventory_risk.csv")
    exporter.save_to_csv(payload["discount_opportunities"], "discount_report.csv")
    
    # Store clean historical representations back into SQL Database summary tables
    print("🗄️ Writing analytical updates straight to Database Summary Tables...")
    exporter.save_to_summary_table(payload["competitor_ranking"], "daily_competitor_summary")
    exporter.save_to_summary_table(payload["price_changes"], "daily_price_delta_summary")
    exporter.save_to_summary_table(pd.DataFrame([payload["kpis"]]), "daily_kpi_summary")
    
    print("✨ Pipeline Complete. Data quality validated, stored, and exported.")

if __name__ == "__main__":
    main()