import dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_USER = dotenv.get_key(".env", "DB_USER")
DB_PASSWORD = dotenv.get_key(".env", "DB_PASS")
DB_NAME = dotenv.get_key(".env", "DB_NAME")
DB_HOST = dotenv.get_key(".env", "DB_HOST")

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()