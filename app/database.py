from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from .config import settings
  
SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{settings.DATABASE_USERNAME}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}" # PostgreSQL database  

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={}, 
    future=True
)

SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, bind=engine
)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()