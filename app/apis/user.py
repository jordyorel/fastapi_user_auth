from uuid import UUID
from typing import Annotated

from fastapi import FastAPI, HTTPException, status, Depends, APIRouter

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, User
from app.crud.user import (
    create_new_user, get_users, 
    get_user, get_user_by_email, 
    get_users_by_role, 
    update_user_in_db, 
    delete_user_in_db)
from app.database import get_db
from app.auth.oauth2 import get_active_user


# Create a router for the users
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# Create a new user
@router.post("/", 
    status_code=status.HTTP_201_CREATED,
    response_model=User
)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    credentials_exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Email already registered"
    )
    if db_user:
        raise credentials_exception
    try:
        db_user = create_new_user(db, user=user)
    except IntegrityError:
        raise credentials_exception
    return db_user

# Get all users
@router.get("/", response_model=list[User])
def read_all_users(
    skip: int | None = None, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    users = get_users(db, skip=skip, limit=limit)
    return users

# Get a user by id
@router.get("/{user_id}", response_model=User)
def read_user(user_id:UUID , db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user



# Update a user
@router.put("/{user_id}", response_model=User)
def update_user(
    user_id: UUID, 
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_active_user)
):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if the user is the same as the one being updated
    if current_user.id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to perform this action"
        )
    db_user = update_user_in_db(db, user_id=user_id, user=user)
    
    return db_user


