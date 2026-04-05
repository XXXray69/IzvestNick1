import os
import re
import secrets

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.db import get_db
from app.core.security import get_current_user
from app.models.chat import Chat
from app.models.device_session import DeviceSession
from app.models.message import Message
from app.models.user import User
from app.schemas.user import SetProfileRequest, UserOut

router = APIRouter(prefix='/users', tags=['users'])


def normalize_username_link(raw: str | None) -> str | None:
    if raw is None:
        return None
    value = raw.strip()
    if not value:
        return None
    if not value.startswith('@'):
        value = '@' + value
    return value.lower()


def validate_username_link(value: str) -> bool:
    return bool(re.fullmatch(r'@[a-z0-9]+', value))


@router.get('/me', response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return current_user


@router.patch('/me', response_model=UserOut)
def update_me(
    payload: SetProfileRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if payload.first_name is not None:
        first_name = payload.first_name.strip()
        if not first_name:
            raise HTTPException(status_code=400, detail='First name cannot be empty')
        current_user.first_name = first_name

    if payload.last_name is not None:
        current_user.last_name = payload.last_name.strip()

    if payload.bio is not None:
        current_user.bio = payload.bio

    if payload.username_link is not None:
        prepared_username = normalize_username_link(payload.username_link)
        if prepared_username is None:
            current_user.username_link = None
        else:
            if not validate_username_link(prepared_username):
                raise HTTPException(
                    status_code=400,
                    detail='ID must start with @ and contain only English letters and digits'
                )

            exists = db.query(User).filter(
                User.username_link == prepared_username,
                User.id != current_user.id
            ).first()
            if exists:
                raise HTTPException(status_code=409, detail='ID already taken')

            current_user.username_link = prepared_username

    db.commit()
    db.refresh(current_user)
    return current_user


@router.post('/me/photos')
def upload_profile_photo(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    os.makedirs(settings.MEDIA_DIR, exist_ok=True)
    user_dir = os.path.join(settings.MEDIA_DIR, f'user_{current_user.id}')
    os.makedirs(user_dir, exist_ok=True)

    existing_files = [f for f in os.listdir(user_dir) if os.path.isfile(os.path.join(user_dir, f))]
    if len(existing_files) >= settings.MAX_PROFILE_PHOTOS:
        raise HTTPException(status_code=400, detail=f'Profile photo limit is {settings.MAX_PROFILE_PHOTOS}')

    ext = (file.filename or 'photo.bin').split('.')[-1]
    filepath = os.path.join(user_dir, f'{secrets.token_hex(8)}.{ext}')
    with open(filepath, 'wb') as out:
        out.write(file.file.read())

    if not current_user.main_photo_path:
        current_user.main_photo_path = filepath
        db.commit()

    return {'status': 'uploaded', 'path': filepath}


@router.post('/me/photos/set-main')
def set_main_photo(path: str = Form(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    current_user.main_photo_path = path
    db.commit()
    return {'status': 'updated', 'main_photo_path': path}


@router.delete('/me')
def delete_my_account(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db.query(Message).filter(Message.sender_id == current_user.id).delete(synchronize_session=False)
    db.query(DeviceSession).filter(DeviceSession.user_id == current_user.id).delete(synchronize_session=False)

    chats = db.query(Chat).all()
    for chat in chats:
        if current_user.id in {m.id for m in chat.members}:
            chat.members = [m for m in chat.members if m.id != current_user.id]

    chats = db.query(Chat).all()
    for chat in chats:
        if len(chat.members) <= 1:
            db.delete(chat)

    db.delete(current_user)
    db.commit()

    return {'status': 'deleted'}
