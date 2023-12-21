from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Construct the database URL
quoted_password = quote(os.getenv("DATABASE_PASSWORD"), safe="")
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{os.getenv('DATABASE_USERNAME')}:{quoted_password}@"
    f"{os.getenv('DATABASE_HOSTNAME')}:{os.getenv('DATABASE_PORT')}/{os.getenv('DATABASE_NAME')}"
)

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create the session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency to get the database session
def get_db():
    """Get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
