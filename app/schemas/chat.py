from typing import List, Optional
from pydantic import BaseModel
from app.schemas.user import UserOut


class CreateDirectChatRequest(BaseModel):
    user_id: int


class ChatOut(BaseModel):
    id: int
    title: Optional[str]
    is_direct: bool
    members: List[UserOut]

    class Config:
        from_attributes = True
