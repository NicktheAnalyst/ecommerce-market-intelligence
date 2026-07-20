from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# 1. Define your database URL (replace with your actual DB path/credentials if not using SQLite)
DATABASE_URL = "sqlite:///./sql_app.db"

# 2. Create the SQLAlchemy engine
# Note: 'connect_args' is only needed if you are using SQLite
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# 3. Create the SessionLocal class (this is what crud.py is looking for!)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Your existing Base class
class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass