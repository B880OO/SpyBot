from datetime import datetime

from sqlalchemy import BigInteger, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from .base import Base


class User(Base):
    __tablename__ = "Users"

    Id: Mapped[int] = mapped_column(primary_key=True)
    Telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    First_name: Mapped[str] = mapped_column(String(255), nullable=False)
    Username: Mapped[str] = mapped_column(String(255), nullable=True)
    Started: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )


class MessageCache(Base):
    __tablename__ = "Messages"

    Id: Mapped[int] = mapped_column(primary_key=True)
    Message_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    Caption: Mapped[str] = mapped_column(String(2555), nullable=False)
    File_id: Mapped[str] = mapped_column(String(355), nullable=True)
    Chat_full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    Chat_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    User_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    Type: Mapped[str] = mapped_column(String(255), nullable=False, default="Message")
