from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.error_record import ErrorRecord
    from app.models.report import Report
    from app.models.study_record import StudyRecord
    from app.models.user import User


class Comment(TimestampMixin, Base):
    __tablename__ = "comments"
    __table_args__ = (
        CheckConstraint(
            "length(trim(content)) BETWEEN 1 AND 500",
            name="ck_comments_content_length",
        ),
        CheckConstraint(
            "(study_record_id IS NOT NULL) + (error_record_id IS NOT NULL) = 1",
            name="ck_comments_exactly_one_target",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    study_record_id: Mapped[int | None] = mapped_column(
        ForeignKey("study_records.id", ondelete="CASCADE"),
        index=True,
    )
    error_record_id: Mapped[int | None] = mapped_column(
        ForeignKey("error_records.id", ondelete="CASCADE"),
        index=True,
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)

    author: Mapped["User"] = relationship(back_populates="comments")
    study_record: Mapped["StudyRecord | None"] = relationship(
        back_populates="comments",
        foreign_keys=[study_record_id],
    )
    error_record: Mapped["ErrorRecord | None"] = relationship(
        back_populates="comments",
        foreign_keys=[error_record_id],
    )
    reports: Mapped[list["Report"]] = relationship(
        back_populates="comment",
        cascade="all, delete-orphan",
        foreign_keys="Report.comment_id",
    )
