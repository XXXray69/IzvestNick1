from typing import List, Optional
from pydantic import BaseModel, model_validator
from app.schemas.user import UserOut


class CreateDirectChatRequest(BaseModel):
    user_id: Optional[int] = None
    username_link: Optional[str] = None

    @model_validator(mode='after')
    def validate_target(self):
        if self.user_id is None and not self.username_link:
            raise ValueError('Either user_id or username_link is required')
        return self


class ChatOut(BaseModel):
    id: int
    title: Optional[str]
    is_direct: bool
    members: List[UserOut]

    class Config:
        from_attributes = True
