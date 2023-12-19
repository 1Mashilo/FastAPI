from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from app.schemas import VoteSchema
from app.database import get_db  
from .auth import get_current_user  
from app.models import Vote, Post  # Use consistent model names

router = APIRouter(prefix="/vote", tags=['vote'])

@router.post("/", status_code=status.HTTP_201_CREATED)
def cast_vote(vote: VoteSchema, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    post_exists = db.query(Post).filter(Post.id == vote.voted_post_id).first()
    if not post_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    # Check if the user has already voted on the same post
    vote_query = db.query(Vote).filter(Vote.post_id == vote.voted_post_id, Vote.user_id == current_user.id)

    found_vote = vote_query.first()
    if vote.vote_direction == 1:
        # If the user has already voted on the post, raise a conflict exception
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User has already voted on this post")

    # Your voting logic goes here
    # For example, assuming you have a Vote model defined in your database models:
    new_vote = Vote(post_id=vote.voted_post_id, dir=vote.vote_direction, user_id=current_user.id)
    db.add(new_vote)
    db.commit()
    db.refresh(new_vote)

    return {"message": "Vote created successfully", "vote": new_vote}
