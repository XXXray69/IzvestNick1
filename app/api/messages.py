from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.security import get_current_user
from app.core.websocket_manager import manager
from app.models.chat import Chat
from app.models.message import Message
from app.models.user import User
from app.schemas.message import DeleteMessageRequest, MessageOut, SendMessageRequest

router = APIRouter(prefix='/messages', tags=['messages'])


@router.get('/{chat_id}', response_model=List[MessageOut])
def list_messages(chat_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    chat = db.get(Chat, chat_id)
    if not chat or current_user.id not in {m.id for m in chat.members}:
        raise HTTPException(status_code=404, detail='Chat not found')
    return chat.messages


@router.post('/{chat_id}', response_model=MessageOut)
async def send_message(chat_id: int, payload: SendMessageRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    chat = db.get(Chat, chat_id)
    if not chat or current_user.id not in {m.id for m in chat.members}:
        raise HTTPException(status_code=404, detail='Chat not found')

    msg = Message(
        chat_id=chat_id,
        sender_id=current_user.id,
        body=payload.body,
        reply_to_message_id=payload.reply_to_message_id,
        forwarded_from_chat_id=payload.forwarded_from_chat_id,
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)

    await manager.broadcast(chat_id, {
        'event': 'new_message',
        'chat_id': chat_id,
        'message': MessageOut.model_validate(msg).model_dump(mode='json'),
    })
    return msg


@router.delete('/{message_id}')
async def delete_message(message_id: int, payload: DeleteMessageRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    msg = db.get(Message, message_id)
    if not msg:
        raise HTTPException(status_code=404, detail='Message not found')
    if msg.sender_id != current_user.id:
        raise HTTPException(status_code=403, detail='Only sender can delete in this MVP')

    chat_id = msg.chat_id
    if payload.delete_for_everyone:
        msg.deleted_for_everyone = True
        msg.body = '[deleted]'
    else:
        db.delete(msg)
    db.commit()

    await manager.broadcast(chat_id, {
        'event': 'message_deleted',
        'chat_id': chat_id,
        'message_id': message_id,
        'delete_for_everyone': payload.delete_for_everyone,
    })
    return {'status': 'deleted', 'delete_for_everyone': payload.delete_for_everyone}
