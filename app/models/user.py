from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    phone_prefix: Mapped[str] = mapped_column(String(12), default='+7')
    phone_number: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(512))
    first_name: Mapped[str] = mapped_column(String(100), default='')
    last_name: Mapped[str] = mapped_column(String(100), default='')
    username_link: Mapped[Optional[str]] = mapped_column(String(64), unique=True, nullable=True)
    bio: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)
    main_photo_path: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    chats: Mapped[List['Chat']] = relationship(secondary='chat_members', back_populates='members')
    sessions: Mapped[List['DeviceSession']] = relationship(back_populates='user', cascade='all, delete-orphan')
