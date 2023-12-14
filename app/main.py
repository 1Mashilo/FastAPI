# main.py
from fastapi import FastAPI
from routes import posts, users

app = FastAPI()

app.include_router(posts.router, prefix="/posts", tags=["posts"])
app.include_router(users.router, prefix="/users", tags=["users"])

# Add other routes and configurations here
