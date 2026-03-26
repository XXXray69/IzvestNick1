from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.security import get_current_user
from app.models.chat import Chat
from app.models.user import User
from app.schemas.chat import ChatOut, CreateDirectChatRequest

router = APIRouter(prefix='/chats', tags=['chats'])


@router.post('/direct', response_model=ChatOut)
def create_direct_chat(payload: CreateDirectChatRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    other = db.get(User, payload.user_id)
    if not other:
        raise HTTPException(status_code=404, detail='Target user not found')

    candidate_chats = db.query(Chat).filter(Chat.is_direct == True).all()
    for chat in candidate_chats:
        member_ids = {m.id for m in chat.members}
        if member_ids == {current_user.id, other.id}:
            return chat

    chat = Chat(is_direct=True)
    chat.members.extend([current_user, other])
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat


@router.get('', response_model=List[ChatOut])
def list_chats(current_user: User = Depends(get_current_user)):
    return current_user.chats


@router.delete('/{chat_id}')
def delete_chat(chat_id: int, delete_for_everyone: bool = False, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    chat = db.get(Chat, chat_id)
    if not chat or current_user.id not in {m.id for m in chat.members}:
        raise HTTPException(status_code=404, detail='Chat not found')

    if delete_for_everyone:
        db.delete(chat)
    else:
        chat.members = [m for m in chat.members if m.id != current_user.id]
    db.commit()
    return {'status': 'deleted', 'delete_for_everyone': delete_for_everyone}
