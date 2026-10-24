import asyncio
from pathlib import Path

from httpx import ASGITransport, AsyncClient, Response
from sqlalchemy import create_engine, text

from app.core.config import get_settings
from app.main import create_app


async def request_health() -> Response:
    transport = ASGITransport(app=create_app())
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        return await client.get("/api/health")


def test_health_check_with_sqlite(
    tmp_path: Path,
    monkeypatch,
) -> None:
    database_path = (tmp_path / "buildlog-test.sqlite3").as_posix()
    database_url = f"sqlite+pysqlite:///{database_path}"
    monkeypatch.setenv("TEST_DATABASE_URL", database_url)
    get_settings.cache_clear()

    settings = get_settings()
    engine = create_engine(settings.test_database_url)
    with engine.connect() as connection:
        assert connection.scalar(text("SELECT 1")) == 1

    response = asyncio.run(request_health())

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    engine.dispose()
    get_settings.cache_clear()


def test_cors_allows_only_frontend_origin() -> None:
    get_settings.cache_clear()
    settings = get_settings()

    async def request_cors_preflights() -> tuple[Response, Response]:
        transport = ASGITransport(app=create_app())
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            allowed_response = await client.options(
                "/api/health",
                headers={
                    "Origin": settings.frontend_origin,
                    "Access-Control-Request-Method": "GET",
                },
            )
            blocked_response = await client.options(
                "/api/health",
                headers={
                    "Origin": "https://example.com",
                    "Access-Control-Request-Method": "GET",
                },
            )
        return allowed_response, blocked_response

    allowed_response, blocked_response = asyncio.run(request_cors_preflights())

    assert allowed_response.status_code == 200
    assert allowed_response.headers["access-control-allow-origin"] == settings.frontend_origin
    assert "access-control-allow-origin" not in blocked_response.headers
