import os
import secrets

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.db import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.user import SetProfileRequest, UserOut

router = APIRouter(prefix='/users', tags=['users'])


@router.get('/me', response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return current_user


@router.patch('/me', response_model=UserOut)
def update_me(payload: SetProfileRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    current_user.username_link = payload.username_link
    current_user.bio = payload.bio
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
