from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.comment import Comment
    from app.models.error_record import ErrorRecord
    from app.models.study_record import StudyRecord
    from app.models.todo import Todo
    from app.models.user import User


class Report(Base):
    __tablename__ = "reports"
    __table_args__ = (
        CheckConstraint(
            "length(trim(reason)) BETWEEN 1 AND 500",
            name="ck_reports_reason_length",
        ),
        CheckConstraint(
            "(study_record_id IS NOT NULL) + (todo_id IS NOT NULL) + "
            "(error_record_id IS NOT NULL) + (comment_id IS NOT NULL) = 1",
            name="ck_reports_exactly_one_target",
        ),
        UniqueConstraint(
            "reporter_id",
            "study_record_id",
            name="uq_reports_reporter_study_record",
        ),
        UniqueConstraint(
            "reporter_id",
            "todo_id",
            name="uq_reports_reporter_todo",
        ),
        UniqueConstraint(
            "reporter_id",
            "error_record_id",
            name="uq_reports_reporter_error_record",
        ),
        UniqueConstraint(
            "reporter_id",
            "comment_id",
            name="uq_reports_reporter_comment",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    reporter_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    study_record_id: Mapped[int | None] = mapped_column(
        ForeignKey("study_records.id", ondelete="CASCADE"),
        index=True,
    )
    todo_id: Mapped[int | None] = mapped_column(
        ForeignKey("todos.id", ondelete="CASCADE"),
        index=True,
    )
    error_record_id: Mapped[int | None] = mapped_column(
        ForeignKey("error_records.id", ondelete="CASCADE"),
        index=True,
    )
    comment_id: Mapped[int | None] = mapped_column(
        ForeignKey("comments.id", ondelete="CASCADE"),
        index=True,
    )
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    reporter: Mapped["User"] = relationship(
        back_populates="reports",
        foreign_keys=[reporter_id],
    )
    study_record: Mapped["StudyRecord | None"] = relationship(
        back_populates="reports",
        foreign_keys=[study_record_id],
    )
    todo: Mapped["Todo | None"] = relationship(
        back_populates="reports",
        foreign_keys=[todo_id],
    )
    error_record: Mapped["ErrorRecord | None"] = relationship(
        back_populates="reports",
        foreign_keys=[error_record_id],
    )
    comment: Mapped["Comment | None"] = relationship(
        back_populates="reports",
        foreign_keys=[comment_id],
    )
