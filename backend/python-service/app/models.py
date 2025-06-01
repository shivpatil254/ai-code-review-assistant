from sqlalchemy import Column, Integer, String, Float, JSON, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class CodeReview(Base):
    __tablename__ = "code_reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    language = Column(String, index=True)
    code = Column(String)
    score = Column(Float)
    issues = Column(JSON)
    metrics = Column(JSON)
    ai_suggestions = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<CodeReview(filename='{self.filename}', score={self.score})>"

# Database setup
DATABASE_URL = "sqlite:///./code_reviews.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
