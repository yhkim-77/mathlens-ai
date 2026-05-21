import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_problems_empty(client: AsyncClient):
    resp = await client.get("/api/v1/problems")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


@pytest.mark.asyncio
async def test_create_and_get_problem(client: AsyncClient):
    payload = {
        "title": "일차방정식 풀기",
        "content_text": "다음 일차방정식을 풀어라. $2x + 1 = 5$",
        "subject": "algebra",
        "grade": "middle_1",
        "difficulty": 2,
        "concept_tags": ["일차방정식"],
        "answer_latex": "x = 2",
    }
    create_resp = await client.post("/api/v1/problems", json=payload)
    assert create_resp.status_code == 201
    created = create_resp.json()
    problem_id = created["id"]
    assert created["title"] == payload["title"]

    # Get by ID
    get_resp = await client.get(f"/api/v1/problems/{problem_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["id"] == problem_id


@pytest.mark.asyncio
async def test_get_problem_not_found(client: AsyncClient):
    resp = await client.get("/api/v1/problems/nonexistent-id")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_get_problems_filter(client: AsyncClient):
    # Create a problem to filter
    await client.post(
        "/api/v1/problems",
        json={
            "title": "이차방정식",
            "content_text": "$x^2 - 4 = 0$",
            "subject": "algebra",
            "grade": "middle_3",
            "difficulty": 3,
            "concept_tags": ["이차방정식"],
        },
    )
    resp = await client.get("/api/v1/problems?grade=middle_3&subject=algebra")
    assert resp.status_code == 200
    problems = resp.json()
    assert any(p["grade"] == "middle_3" for p in problems)


@pytest.mark.asyncio
async def test_recommend_problems(client: AsyncClient):
    """Recommendation returns a list (possibly empty if no problems for grade)."""
    resp = await client.get(
        "/api/v1/problems/recommend?user_id=testuser&grade=high_1"
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "problems" in data
    assert "recommendation_meta" in data
