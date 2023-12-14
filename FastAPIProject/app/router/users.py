
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from app.models import Base, Post, User 
from app.database import get_db
from app.schemas import PostCreate, UserCreate, UserOut, PostResponse
from passlib.hash import bcrypt
from app.utils import sqlalchemy_model_to_dict

router = APIRouter(
    prefix="/users"
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user.hash_password()
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return sqlalchemy_model_to_dict(new_user)

@router.get("/{id}", response_model=UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == id).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} was not found"
        )

    return sqlalchemy_model_to_dict(db_user)



