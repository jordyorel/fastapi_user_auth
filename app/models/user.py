import enum, uuid

from sqlalchemy import Column, Integer, String, Text, Enum, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID



from ..database import Base
from .mixins import Timestamp

# This is a Pydantic model for User roles
class UserRole(enum.IntEnum):
    teacher = 1
    student = 2
    parent = 3 

# This is a SQLAlchemy model for User table
class User(Timestamp, Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.student)
    is_active = Column(Boolean, default=True)  

    profile = relationship("Profile", back_populates="owner", uselist=False)
    
# This is a SQLAlchemy model for User Profile table
class Profile(Timestamp,Base):
    __tablename__ = 'profiles'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    bio = Column(Text, nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)

    owner = relationship("User", back_populates="profile")
