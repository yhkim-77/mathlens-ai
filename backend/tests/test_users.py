import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import User
from app.core.database import get_db


@pytest.mark.asyncio
async def test_get_report_not_found(client: AsyncClient):
    resp = await client.get("/api/v1/users/nonexistent/report")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_get_mastery_not_found(client: AsyncClient):
    resp = await client.get("/api/v1/users/nonexistent/mastery")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_get_report_empty(client: AsyncClient, db_session: AsyncSession):
    # Create a user
    user = User(id="usr-report-test", email="report@test.com", grade="middle_2")
    db_session.add(user)
    await db_session.commit()

    resp = await client.get("/api/v1/users/usr-report-test/report")
    assert resp.status_code == 200
    data = resp.json()
    assert data["user_id"] == "usr-report-test"
    assert data["total_problems"] == 0
    assert data["correct_rate"] == 0.0
    assert data["study_streak"] == 0


@pytest.mark.asyncio
async def test_get_mastery_empty(client: AsyncClient, db_session: AsyncSession):
    user = User(id="usr-mastery-test", email="mastery@test.com", grade="high_1")
    db_session.add(user)
    await db_session.commit()

    resp = await client.get("/api/v1/users/usr-mastery-test/mastery")
    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.asyncio
async def test_get_wrong_notes_empty(client: AsyncClient, db_session: AsyncSession):
    user = User(id="usr-notes-test", email="notes@test.com", grade="middle_3")
    db_session.add(user)
    await db_session.commit()

    resp = await client.get("/api/v1/users/usr-notes-test/wrong-notes")
    assert resp.status_code == 200
    assert resp.json() == []
