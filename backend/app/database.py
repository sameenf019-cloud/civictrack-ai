import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Local SQLite file. Later we can change this to a PostgreSQL URL
# using the DATABASE_URL environment variable.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./civictrack.db")

# SQLite needs this extra option because FastAPI uses multiple threads.
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Gives one database session per request and closes it afterwards."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()