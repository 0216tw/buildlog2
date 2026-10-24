from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKey, String, false
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.report import Report
    from app.models.user import User


class Todo(TimestampMixin, Base):
    __tablename__ = "todos"
    __table_args__ = (
        CheckConstraint(
            "length(trim(title)) BETWEEN 1 AND 100",
            name="ck_todos_title_length",
        ),
        CheckConstraint(
            "(is_completed AND completed_at IS NOT NULL) OR "
            "(NOT is_completed AND completed_at IS NULL)",
            name="ck_todos_completed_at_matches_status",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    is_completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default=false(),
        nullable=False,
    )
    is_public: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default=false(),
        nullable=False,
    )
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    author: Mapped["User"] = relationship(back_populates="todos")
    reports: Mapped[list["Report"]] = relationship(
        back_populates="todo",
        cascade="all, delete-orphan",
        foreign_keys="Report.todo_id",
    )
