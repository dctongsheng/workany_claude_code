"""Task database model."""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.message import Message
    from app.models.session import Session
    from app.models.file import File


class Task(Base):
    """Task model for AI execution tasks."""

    __tablename__ = "tasks"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    session_id: Mapped[str | None] = mapped_column(String, ForeignKey("sessions.id"))
    task_index: Mapped[int | None] = mapped_column(Integer, default=1)
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(
        String, default="running", nullable=False
    )  # pending, running, completed, error, stopped
    cost: Mapped[float | None] = mapped_column(Float, nullable=True)
    duration: Mapped[int | None] = mapped_column(Integer, nullable=True)  # milliseconds
    favorite: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )

    # Relationships
    session: Mapped["Session | None"] = relationship("Session", back_populates="tasks")
    messages: Mapped[list["Message"]] = relationship(
        "Message", back_populates="task", cascade="all, delete-orphan"
    )
    files: Mapped[list["File"]] = relationship(
        "File", back_populates="task", cascade="all, delete-orphan"
    )
