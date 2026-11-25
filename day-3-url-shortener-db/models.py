from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from app.venv.database import Base


class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True, nullable=False)
    original_url = Column(String, nullable=False)
    visits = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)