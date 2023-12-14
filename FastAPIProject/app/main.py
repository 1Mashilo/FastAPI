# app/main.py
from fastapi import FastAPI
from app.router import posts, users
from app.database import engine
from app.models import Base
from passlib.hash import bcrypt

Base.metadata.create_all(bind=engine)

hash_rounds = 12

app = FastAPI()

# Include routers
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(auth.router)