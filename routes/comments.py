from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import Comment, Post, User
from schemas import CommentCreate, CommentResponse
from auth import get_current_user


router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)


# =========================
# ADD COMMENT
# =========================

@router.post(
    "/post/{post_id}",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_comment(
    post_id: int,
    comment_data: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if post exists
    post = db.query(Post).filter(
        Post.id == post_id
    ).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    new_comment = Comment(
        content=comment_data.content,
        post_id=post_id,
        user_id=current_user.id
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment


# =========================
# GET COMMENTS FOR A POST
# =========================

@router.get(
    "/post/{post_id}",
    response_model=list[CommentResponse]
)
def get_comments(
    post_id: int,
    db: Session = Depends(get_db)
):
    # Check if post exists
    post = db.query(Post).filter(
        Post.id == post_id
    ).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    return db.query(Comment).filter(
        Comment.post_id == post_id
    ).order_by(
        Comment.created_at.asc()
    ).all()


# =========================
# DELETE COMMENT
# =========================

@router.delete(
    "/{comment_id}"
)
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    comment = db.query(Comment).filter(
        Comment.id == comment_id
    ).first()

    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )

    # Only comment owner can delete
    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own comments"
        )

    db.delete(comment)
    db.commit()

    return {
        "message": "Comment deleted successfully"
    }
