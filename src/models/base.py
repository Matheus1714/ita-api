from datetime import datetime, timezone

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def _utc_now() -> datetime:
  return datetime.now(timezone.utc)


class Base(DeclarativeBase):
  created_at: Mapped[datetime] = mapped_column(DateTime, default=_utc_now)
  updated_at: Mapped[datetime] = mapped_column(
    DateTime, default=_utc_now, onupdate=_utc_now
  )
