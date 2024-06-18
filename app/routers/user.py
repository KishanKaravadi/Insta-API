from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # Hash password

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    # Add to database

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get('/{id}', response_model=schemas.User)
def get_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).where(
        models.User.id == id).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")

    return user
