import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_root(client: AsyncClient):
    resp = await client.get("/")
    assert resp.status_code == 200
    data = resp.json()
    assert "MathLens" in data["message"]


@pytest.mark.asyncio
async def test_health(client: AsyncClient):
    resp = await client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_register_and_login(client: AsyncClient):
    # Register
    resp = await client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "password": "password123", "grade": "middle_2"},
    )
    assert resp.status_code == 201
    tokens = resp.json()
    assert "access_token" in tokens

    # Login
    resp2 = await client.post(
        "/api/v1/auth/token",
        data={"username": "test@example.com", "password": "password123"},
    )
    assert resp2.status_code == 200
    assert "access_token" in resp2.json()


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient):
    await client.post(
        "/api/v1/auth/register",
        json={"email": "dup@example.com", "password": "pass"},
    )
    resp = await client.post(
        "/api/v1/auth/register",
        json={"email": "dup@example.com", "password": "pass"},
    )
    assert resp.status_code == 400


@pytest.mark.asyncio
async def test_wrong_password(client: AsyncClient):
    await client.post(
        "/api/v1/auth/register",
        json={"email": "user2@example.com", "password": "correct"},
    )
    resp = await client.post(
        "/api/v1/auth/token",
        data={"username": "user2@example.com", "password": "wrong"},
    )
    assert resp.status_code == 401
