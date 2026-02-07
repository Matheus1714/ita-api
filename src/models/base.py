from datetime import datetime, timezone

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
  created_at: Mapped[datetime] = mapped_column(DateTime, default=timezone.now())
  updated_at: Mapped[datetime] = mapped_column(
    DateTime, default=timezone.now(), onupdate=timezone.now()
  )
