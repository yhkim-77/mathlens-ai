import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_analyze_mock(client: AsyncClient):
    """Analyze endpoint uses mock when OPENAI_API_KEY is not set."""
    import base64
    # 1x1 white PNG
    png_bytes = (
        b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01'
        b'\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00'
        b'\x00\x0cIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x05\x18'
        b'\xd8N\x00\x00\x00\x00IEND\xaeB`\x82'
    )
    b64 = base64.b64encode(png_bytes).decode()

    resp = await client.post(
        "/api/v1/analyze",
        json={
            "image_base64": b64,
            "user_id": "testuser",
            "recognized_latex": "x = 1",
            "student_grade": "middle_2",
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "is_correct" in data
    assert "feedback" in data
    assert "recognized_latex" in data


@pytest.mark.asyncio
async def test_analyze_empty_canvas(client: AsyncClient):
    resp = await client.post(
        "/api/v1/analyze",
        json={"image_base64": "   ", "user_id": "testuser"},
    )
    assert resp.status_code == 400


@pytest.mark.asyncio
async def test_submission_flow(client: AsyncClient):
    """Submit → status check."""
    import base64
    png_bytes = (
        b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01'
        b'\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00'
        b'\x00\x0cIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x05\x18'
        b'\xd8N\x00\x00\x00\x00IEND\xaeB`\x82'
    )
    b64 = base64.b64encode(png_bytes).decode()

    resp = await client.post(
        "/api/v1/submissions",
        json={
            "user_id": "testuser2",
            "image_base64": b64,
            "recognized_latex": "2x = 4",
        },
    )
    assert resp.status_code == 202
    data = resp.json()
    assert "submission_id" in data
    assert data["status"] == "received"

    # Check status
    sid = data["submission_id"]
    status_resp = await client.get(f"/api/v1/submissions/{sid}/status")
    assert status_resp.status_code == 200
    assert status_resp.json()["submission_id"] == sid
