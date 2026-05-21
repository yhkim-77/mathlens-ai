"""
Submission API — POST /submissions, GET /submissions/{id}/status
WebSocket /ws/v1/submissions/{id}
"""
import asyncio
import base64
import uuid
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import get_current_user
from app.core.database import get_db
from app.models.models import (
    Problem, RecognitionResult, Submission,
    User, UserProblemHistory,
)
from app.services.analysis import analyze_solution
from app.services.problems import update_concept_mastery

router = APIRouter()

# In-memory WebSocket registry  {submission_id: [WebSocket]}
_ws_clients: dict[str, list[WebSocket]] = {}


class SubmissionRequest(BaseModel):
    user_id: str
    problem_id: Optional[str] = None
    session_id: Optional[str] = None
    image_base64: str
    image_mime_type: str = "image/png"
    recognized_latex: Optional[str] = None  # pre-recognized by client (iink SDK)
    stroke_metadata: Optional[dict] = None
    client_timestamp: Optional[str] = None
    device_info: Optional[dict] = None


class SubmissionResponse(BaseModel):
    submission_id: str
    status: str
    websocket_url: str
    estimated_processing_time_ms: int = 5000


class SubmissionStatusResponse(BaseModel):
    submission_id: str
    status: str
    result: Optional[dict] = None


async def _broadcast(submission_id: str, message: dict):
    clients = _ws_clients.get(submission_id, [])
    disconnected = []
    for ws in clients:
        try:
            await ws.send_json(message)
        except Exception:
            disconnected.append(ws)
    for ws in disconnected:
        clients.remove(ws)


async def _process_submission(
    submission_id: str,
    image_base64: str,
    recognized_latex: str,
    problem_text: Optional[str],
    user_id: str,
    problem_id: Optional[str],
):
    """Background task: run AI analysis and persist result."""
    from app.core.database import AsyncSessionLocal
    from app.core.config import settings

    async with AsyncSessionLocal() as db:
        # Update status → processing
        result = await db.execute(select(Submission).where(Submission.id == submission_id))
        submission = result.scalar_one_or_none()
        if not submission:
            return

        submission.status = "processing"
        await db.commit()
        await _broadcast(submission_id, {"stage": "processing", "ts": datetime.utcnow().isoformat()})

        # Run AI analysis
        analysis = await analyze_solution(
            image_base64=image_base64,
            problem_text=problem_text,
            recognized_latex=recognized_latex,
        )

        # Save recognition result
        rec = RecognitionResult(
            submission_id=submission_id,
            htr_raw_latex=analysis.get("recognized_latex", recognized_latex),
            htr_steps=analysis.get("steps"),
            htr_confidence=analysis.get("confidence"),
            is_correct=analysis.get("is_correct"),
            error_steps=analysis.get("error_steps"),
            error_type=analysis.get("error_steps", [{}])[0].get("error_type") if analysis.get("error_steps") else None,
            error_subtype=analysis.get("error_steps", [{}])[0].get("error_subtype") if analysis.get("error_steps") else None,
            error_step=analysis.get("error_steps", [{}])[0].get("step_order") if analysis.get("error_steps") else None,
            feedback_text=analysis.get("feedback_message"),
            concept_explanation=analysis.get("concept_explanation"),
            correct_solution_latex=None,
            concept_tags_inferred=analysis.get("recommended_concept_tags"),
            llm_model_version=settings.OPENAI_MODEL,
            confidence=analysis.get("confidence"),
            processing_time_ms=analysis.get("processing_time_ms"),
        )
        db.add(rec)

        # Update submission status
        submission.status = "completed"
        submission.processed_at = datetime.utcnow()

        # Record problem history
        history = UserProblemHistory(
            user_id=user_id,
            problem_id=problem_id or submission_id,
            submission_id=submission_id,
            is_correct=analysis.get("is_correct"),
            error_type=rec.error_type,
        )
        db.add(history)

        await db.commit()

        # Update concept mastery
        concept_tags = analysis.get("recommended_concept_tags") or []
        if concept_tags:
            await update_concept_mastery(db, user_id, concept_tags, analysis.get("is_correct", False))
            await db.commit()

        await _broadcast(
            submission_id,
            {
                "stage": "analysis_done",
                "result_id": rec.id,
                "is_correct": analysis.get("is_correct"),
                "ts": datetime.utcnow().isoformat(),
            },
        )


