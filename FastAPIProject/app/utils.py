from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from app.schemas import TokenData
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


# Constants
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
hash_rounds = 12

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenData(**payload)
    except JWTError:
        raise credentials_exception
    return token_data


def hash(password: str):
    return pwd_contract.hash(password)

def verify(plain_password, hash_password):
    return pwd_contract.verify(plain_password, hash_password)

def sqlalchemy_model_to_dict(model, exclude=None):
    if exclude is None:
        exclude = []
    return {column.name: getattr(model, column.name) for column in model.__table__.columns if column.name not in exclude}
