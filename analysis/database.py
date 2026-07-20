# analysis/database.py
import psycopg2
from psycopg2.extras import execute_values
from typing import List
from analysis.models import ProductRecord
from utils.logger import logger

class DatabaseLoader:
    def __init__(self, db_url: str = "postgresql://postgres:postgres@localhost:5432/market_intelligence"):
        self.db_url = db_url
        self._bootstrap_db()

    def _bootstrap_db(self):
        """Initializes target historical tables if they don't exist yet."""
        query = """
        CREATE TABLE IF NOT EXISTS store_products (
            product_id VARCHAR(32) PRIMARY KEY,
            product_name VARCHAR(255) NOT NULL,
            price NUMERIC(12, 2) NOT NULL,
            currency VARCHAR(10) NOT NULL,
            competitor VARCHAR(100) NOT NULL,
            original_price NUMERIC(12, 2),
            rating REAL,
            review_count INTEGER,
            exchange_rate NUMERIC(10, 4),
            price_kes NUMERIC(12, 2),
            discount_percentage INTEGER,
            shipping_cost NUMERIC(10, 2),
            category VARCHAR(100),
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        conn = None
        try:
            conn = psycopg2.connect(self.db_url)
            with conn.cursor() as cur:
                cur.execute(query)
            conn.commit()
        except Exception as e:
            logger.error(f"Database bootstrap failed: {e}")
            if conn: conn.rollback()
        finally:
            if conn: conn.close()

    def upsert_batch(self, records: List[ProductRecord]):
        """Executes a high-performance transactional batch upsert routine."""
        if not records:
            return

        query = """
        INSERT INTO store_products (
            product_id, product_name, price, currency, competitor, original_price,
            rating, review_count, exchange_rate, price_kes, discount_percentage, 
            shipping_cost, category
        ) VALUES %s
        ON CONFLICT (product_id) DO UPDATE SET
            price = EXCLUDED.price,
            original_price = EXCLUDED.original_price,
            rating = EXCLUDED.rating,
            review_count = EXCLUDED.review_count,
            exchange_rate = EXCLUDED.exchange_rate,
            price_kes = EXCLUDED.price_kes,
            discount_percentage = EXCLUDED.discount_percentage,
            shipping_cost = EXCLUDED.shipping_cost,
            category = EXCLUDED.category,
            updated_at = CURRENT_TIMESTAMP;
        """
        
        # Prepare the list of tuples for psycopg2 batch execution
        data_tuples = [
            (
                r.product_id, r.product_name, r.price, r.currency, r.competitor, r.original_price,
                r.rating, r.review_count, r.exchange_rate, r.price_kes, r.discount_percentage,
                r.shipping_cost, r.category
            ) for r in records
        ]

        conn = None
        try:
            conn = psycopg2.connect(self.db_url)
            with conn.cursor() as cur:
                # Reuses connection pool parameters to securely commit batch lines inside a single block
                execute_values(cur, query, data_tuples)
            conn.commit()
            logger.info(f"Successfully upserted batch of {len(records)} records into the database.")
        except Exception as e:
            logger.error(f"Failed to execute database upsert batch: {e}")
            if conn: 
                conn.rollback()
            raise e
        finally:
            if conn: 
                conn.close()