from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class NewsModel(Base):
    """Modelo SQLAlchemy - Capa de infraestructura"""
    __tablename__ = "news"
    
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    content_veredict = Column(String, nullable=False)
    semantic_veredict = Column(String, nullable=False)
    general_veredict = Column(String, nullable=False)
    content_score = Column(Float, nullable=False)
    semantic_score = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


