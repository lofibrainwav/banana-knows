import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from scripts.storage.models import Base

# Database URL from environment or default to local SQLite file
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./memory.db")

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialize database (create tables)
def init_db():
    Base.metadata.create_all(bind=engine) 