from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.utils import verify_password
from app.database import get_db
from app.schemas.auth import Token
from app.crud.user import get_user_by_email

from .oauth2 import create_access_token


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/", response_model=Token)
def login(
    user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    user = get_user_by_email(db, email=user_credentials.username)
    if user is None or not verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=401,
            detail=f"Invalid Credentials",
        )
    access_token = create_access_token(data={"email": user.email})

    return {"access_token": access_token, "token_type": "bearer"}

