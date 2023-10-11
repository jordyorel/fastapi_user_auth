from uuid import UUID

from pydantic import BaseModel

class ProfileBase(BaseModel):
    first_name: str
    last_name: str
    bio: str = None


class ProfileCreate(ProfileBase):
    pass

class Profile(ProfileBase):
    id: UUID
    user_id: UUID

    class Config:
        from_attribute = True
