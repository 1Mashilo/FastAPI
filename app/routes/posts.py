from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from  . .database import get_db
from .. models import Post
from schemas import PostCreate, PostResponse
from utils import sqlalchemy_model_to_dict 

router = APIRouter()

@router.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    return posts

@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    db_post = Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return sqlalchemy_model_to_dict(db_post)

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
def delete_post(id: int, db: Session = Depends(get_db)):
    db_post = db.query(Post).filter(Post.id == id).first()

    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} does not exist"
        )

    db.delete(db_post)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/posts/{id}", response_model=PostResponse)
def update_post(id: int, post: PostCreate, db: Session = Depends(get_db)):
    db_post = db.query(Post).filter(Post.id == id).first()

    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} does not exist"
        )

    for key, value in post.dict().items():
        setattr(db_post, key, value)

    db.commit()
    db.refresh(db_post)
    return sqlalchemy_model_to_dict(db_post)

# Include this router in the main application

