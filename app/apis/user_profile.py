from fastapi import FastAPI, HTTPException, status, Depends, APIRouter

from sqlalchemy.orm import Session
from app.database import get_db

from app.schemas.user_profile import ProfileCreate, Profile 
from app.schemas.user import User
from app.auth.oauth2 import get_active_user

from app.crud.user_profile import (
    create_user_profile, 
    get_user_profile
)

# Create a router for the user profile
router = APIRouter(
    prefix="/profile",
    tags=["User Profile"]
)

@router.get("/")
def read_profile(
    current_user: User = Depends(get_active_user),
    db: Session = Depends(get_db)
):
    db_profile = get_user_profile(db, user_id=current_user.id)
    if db_profile is None:
        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )
    return db_profile

# Create a new user profile
@router.post("/", 
    status_code=status.HTTP_201_CREATED,
    response_model=Profile
)
def create_profile(
    profile: ProfileCreate, 
    current_user: User = Depends(get_active_user),
    db: Session = Depends(get_db)
):
    db_profile = create_user_profile(db, profile=profile, user_id=current_user.id)
    return db_profile




















# Get a user profile
# @router.get("/", 
#     status_code=status.HTTP_200_OK,
#     response_model=Profile
# )
# def get_profile(
#     current_user: User = Depends(get_active_user),
#     db: Session = Depends(get_db)
# ):

#     db_profile = get_user_profile(db, user_id=current_user)
#     if db_profile is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Profile not found"
#         )
#     return db_profile