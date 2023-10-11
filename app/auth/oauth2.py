from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from jose import jwt, JWTError

from app.models.user import User
from app.database import get_db
from app.schemas.auth import TokenData
from app.crud.user import get_user_by_email
from app.config import settings

# Create an OAuth2PasswordBearer scheme for token handling
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth") 

# Load settings from the configuration module
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
# ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# Create an access token with an expiration time
def create_access_token(data: dict):
    to_encode = data.copy()
    expiration = datetime.utcnow() + timedelta(hours=1)
    to_encode.update({"expiration": expiration.strftime("%Y-%m-%d %H:%M:%S")})
    
    # Encode the JWT token with the provided data, secret key, and algorithm
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

# Verify the JWT token and retrieve user information
def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], 
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception

    # Retrieve the user from the database using the email from the token
    user = get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
          
    return user

# Get the currently authenticated user (the active user)
def get_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if not current_user.id:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

