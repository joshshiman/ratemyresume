from sqlalchemy import create_engine, Column, String, JSON
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

class Job(Base):
    __tablename__ = "jobs"

    id = Column(String(36), primary_key=True)  # UUID length
    title = Column(String(255))
    company = Column(String(255))
    location = Column(String(255))
    pay = Column(JSON)
    description = Column(JSON)
    source_url = Column(String(512))

# Use standard PostgreSQL driver
DATABASE_URL = os.getenv("SUPABASE_DB_URL")

# Verify connection URL format
if not DATABASE_URL.startswith("postgresql://"):
    raise ValueError(f"Invalid DB URL format: {DATABASE_URL}")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("✅ Database tables created successfully!")