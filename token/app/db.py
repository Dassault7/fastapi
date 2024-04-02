"""
token: Database setup for the token app
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    """
    Get the database session for the app

    :yield: The database session
    :rtype: Session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
