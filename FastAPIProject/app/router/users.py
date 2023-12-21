from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends, APIRouter
from app.models import User
from app.database import get_db
from app.schemas import UserCreate, UserOut
from passlib.context import CryptContext
from .auth import get_current_user
from app.utils import sqlalchemy_model_to_dict

router = APIRouter(
    prefix="/users",
    tags=['users']
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Endpoint to create a new user."""
    hashed_password = pwd_context.hash(user.password)
    new_user = User(email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return sqlalchemy_model_to_dict(new_user)


@router.get("/{id}", response_model=UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    """Endpoint to retrieve a user by ID."""
    db_user = db.query(User).filter(User.id == id).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} was not found"
        )

    return sqlalchemy_model_to_dict(db_user)


@router.get('/current-user', response_model=UserOut)
def get_current_user_route(current_user: User = Depends(get_current_user)):
    """Endpoint to retrieve the current authenticated user."""
    return sqlalchemy_model_to_dict(current_user)
