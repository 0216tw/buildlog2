from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKey, String, Text, false
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.comment import Comment
    from app.models.like import Like
    from app.models.report import Report
    from app.models.user import User


class ErrorRecord(TimestampMixin, Base):
    __tablename__ = "error_records"
    __table_args__ = (
        CheckConstraint(
            "length(trim(title)) BETWEEN 1 AND 100",
            name="ck_error_records_title_length",
        ),
        CheckConstraint(
            "length(trim(content)) BETWEEN 1 AND 5000",
            name="ck_error_records_content_length",
        ),
        CheckConstraint(
            "solution IS NULL OR length(trim(solution)) BETWEEN 1 AND 5000",
            name="ck_error_records_solution_length",
        ),
        CheckConstraint(
            "NOT is_resolved OR solution IS NOT NULL",
            name="ck_error_records_resolved_requires_solution",
        ),
        CheckConstraint(
            "(is_resolved AND resolved_at IS NOT NULL) OR "
            "(NOT is_resolved AND resolved_at IS NULL)",
            name="ck_error_records_resolved_at_matches_status",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    solution: Mapped[str | None] = mapped_column(Text)
    is_resolved: Mapped[bool] = mapped_column(
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
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    author: Mapped["User"] = relationship(back_populates="error_records")
    comments: Mapped[list["Comment"]] = relationship(
        back_populates="error_record",
        cascade="all, delete-orphan",
        foreign_keys="Comment.error_record_id",
    )
    likes: Mapped[list["Like"]] = relationship(
        back_populates="error_record",
        cascade="all, delete-orphan",
        foreign_keys="Like.error_record_id",
    )
    reports: Mapped[list["Report"]] = relationship(
        back_populates="error_record",
        cascade="all, delete-orphan",
        foreign_keys="Report.error_record_id",
    )
