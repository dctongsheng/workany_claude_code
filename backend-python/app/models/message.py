"""Message database model."""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.task import Task


class Message(Base):
    """Message model for task execution messages."""

    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    task_id: Mapped[str] = mapped_column(String, ForeignKey("tasks.id"), nullable=False)
    type: Mapped[str] = mapped_column(
        String, nullable=False
    )  # text, tool_use, tool_result, result, error, user, plan
    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    tool_name: Mapped[str | None] = mapped_column(String, nullable=True)
    tool_input: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON
    tool_output: Mapped[str | None] = mapped_column(Text, nullable=True)
    tool_use_id: Mapped[str | None] = mapped_column(String, nullable=True)
    subtype: Mapped[str | None] = mapped_column(String, nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    attachments: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )

    # Relationships
    task: Mapped["Task"] = relationship("Task", back_populates="messages")
