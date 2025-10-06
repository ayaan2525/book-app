from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool
from config import settings
from contextlib import contextmanager



engine = create_engine(

    settings.DATABASE_URL,
    # connect_args are specific to SQLite 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    future=True,
    echo=False,
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()



# Dependency for getting DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()