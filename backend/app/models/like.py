from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.error_record import ErrorRecord
    from app.models.study_record import StudyRecord
    from app.models.user import User


class Like(Base):
    __tablename__ = "likes"
    __table_args__ = (
        CheckConstraint(
            "(study_record_id IS NOT NULL) + (error_record_id IS NOT NULL) = 1",
            name="ck_likes_exactly_one_target",
        ),
        UniqueConstraint(
            "user_id",
            "study_record_id",
            name="uq_likes_user_study_record",
        ),
        UniqueConstraint(
            "user_id",
            "error_record_id",
            name="uq_likes_user_error_record",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
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
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    user: Mapped["User"] = relationship(back_populates="likes")
    study_record: Mapped["StudyRecord | None"] = relationship(
        back_populates="likes",
        foreign_keys=[study_record_id],
    )
    error_record: Mapped["ErrorRecord | None"] = relationship(
        back_populates="likes",
        foreign_keys=[error_record_id],
    )
