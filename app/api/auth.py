from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session
import random
import re
import string

from app.core.db import get_db
from app.core.security import hash_password, verify_password
from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest, TokenPairResponse
from app.schemas.user import UserOut
from app.services.auth_service import issue_session_tokens, normalize_phone

router = APIRouter(prefix='/auth', tags=['auth'])


def generate_unique_username_link(db: Session) -> str:
    alphabet = string.ascii_lowercase + string.digits
    while True:
        candidate = '@' + ''.join(random.choice(alphabet) for _ in range(9))
        exists = db.query(User).filter(User.username_link == candidate).first()
        if not exists:
            return candidate


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


@router.post('/register')
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    if payload.password != payload.confirm_password:
        raise HTTPException(status_code=400, detail='Passwords do not match')

    phone_number = normalize_phone(payload.phone_number)
    existing = db.query(User).filter(User.phone_number == phone_number).first()
    if existing:
        raise HTTPException(status_code=409, detail='Phone already registered')

    user = User(
        phone_prefix=payload.phone_prefix,
        phone_number=phone_number,
        password_hash=hash_password(payload.password),
        first_name='',
        last_name='',
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {'user_id': user.id, 'status': 'registered'}


@router.post('/complete-profile', response_model=UserOut)
def complete_profile(
    user_id: int = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    username_link: str | None = Form(None),
    db: Session = Depends(get_db),
):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    first_name = first_name.strip()
    last_name = last_name.strip()
    if not first_name or not last_name:
        raise HTTPException(status_code=400, detail='First name and last name are required')

    prepared_username = normalize_username_link(username_link)

    if prepared_username:
        if not validate_username_link(prepared_username):
            raise HTTPException(
                status_code=400,
                detail='ID must start with @ and contain only English letters and digits'
            )

        exists = db.query(User).filter(
            User.username_link == prepared_username,
            User.id != user.id
        ).first()
        if exists:
            raise HTTPException(status_code=409, detail='ID already taken')

        user.username_link = prepared_username
    elif not user.username_link:
        user.username_link = generate_unique_username_link(db)

    user.first_name = first_name
    user.last_name = last_name

    db.commit()
    db.refresh(user)
    return user


@router.post('/login', response_model=TokenPairResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    phone_number = normalize_phone(payload.phone_number)
    user = db.query(User).filter(User.phone_number == phone_number).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail='Invalid phone or password')
    return issue_session_tokens(db, user, payload.device_name)
