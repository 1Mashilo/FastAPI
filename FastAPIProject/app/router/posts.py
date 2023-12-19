from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from app.models import Base, Post, User
from app.schemas import PostCreate, UserCreate, UserOut, PostResponse
from app.database import engine, get_db
from app.utils import sqlalchemy_model_to_dict
from .auth import oauth2, get_current_user
from typing import Optional, List

router = APIRouter()

@router.get("/posts", response_model=List[PostResponse])
def get_posts(
    db: Session = Depends(get_db),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
    category: Optional[str] = "",
    author: Optional[str] = ""
):
    query = db.query(Post).filter(Post.title.contains(search))

    if category:
        query = query.filter(Post.category == category)

    if author:
        query = query.filter(Post.author == author)

    posts = query.limit(limit).offset(skip).all()
      # Convert SQLAlchemy models to Pydantic models
    response_posts = []
    for post in posts:
        owner_pydantic = UserOut.from_orm(post.owner)
        response_post = PostResponse(
            **sqlalchemy_model_to_dict(post),
            owner=owner_pydantic
        )
        response_posts.append(response_post)

    return response_posts
    


@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_post = Post(**post.dict(), owner_id=current_user.id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    # Convert SQLAlchemy model instance to Pydantic model
    owner_pydantic = UserOut.from_orm(current_user)

    # Populate the owner field in the response
    response_post = PostResponse(
        **sqlalchemy_model_to_dict(db_post),
        owner=owner_pydantic
    )

    return response_post


@router.get("/posts/{id}", response_model=PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    db_post = db.query(Post).filter(Post.id == id).first()

    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found"
        )

    return sqlalchemy_model_to_dict(db_post)

@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_post = db.query(Post).filter(Post.id == id).first()

    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} does not exist"
        )

    if db_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    db.delete(db_post)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/posts/{id}", response_model=PostResponse)
def update_post(
    id: int,
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_post = db.query(Post).filter(Post.id == id).first()

    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} does not exist"
        )

    if db_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    for key, value in post.dict().items():
        setattr(db_post, key, value)

    db.commit()
    db.refresh(db_post)
    owner_pydantic = UserOut.from_orm(db_post.owner)
    response_post = PostResponse(
        **sqlalchemy_model_to_dict(db_post),
        owner=owner_pydantic
    )

    return response_post
