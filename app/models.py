from datetime import UTC, datetime

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """
    Common SQLAlchemy base class for all ORM models.

    Models inherit from Base so they share the same metadata registry
    (Base.metadata), allowing SQLAlchemy to discover and manage all
    tables together.
    """


class Url(Base):
    __tablename__ = "urls"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    short_code: Mapped[str | None] = mapped_column(String(10), unique=True, index=True)
    original_url: Mapped[str] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )
