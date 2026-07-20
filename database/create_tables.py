from database.base import Base
from database.connection import engine
import database.models

Base.metadata.drop_all(bind=engine)

Base.metadata.create_all(bind=engine)

print("Fresh database created.")