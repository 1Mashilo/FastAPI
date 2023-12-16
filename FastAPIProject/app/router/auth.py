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
    user = db.query(User).filter(User.email == user_credentials.username).first()
    
    
    if not user or not verify(user_credentials.password, user.password):
        raise_authentication_error()

    access_token = create_access_token(data={"id": user.email})
    return access_token


def get_current_user(token: str = Depends(oauth2), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = verify_token(token, credentials_exception)
    user = db.query(User).filter(User.id == token.id).first()
    return user

def raise_authentication_error():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Credentials"
    )