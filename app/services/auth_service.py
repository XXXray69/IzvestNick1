import secrets
from typing import Optional
from sqlalchemy.orm import Session

from app.core.security import create_access_token, create_refresh_token
from app.models.device_session import DeviceSession
from app.models.user import User
from app.schemas.auth import TokenPairResponse


def normalize_phone(phone: str) -> str:
    return ''.join(ch for ch in phone if ch.isdigit())


def issue_session_tokens(db: Session, user: User, device_name: Optional[str]) -> TokenPairResponse:
    jti = secrets.token_urlsafe(24)
    session = DeviceSession(user_id=user.id, refresh_token_jti=jti, device_name=device_name)
    db.add(session)
    db.commit()
    access = create_access_token(user.id)
    refresh = create_refresh_token(user.id, jti)
    return TokenPairResponse(access_token=access, refresh_token=refresh)
