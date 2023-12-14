from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends, APIRouter
from app.models import User
from app.schemas import UserLogin
from app.database import get_db
from auth import utils

router = APIRouter(tags=['Authentication'])

def raise_authentication_error():
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Invalid Credentials"
    )

@router.post('/login')
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_credentials.email).first()
    
    if not user or not utils.verify(user_credentials.password, user.passlib):
        raise_authentication_error()

    return {"token"}
