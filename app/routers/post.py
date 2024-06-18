from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ''):

    posts = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        # type: ignore
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(
        limit).offset(skip).all()

    return posts


@router.get("/me", response_model=List[schemas.PostOut])
def get_my_posts(db: Session = Depends(get_db), curr_user: models.User = Depends(oauth2.get_current_user)):

    posts = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        # type: ignore
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).where(
        models.Post.owner_id == curr_user.id).all()

    return posts


@router.get("/{id}", response_model=schemas.PostOut)
def def_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        # type: ignore
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).where(
        models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} was not found')
    return post


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), curr_user: models.User = Depends(oauth2.get_current_user)):

    new_post = models.Post(owner_id=curr_user.id, **post.model_dump())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), curr_user: models.User = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).where(models.Post.id == id)

    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")

    if post.owner_id != curr_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Not authorized to perfrom requested action')

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put(path='/{id}', response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), curr_user: models.User = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).where(
        models.Post.id == id)

    updated_post = post_query.first()

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")

    if updated_post.owner_id != curr_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Not authorized to perfrom requested action')

    post_query.update(post.model_dump(), synchronize_session=False)

    db.commit()

    return post_query.first()
