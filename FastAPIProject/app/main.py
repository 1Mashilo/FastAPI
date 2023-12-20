from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.router import posts, users, auth, vote
from dotenv import load_dotenv
from alembic.config import Config
from alembic import command

load_dotenv()

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You may want to restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

alembic_config = Config("alembic.ini")

# Include routers
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(auth.router)
app.include_router(vote.router)

# Define an asynchronous function to apply Alembic migrations
async def apply_migrations():
    command.upgrade(alembic_config, "head")

# Register the function to run during startup
@app.on_event("startup")
async def startup_event():
    await apply_migrations()

# Example of custom middleware
async def custom_middleware(request: Request, call_next):
    # Do something before handling the request
    response = await call_next(request)
    # Do something after handling the request
    return response

# Add custom middleware
app.add_middleware(custom_middleware)

# Example of handling exceptions globally
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(content={"error": "Internal Server Error"}, status_code=500)

