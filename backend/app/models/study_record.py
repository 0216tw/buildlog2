from typing import TYPE_CHECKING

from sqlalchemy import Boolean, CheckConstraint, ForeignKey, String, Text, false
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.comment import Comment
    from app.models.like import Like
    from app.models.report import Report
    from app.models.user import User


class StudyRecord(TimestampMixin, Base):
    __tablename__ = "study_records"
    __table_args__ = (
        CheckConstraint(
            "length(trim(title)) BETWEEN 1 AND 100",
            name="ck_study_records_title_length",
        ),
        CheckConstraint(
            "length(trim(content)) BETWEEN 1 AND 5000",
            name="ck_study_records_content_length",
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
    is_public: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default=false(),
        nullable=False,
    )

    author: Mapped["User"] = relationship(back_populates="study_records")
    comments: Mapped[list["Comment"]] = relationship(
        back_populates="study_record",
        cascade="all, delete-orphan",
        foreign_keys="Comment.study_record_id",
    )
    likes: Mapped[list["Like"]] = relationship(
        back_populates="study_record",
        cascade="all, delete-orphan",
        foreign_keys="Like.study_record_id",
    )
    reports: Mapped[list["Report"]] = relationship(
        back_populates="study_record",
        cascade="all, delete-orphan",
        foreign_keys="Report.study_record_id",
    )
