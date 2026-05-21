import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_concepts_empty(client: AsyncClient):
    resp = await client.get("/api/v1/concepts")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


@pytest.mark.asyncio
async def test_create_and_get_concept(client: AsyncClient):
    payload = {
        "name": "일차방정식",
        "subject": "algebra",
        "grade": "middle_1",
        "description": "ax + b = 0 형태의 방정식",
        "formula": "x = -b/a",
        "prerequisites": [],
        "related_concepts": [],
    }
    create_resp = await client.post("/api/v1/concepts", json=payload)
    assert create_resp.status_code == 201
    created = create_resp.json()
    concept_id = created["id"]
    assert created["name"] == "일차방정식"

    get_resp = await client.get(f"/api/v1/concepts/{concept_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["id"] == concept_id


@pytest.mark.asyncio
async def test_concept_not_found(client: AsyncClient):
    resp = await client.get("/api/v1/concepts/nonexistent")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_concept_explanation(client: AsyncClient):
    """Explanation endpoint uses mock when API key not set."""
    # Create a concept first
    create_resp = await client.post(
        "/api/v1/concepts",
        json={
            "name": "이차방정식",
            "subject": "algebra",
            "grade": "middle_3",
            "description": "ax^2 + bx + c = 0",
            "formula": r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}",
        },
    )
    concept_id = create_resp.json()["id"]

    resp = await client.get(f"/api/v1/concepts/{concept_id}/explanation?grade=middle_3")
    assert resp.status_code == 200
    data = resp.json()
    assert "explanation" in data
    assert data["concept_id"] == concept_id
