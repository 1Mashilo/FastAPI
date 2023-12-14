# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote

password = "Mashilo@95"
quoted_password = quote(password, safe="")
SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:{quoted_password}@localhost/FastAPI"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
