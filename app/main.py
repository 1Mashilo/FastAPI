
"""
FastAPI application for managing blog posts.
"""

from fastapi import FastAPI, HTTPException, Response, status, Depends
from sqlalchemy.orm import Session
from fastapi.responses import Response
from database import engine, get_db
from models import Base, Post, User
from schemas import PostCreate, UserCreate, UserOut,  PostResponse
from passlib.hash import bcrypt
hash_rounds = 12

Base.metadata.create_all(bind=engine)  
hash_rounds = 12
app = FastAPI()

@app.get("/")
def root():
    """
    Welcome endpoint.
    """
    return {"message": "Welcome to my API"}

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    """
    Retrieve a list of all blog posts.

    Args:
        db (Session): The database session.

    Returns:
        List[Post]: A list of all blog posts.
    """
    posts = db.query(Post).all()
    return posts
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    """
    Create a new blog post.

    Args:
        post (PostCreate): The data for the new post.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing the newly created post.
    """
    db_post = Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return sqlalchemy_model_to_dict(db_post)

@app.get("/posts/{id}", response_model=dict)
def get_post(id: int, db: Session = Depends(get_db)):
    """
    Retrieve details of a specific post by ID.

    Args:
        id (int): The ID of the post to retrieve.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing the details of the specified post.
    """
    db_post = db.query(Post).filter(Post.id == id).first()

    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found"
        )

    return {"post_detail": db_post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    """
    Delete a post by ID.

    Args:
        id (int): The ID of the post to delete.
        db (Session): The database session.

    Returns:
        Response: An HTTP response indicating the success of the operation.
    """
    db_post = db.query(Post).filter(Post.id == id).first()

    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} does not exist"
        )

    db.delete(db_post)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", response_model=dict)
def update_post(id: int, post: PostCreate, db: Session = Depends(get_db)):
    """
    Update a post by ID.

    Args:
        id (int): The ID of the post to update.
        post (PostCreate): The updated data for the post.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing the updated post.
    """
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

@app.post("/user", status_code=status.HTTP_201_CREATED,response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user.hash_password()
    new_user = User(**user.dict()) 
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return sqlalchemy_model_to_dict(new_user)

def sqlalchemy_model_to_dict(model):
    return {column.name: getattr(model, column.name) for column in model.__table__.columns}
