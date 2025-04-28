from sqlalchemy import Column, Integer, String, DateTime, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# Base class for declarative models
Base = declarative_base()

class MemoryEntry(Base):
    __tablename__ = 'memory_entries'

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    source = Column(String, default='', nullable=False)
    tags = Column(JSON, default=[], nullable=False)
    embedding = Column(JSON, nullable=False)
    summary = Column(Text, default='', nullable=False) 