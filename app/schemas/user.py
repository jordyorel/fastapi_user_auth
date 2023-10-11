from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field



class UserBase(BaseModel):
    email: EmailStr
    role: int = Field(default=2)

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: UUID
    is_active: bool

    class Config:
        from_attributes = True

