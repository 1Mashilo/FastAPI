from sqlalchemy import create_engine
from app.config import Settings
from app.models import Base
from app.router import posts, users, auth, vote
from app.database import get_db
from dotenv import load_dotenv
from fastapi import FastAPI
import os

# Load environment variables from .env file
load_dotenv()

# Create engine
engine = create_engine(Settings().DATABASE_URL)

# Bind the metadata to the engine
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI()

# Include routers
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(auth.router)
app.include_router(vote.router)

