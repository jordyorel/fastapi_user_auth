from uuid import UUID

from sqlalchemy.orm import Session

from app.utils import hash_password
from app.models.user import User
from app.schemas.user import UserCreate

# Get a user by id
def get_user(db: Session, user_id: UUID):
    return db.query(User).filter(User.id == user_id).first()

# Get a user by email
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# Get all users
def get_users(db: Session, skip: int, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

# Todo: make this fuction actually gets users by role
def get_users_by_role(db: Session, role: int, skip: int, limit: int = 100):
    return db.query(User).filter(User.role == role).offset(skip).limit(limit).all()

# Create a new user
def create_new_user(db: Session, user: UserCreate):
    hashed_password = hash_password(user.password)
    user.password = hashed_password
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Update a user
def update_user_in_db(db: Session, user_id: UUID, user: UserCreate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        return None
    db_user.email = user.email
    db_user.role = user.role
    db.commit()
    db.refresh(db_user)
    return db_user

# Delete a user
def delete_user_in_db(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    db.delete(db_user)
    db.commit()
    return db_user
    