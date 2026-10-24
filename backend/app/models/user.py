from enum import StrEnum
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.comment import Comment
    from app.models.error_record import ErrorRecord
    from app.models.like import Like
    from app.models.report import Report
    from app.models.study_record import StudyRecord
    from app.models.todo import Todo


class UserRole(StrEnum):
    USER = "user"
    ADMIN = "admin"


class User(TimestampMixin, Base):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint(
            "length(trim(email)) BETWEEN 3 AND 320",
            name="ck_users_email_length",
        ),
        CheckConstraint(
            "length(password_hash) > 0",
            name="ck_users_password_hash_not_empty",
        ),
        CheckConstraint(
            "length(trim(nickname)) BETWEEN 2 AND 20",
            name="ck_users_nickname_length",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(320), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    nickname: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    role: Mapped[UserRole] = mapped_column(
        Enum(
            UserRole,
            values_callable=lambda roles: [role.value for role in roles],
            native_enum=False,
            create_constraint=True,
            length=20,
            name="user_role",
        ),
        default=UserRole.USER,
        server_default=UserRole.USER.value,
        nullable=False,
    )

    study_records: Mapped[list["StudyRecord"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan",
    )
    todos: Mapped[list["Todo"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan",
    )
    error_records: Mapped[list["ErrorRecord"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan",
    )
    comments: Mapped[list["Comment"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan",
    )
    likes: Mapped[list["Like"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    reports: Mapped[list["Report"]] = relationship(
        back_populates="reporter",
        cascade="all, delete-orphan",
        foreign_keys="Report.reporter_id",
    )
