from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

chat_members = Table(
    'chat_members',
    Base.metadata,
    Column('chat_id', ForeignKey('chats.id'), primary_key=True),
    Column('user_id', ForeignKey('users.id'), primary_key=True),
)


class Chat(Base):
    __tablename__ = 'chats'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_direct: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    members: Mapped[List['User']] = relationship(secondary=chat_members, back_populates='chats')
    messages: Mapped[List['Message']] = relationship(back_populates='chat', cascade='all, delete-orphan')
