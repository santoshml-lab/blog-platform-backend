from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import Post, User
from schemas import PostCreate, PostUpdate, PostResponse
from auth import get_current_user


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


# =========================
# CREATE POST
# =========================

@router.post(
    "/",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED
)
def create_post(
    post_data: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_post = Post(
        title=post_data.title,
        content=post_data.content,
        author_id=current_user.id
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


# =========================
# GET ALL POSTS
# =========================

@router.get(
    "/",
    response_model=list[PostResponse]
)
def get_posts(
    db: Session = Depends(get_db)
):
    return db.query(Post).order_by(
        Post.created_at.desc()
    ).all()


# =========================
# GET SINGLE POST
# =========================

@router.get(
    "/{post_id}",
    response_model=PostResponse
)
def get_post(
    post_id: int,
    db: Session = Depends(get_db)
):
    post = db.query(Post).filter(
        Post.id == post_id
    ).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    return post


# =========================
# UPDATE POST
# =========================

@router.put(
    "/{post_id}",
    response_model=PostResponse
)
def update_post(
    post_id: int,
    post_data: PostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post = db.query(Post).filter(
        Post.id == post_id
    ).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    # Only the author can edit
    if post.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only edit your own posts"
        )

    post.title = post_data.title
    post.content = post_data.content

    db.commit()
    db.refresh(post)

    return post


# =========================
# DELETE POST
# =========================

@router.delete(
    "/{post_id}"
)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post = db.query(Post).filter(
        Post.id == post_id
    ).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    # Only the author can delete
    if post.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own posts"
        )

    db.delete(post)
    db.commit()

    return {
        "message": "Post deleted successfully"
    }
