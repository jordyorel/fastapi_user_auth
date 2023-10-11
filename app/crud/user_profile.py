from uuid import UUID

from sqlalchemy.orm import Session

from app.models.user import Profile
from app.schemas.user_profile import ProfileCreate

# Create a new user profile
def create_user_profile(db: Session, profile: ProfileCreate, user_id: UUID):
    db_profile = Profile(**profile.dict(), user_id=user_id)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

# Get a user profile
def get_user_profile(db: Session, user_id: UUID):
    return db.query(Profile).filter(Profile.id == user_id).first()

