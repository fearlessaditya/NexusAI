from sqlalchemy.orm import sessionmaker

from app.database.connection import engine

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
from sqlalchemy.orm import Session


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()