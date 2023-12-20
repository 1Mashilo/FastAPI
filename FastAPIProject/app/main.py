from alembic.config import Config
from alembic import command
from fastapi import FastAPI
from app.router import posts, users, auth, vote
from dotenv import load_dotenv


load_dotenv()

app = FastAPI()

alembic_config = Config("alembic.ini")

# Include routers
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(auth.router)
app.include_router(vote.router)

# Apply Alembic migrations during application startup
command.upgrade(alembic_config, "head")
