from pathlib import Path
import pandas as pd

class Exporter:
    
    def __init__(self):
        self.OUTPUT_DIR = Path("data/analytics")
        # Ensure target folder structures exist before exporting
        self.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        
    def save(self, dataframe: pd.DataFrame, filename: str):
        """
        Exports clean DataFrames or structural Series safely to disk as CSV.
        """
        # Convert Series structures dynamically to DataFrames if passed from ranking pipelines
        if isinstance(dataframe, pd.Series):
            dataframe = dataframe.to_frame()
            
        target_path = self.OUTPUT_DIR / filename
        dataframe.to_csv(target_path, index=False)