# analysis/exporter.py
from pathlib import Path
import pandas as pd
from database.connection import engine as db_engine

class Exporter:
    
    def __init__(self):
        self.OUTPUT_DIR = Path("data/analytics")
        self.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        
    def save_to_csv(self, dataframe: pd.DataFrame, filename: str):
        """Saves analytical output to standard flat files."""
        if isinstance(dataframe, pd.Series):
            dataframe = dataframe.to_frame()
        dataframe.to_csv(self.OUTPUT_DIR / filename, index=False)

    def save_to_summary_table(self, dataframe: pd.DataFrame, table_name: str):
        """
        Step 2 Improvement: Persists generated analytics directly back into SQL 
        summary tables (e.g., daily_competitor_summary) for historical tracking.
        """
        # if_exists='append' maintains histories day-over-day
        dataframe.to_sql(
            name=table_name,
            con=db_engine,
            if_exists="append",
            index=False
        )