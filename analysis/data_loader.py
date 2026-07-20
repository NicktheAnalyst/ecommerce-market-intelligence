# analysis/data_loader.py
import pandas as pd
from sqlalchemy import text
from database.connection import engine

class DataLoader:
    
    def load_prices(self):
        query = text("""
            SELECT *
            FROM prices
        """)
        return pd.read_sql(
            query,
            engine
        )

    def load_snapshots(self):
        query = text("""
            SELECT *
            FROM daily_snapshots
        """)
        return pd.read_sql(
            query,
            engine
        )

    def load_products(self):
        query = text("""
            SELECT *
            FROM products
        """)
        return pd.read_sql(
            query,
            engine
        )

    def load_competitors(self):
        query = text("""
            SELECT *
            FROM competitors
        """)
        return pd.read_sql(
            query,
            engine
        )