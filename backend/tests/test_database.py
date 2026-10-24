from datetime import UTC, datetime
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.base import Base
from app.db.session import create_db_engine
from app.models import Comment, ErrorRecord, Like, Report, StudyRecord, Todo, User

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ALEMBIC_INI = PROJECT_ROOT / "backend" / "alembic.ini"


@pytest.fixture
def session(tmp_path: Path) -> Session:
    database_url = f"sqlite+pysqlite:///{(tmp_path / 'models.sqlite3').as_posix()}"
    engine = create_db_engine(database_url)
    Base.metadata.create_all(engine)

    with Session(engine, expire_on_commit=False) as database_session:
        yield database_session

    engine.dispose()


def make_user(email: str, nickname: str) -> User:
    return User(
        email=email,
        password_hash="hashed-password-for-test",
        nickname=nickname,
    )


def test_models_store_records_with_safe_defaults(session: Session) -> None:
    author = make_user("author@example.com", "author")
    visitor = make_user("visitor@example.com", "visitor")
    study_record = StudyRecord(author=author, title="FastAPI", content="API 공부")
    todo = Todo(author=author, title="저장 버튼 만들기")
    error_record = ErrorRecord(
        author=author,
        title="ImportError",
        content="모듈을 찾을 수 없음",
    )
    study_comment = Comment(
        author=visitor,
        study_record=study_record,
        content="도움이 됐어요",
    )
    error_comment = Comment(
        author=visitor,
        error_record=error_record,
        content="같은 오류를 겪었어요",
    )
    like = Like(user=visitor, study_record=study_record)
    report = Report(reporter=visitor, todo=todo, reason="확인이 필요합니다")
    session.add_all(
        [
            author,
            visitor,
            study_record,
            todo,
            error_record,
            study_comment,
            error_comment,
            like,
            report,
        ]
    )
    session.commit()
    study_record_id = study_record.id
    todo_id = todo.id
    error_record_id = error_record.id
    session.expire_all()

    saved_study_record = session.get(StudyRecord, study_record_id)
    saved_todo = session.get(Todo, todo_id)
    saved_error_record = session.get(ErrorRecord, error_record_id)

    assert saved_study_record is not None
    assert saved_todo is not None
    assert saved_error_record is not None
    assert saved_study_record.is_public is False
    assert saved_todo.is_public is False
    assert saved_todo.is_completed is False
    assert saved_todo.completed_at is None
    assert saved_error_record.is_public is False
    assert saved_error_record.is_resolved is False
    assert saved_error_record.solution is None
    assert saved_error_record.resolved_at is None
    assert study_comment.study_record_id == study_record.id
    assert error_comment.error_record_id == error_record.id
    assert like.study_record_id == study_record.id
    assert report.todo_id == todo.id
    assert author.created_at is not None


def test_user_email_and_nickname_must_be_unique(session: Session) -> None:
    user = make_user("unique@example.com", "unique_user")
    session.add(user)
    session.commit()

    session.add(make_user("unique@example.com", "another_user"))
    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()

    session.add(make_user("another@example.com", "unique_user"))
    with pytest.raises(IntegrityError):
        session.commit()


def test_duplicate_likes_and_reports_are_rejected(session: Session) -> None:
    author = make_user("author@example.com", "author")
    visitor = make_user("visitor@example.com", "visitor")
    study_record = StudyRecord(author=author, title="SQLAlchemy", content="모델 공부")
    session.add_all([author, visitor, study_record])
    session.commit()

    session.add(Like(user=visitor, study_record=study_record))
    session.commit()
    session.add(Like(user=visitor, study_record=study_record))
    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()

    session.add(Report(reporter=visitor, study_record=study_record, reason="첫 신고"))
    session.commit()
    session.add(Report(reporter=visitor, study_record=study_record, reason="중복 신고"))
    with pytest.raises(IntegrityError):
        session.commit()


def test_status_dates_and_target_rules_are_enforced(session: Session) -> None:
    author = make_user("author@example.com", "author")
    session.add(author)
    session.commit()

    invalid_todo = Todo(
        author=author,
        title="완료 날짜 없는 할 일",
        is_completed=True,
    )
    session.add(invalid_todo)
    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()

    invalid_error = ErrorRecord(
        author=author,
        title="해결 방법 없는 오류",
        content="오류 내용",
        is_resolved=True,
        resolved_at=datetime.now(UTC),
    )
    session.add(invalid_error)
    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()

    invalid_comment = Comment(author=author, content="대상이 없는 댓글")
    session.add(invalid_comment)
    with pytest.raises(IntegrityError):
        session.commit()


def test_alembic_migration_matches_models(tmp_path: Path) -> None:
    database_path = (tmp_path / "migration.sqlite3").as_posix()
    database_url = f"sqlite+pysqlite:///{database_path}"
    alembic_config = Config(str(ALEMBIC_INI))
    alembic_config.set_main_option("sqlalchemy.url", database_url)

    command.upgrade(alembic_config, "head")

    engine = create_db_engine(database_url)
    table_names = set(inspect(engine).get_table_names())
    assert {
        "alembic_version",
        "users",
        "study_records",
        "todos",
        "error_records",
        "comments",
        "likes",
        "reports",
    } == table_names
    command.check(alembic_config)

    command.downgrade(alembic_config, "base")
    remaining_tables = set(inspect(engine).get_table_names())
    assert not remaining_tables.intersection(Base.metadata.tables)
    engine.dispose()
