from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Replace with your actual credentials
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:secret@db:5432/dms_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
