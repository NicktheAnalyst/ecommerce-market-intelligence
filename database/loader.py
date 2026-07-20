from database.connection import SessionLocal
from database.repository import Repository

class DatabaseLoader:

    def load(self, records):
        session = SessionLocal()
        repo = Repository(session)
        
        try:
            for record in records:
                # 1. Resolve or generate dimension records
                product = repo.get_or_create_product(record)
                competitor = repo.get_or_create_competitor(
                    record.competitor,
                    record.website,
                    record.country
                )
                
                # 2. Append chronological timeline metrics
                repo.insert_price(product, competitor, record)
                repo.insert_snapshot(product, competitor, record)
            
            # Commit all operations simultaneously if the entire batch passes
            session.commit()
            
        except Exception:
            # Roll back everything if any individual item fails to protect data integrity
            session.rollback()
            raise
            
        finally:
            # Always hand back connection resources back to the connection pool
            session.close()