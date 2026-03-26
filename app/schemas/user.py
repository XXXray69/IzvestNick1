from typing import Optional
from pydantic import BaseModel, Field


class UserOut(BaseModel):
    id: int
    phone_prefix: str
    phone_number: str
    first_name: str
    last_name: str
    username_link: Optional[str] = None
    bio: Optional[str] = None
    main_photo_path: Optional[str] = None

    class Config:
        from_attributes = True


class SetProfileRequest(BaseModel):
    username_link: Optional[str] = Field(default=None, max_length=64)
    bio: Optional[str] = Field(default=None, max_length=300)
