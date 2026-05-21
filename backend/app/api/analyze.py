from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
import base64

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.analysis import analyze_solution

router = APIRouter()


class AnalyzeRequest(BaseModel):
    image_base64: str
    problem_id: Optional[str] = None
    problem_text: Optional[str] = None
    recognized_latex: Optional[str] = None
    user_id: str
    student_grade: str = "middle_2"


class ErrorDetail(BaseModel):
    step: int
    error_type: str
    description: str
    correct_expression: str


class AnalyzeResponse(BaseModel):
    is_correct: bool
    recognized_latex: str
    steps: list[str]
    errors: list[dict]
    concept_understanding: str
    feedback: str
    concept_explanation: str
    recommended_concept_tags: list[str]
    confidence: float
    processing_time_ms: int


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_endpoint(request: AnalyzeRequest):
    """
    Synchronous analysis endpoint — use /submissions for async (recommended).
    Accepts base64 image + optional pre-recognized LaTeX and returns AI feedback.
    """
    if not request.image_base64.strip():
        raise HTTPException(status_code=400, detail="SUBMISSION_EMPTY_CANVAS")

    result = await analyze_solution(
        image_base64=request.image_base64,
        problem_text=request.problem_text,
        recognized_latex=request.recognized_latex or "",
        student_grade=request.student_grade,
    )

    return AnalyzeResponse(
        is_correct=result.get("is_correct", False),
        recognized_latex=result.get("recognized_latex", ""),
        steps=result.get("steps", []),
        errors=result.get("error_steps", []),
        concept_understanding=result.get("concept_understanding_summary", ""),
        feedback=result.get("feedback_message", ""),
        concept_explanation=result.get("concept_explanation", ""),
        recommended_concept_tags=result.get("recommended_concept_tags", []),
        confidence=result.get("confidence", 0.0),
        processing_time_ms=result.get("processing_time_ms", 0),
    )


@router.post("/analyze/image")
async def analyze_image(
    file: UploadFile = File(...),
    user_id: str = "",
    problem_id: str = "",
    student_grade: str = "middle_2",
):
    """Upload an image file and synchronously analyze the math solution."""
    from app.core.config import settings as _settings
    contents = await file.read()
    if len(contents) > _settings.MAX_IMAGE_UPLOAD_BYTES:
        raise HTTPException(status_code=400, detail="SUBMISSION_IMAGE_TOO_LARGE")

    image_base64 = base64.b64encode(contents).decode("utf-8")
    result = await analyze_solution(
        image_base64=image_base64,
        problem_text=None,
        recognized_latex="",
        student_grade=student_grade,
    )

    return {
        "user_id": user_id,
        "problem_id": problem_id,
        "is_correct": result.get("is_correct"),
        "recognized_latex": result.get("recognized_latex"),
        "steps": result.get("steps"),
        "errors": result.get("error_steps"),
        "feedback": result.get("feedback_message"),
        "concept_explanation": result.get("concept_explanation"),
        "recommended_concept_tags": result.get("recommended_concept_tags"),
        "confidence": result.get("confidence"),
        "processing_time_ms": result.get("processing_time_ms"),
    }
