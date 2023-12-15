from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import Token, TokenData
from app.utils import verify, verify_token, create_access_token


router = APIRouter(tags=['Authentication'])

oauth2 = OAuth2PasswordBearer(tokenUrl="/login")

@router.post('/login', response_model=Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.get(User, user_credentials.username)
    
    if not user or not verify(user_credentials.password, user.password):
        raise_authentication_error()

    access_token = create_access_token(data={"id": user.email})
    return {"token": access_token}


def get_current_user(token_data: TokenData = Depends(verify_token)):
    if token_data.id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token_data.id


def raise_authentication_error():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Credentials"
    )