@router.post("/submissions", response_model=SubmissionResponse, status_code=202)
async def create_submission(
    request: SubmissionRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """
    Accept a handwritten math solution for async AI analysis.
    Returns 202 immediately; use WebSocket for progress.
    """
    # Validate image size (~2MB after base64)
    if len(request.image_base64) > 2_800_000:
        raise HTTPException(status_code=400, detail="SUBMISSION_IMAGE_TOO_LARGE")

    if not request.image_base64.strip():
        raise HTTPException(status_code=400, detail="SUBMISSION_EMPTY_CANVAS")

    # Fetch problem text if problem_id is given
    problem_text: Optional[str] = None
    if request.problem_id:
        result = await db.execute(select(Problem).where(Problem.id == request.problem_id))
        prob = result.scalar_one_or_none()
        if prob:
            problem_text = prob.content_text

    # Create submission record
    submission = Submission(
        user_id=request.user_id,
        problem_id=request.problem_id,
        session_id=request.session_id or str(uuid.uuid4()),
        stroke_metadata=request.stroke_metadata,
        device_info=request.device_info,
        status="received",
    )
    db.add(submission)
    await db.flush()
    submission_id = submission.id

    background_tasks.add_task(
        _process_submission,
        submission_id=submission_id,
        image_base64=request.image_base64,
        recognized_latex=request.recognized_latex or "",
        problem_text=problem_text,
        user_id=request.user_id,
        problem_id=request.problem_id,
    )

    return SubmissionResponse(
        submission_id=submission_id,
        status="received",
        websocket_url=f"/ws/v1/submissions/{submission_id}",
    )


@router.get("/submissions/{submission_id}/status", response_model=SubmissionStatusResponse)
async def get_submission_status(
    submission_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Poll submission status (fallback when WebSocket is unavailable)."""
    result = await db.execute(
        select(Submission)
        .options(selectinload(Submission.recognition_result))
        .where(Submission.id == submission_id)
    )
    submission = result.scalar_one_or_none()
    if not submission:
        raise HTTPException(status_code=404, detail="SUBMISSION_NOT_FOUND")

    response_data: dict = {"submission_id": submission_id, "status": submission.status}
    rec = submission.recognition_result
    if submission.status == "completed" and rec:
        response_data["result"] = {
            "is_correct": rec.is_correct,
            "recognized_latex": rec.htr_raw_latex,
            "steps": rec.htr_steps,
            "errors": rec.error_steps,
            "feedback": rec.feedback_text,
            "concept_explanation": rec.concept_explanation,
            "confidence": rec.confidence,
        }

    return SubmissionStatusResponse(**response_data)


@router.get("/results/{submission_id}")
async def get_result(submission_id: str, db: AsyncSession = Depends(get_db)):
    """Get full analysis result for a completed submission."""
    stmt = (
        select(Submission)
        .options(selectinload(Submission.recognition_result))
        .where(Submission.id == submission_id)
    )
    result = await db.execute(stmt)
    submission = result.scalar_one_or_none()
    if not submission:
        raise HTTPException(status_code=404, detail="SUBMISSION_NOT_FOUND")

    rec = submission.recognition_result
    return {
        "submission_id": submission_id,
        "problem_id": submission.problem_id,
        "user_id": submission.user_id,
        "submitted_at": submission.submitted_at.isoformat() if submission.submitted_at else None,
        "status": submission.status,
        "htr_result": {
            "raw_latex": rec.htr_raw_latex if rec else None,
            "steps": rec.htr_steps if rec else None,
            "overall_confidence": rec.htr_confidence if rec else None,
        },
        "analysis_result": {
            "is_correct": rec.is_correct if rec else None,
            "error_type": rec.error_type if rec else None,
            "error_subtype": rec.error_subtype if rec else None,
            "error_step": rec.error_step if rec else None,
            "feedback_text": rec.feedback_text if rec else None,
            "concept_explanation": rec.concept_explanation if rec else None,
            "concept_tags_inferred": rec.concept_tags_inferred if rec else None,
            "confidence": rec.confidence if rec else None,
            "processing_time_ms": rec.processing_time_ms if rec else None,
        } if rec else None,
    }


@router.websocket("/ws/v1/submissions/{submission_id}")
async def websocket_status(websocket: WebSocket, submission_id: str):
    """WebSocket endpoint for real-time processing status."""
    await websocket.accept()
    if submission_id not in _ws_clients:
        _ws_clients[submission_id] = []
    _ws_clients[submission_id].append(websocket)

    try:
        while True:
            # Keep connection alive; send pings
            await asyncio.sleep(30)
            await websocket.send_json({"type": "ping"})
    except WebSocketDisconnect:
        if submission_id in _ws_clients:
            try:
                _ws_clients[submission_id].remove(websocket)
            except ValueError:
                pass
