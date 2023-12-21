from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException
from passlib.context import CryptContext
from typing import Optional
from app.schemas import TokenData, Token
from fastapi.security import OAuth2PasswordBearer
from app.config.dev_config import Settings

# Load settings
settings = Settings()

ALGORITHM = settings.ALGORITHM
SECRET_KEY = settings.SECRET_KEY

# Initialize passlib context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 password bearer for authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> Token:
    """Create an access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return Token(access_token=encoded_jwt, token_type="bearer")


def verify_token(token: str, credentials_exception: HTTPException) -> TokenData:
    """Verify the access token and extract token data."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenData(**payload)
    except JWTError:
        raise credentials_exception
    return token_data


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password, rounds=HASH_ROUNDS)


def verify(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hashed version."""
    return pwd_context.verify(plain_password, hashed_password)


def sqlalchemy_model_to_dict(instance) -> dict:
    """Convert a SQLAlchemy model instance to a dictionary."""
    result = {column.name: getattr(instance, column.name) for column in instance.__table__.columns}

    # Add logic to count likes
    if hasattr(instance, 'votes'):
        result['likes'] = sum(1 for vote in instance.votes if vote.vote_direction == 1)
    else:
        result['likes'] = 0

    return result
