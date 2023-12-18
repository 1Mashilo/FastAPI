from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from app.schemas import TokenData, Token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from typing import Optional

pwd_contract = CryptContext(schemes=["bcrypt"], deprecated="auto")

hash_rounds = 12

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> Token:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return Token(access_token=encoded_jwt, token_type="bearer")

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
