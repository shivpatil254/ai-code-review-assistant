from sqlalchemy.orm import Session
from .models import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()