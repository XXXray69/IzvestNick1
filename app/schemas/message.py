from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class SendMessageRequest(BaseModel):
    body: str = Field(min_length=1, max_length=10000)
    reply_to_message_id: Optional[int] = None
    forwarded_from_chat_id: Optional[int] = None


class MessageOut(BaseModel):
    id: int
    chat_id: int
    sender_id: int
    body: str
    reply_to_message_id: Optional[int] = None
    forwarded_from_chat_id: Optional[int] = None
    deleted_for_everyone: bool
    created_at: datetime

    class Config:
        from_attributes = True


class DeleteMessageRequest(BaseModel):
    delete_for_everyone: bool = False
