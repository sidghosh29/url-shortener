from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.config import settings

engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
# autoflush=False: Prevents the session from automatically sending pending 
# changes (SQL statements) to the database before running a new query.
#
# autocommit=False: Prevents changes from instantly saving. Requires a manual 
# session.commit() to permanently write the transaction to the database.
#
# Summary: Autoflush controls when changes are *sent* to the database; 
# autocommit controls when they are permanently *saved*.

def get_db():
    """
    FastAPI dependency that provides a database session
    and ensures it is closed after the request completes.
    """
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()