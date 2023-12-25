from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from alembic.config import Config
from alembic import command
from app.router import posts, users, auth, vote

# Load environment variables from .env file
load_dotenv()

# Create a FastAPI instance
app = FastAPI()

# Enable CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Alembic for database migrations
alembic_config = Config("alembic.ini")

# Include routers
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(auth.router)
app.include_router(vote.router)

# Define an asynchronous function to apply Alembic migrations
async def apply_migrations():
    """Apply database migrations using Alembic."""
    command.upgrade(alembic_config, "head")

# Register the function to run during startup
@app.on_event("startup")
async def startup_event():
    """Event handler to apply database migrations on application startup."""
    await apply_migrations()
