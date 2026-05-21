from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.models import User, ConceptMastery, UserProblemHistory, Submission, RecognitionResult

router = APIRouter()


class LearningReport(BaseModel):
    user_id: str
    period: str
    total_problems: int
    correct_rate: float
    weak_concepts: list[str]
    error_type_distribution: dict[str, float]
    study_streak: int
    mastered_concepts: list[str]


class ConceptMasteryOut(BaseModel):
    concept_id: str
    status: str
    mastery_level: int
    consecutive_correct: int
    correct_count: int
    total_count: int
    next_review_at: Optional[str]


@router.get("/users/{user_id}/report", response_model=LearningReport)
async def get_learning_report(
    user_id: str,
    period: str = Query("week", pattern="^(week|month|all)$"),
    db: AsyncSession = Depends(get_db),
):
    """Get user learning report for given period."""
    # Validate user
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="USER_NOT_FOUND")

    # Determine period start
    now = datetime.utcnow()
    if period == "week":
        start = now - timedelta(days=7)
        period_label = f"{start.strftime('%Y-%m-%d')} ~ {now.strftime('%Y-%m-%d')}"
    elif period == "month":
        start = now - timedelta(days=30)
        period_label = f"{start.strftime('%Y-%m-%d')} ~ {now.strftime('%Y-%m-%d')}"
    else:
        start = datetime(2000, 1, 1)
        period_label = "전체"

    # History in period
    stmt = select(UserProblemHistory).where(
        and_(
            UserProblemHistory.user_id == user_id,
            UserProblemHistory.solved_at >= start,
        )
    )
    res = await db.execute(stmt)
    history = res.scalars().all()

    total = len(history)
    correct = sum(1 for h in history if h.is_correct)
    correct_rate = round(correct / total, 2) if total > 0 else 0.0

    # Error distribution
    error_counts: dict[str, int] = {}
    for h in history:
        if h.error_type:
            error_counts[h.error_type] = error_counts.get(h.error_type, 0) + 1
    total_errors = sum(error_counts.values()) or 1
    error_dist = {k: round(v / total_errors, 2) for k, v in error_counts.items()}

    # Mastery data
    mastery_stmt = select(ConceptMastery).where(ConceptMastery.user_id == user_id)
    mastery_res = await db.execute(mastery_stmt)
    masteries = mastery_res.scalars().all()

    mastered = [m.concept_id for m in masteries if m.status == "mastered"]
    weak = [
        m.concept_id
        for m in sorted(
            [m for m in masteries if m.total_count > 0],
            key=lambda m: m.correct_count / m.total_count if m.total_count else 1,
        )[:3]
        if m.total_count > 0 and (m.correct_count / m.total_count) < 0.7
    ]

    # Study streak (consecutive days with at least 1 problem solved)
    streak = 0
    check_day = now.date()
    all_days = {h.solved_at.date() for h in history}
    while check_day in all_days:
        streak += 1
        check_day = check_day - timedelta(days=1)

    return LearningReport(
        user_id=user_id,
        period=period_label,
        total_problems=total,
        correct_rate=correct_rate,
        weak_concepts=weak,
        error_type_distribution=error_dist,
        study_streak=streak,
        mastered_concepts=mastered,
    )


@router.get("/users/{user_id}/mastery", response_model=list[ConceptMasteryOut])
async def get_concept_mastery(user_id: str, db: AsyncSession = Depends(get_db)):
    """Get per-concept mastery status for a user."""
    result = await db.execute(select(User).where(User.id == user_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="USER_NOT_FOUND")

    stmt = select(ConceptMastery).where(ConceptMastery.user_id == user_id)
    res = await db.execute(stmt)
    masteries = res.scalars().all()

    return [
        ConceptMasteryOut(
            concept_id=m.concept_id,
            status=m.status,
            mastery_level=int((m.correct_count / m.total_count * 100)) if m.total_count > 0 else 0,
            consecutive_correct=m.consecutive_correct,
            correct_count=m.correct_count,
            total_count=m.total_count,
            next_review_at=m.next_review_at.isoformat() if m.next_review_at else None,
        )
        for m in masteries
    ]


@router.get("/users/{user_id}/wrong-notes")
async def get_wrong_notes(
    user_id: str,
    limit: int = Query(50, le=200),
    error_type: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """Get wrong answer notes for a user."""
    result = await db.execute(select(User).where(User.id == user_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="USER_NOT_FOUND")

    conditions = [
        UserProblemHistory.user_id == user_id,
        UserProblemHistory.is_correct == False,  # noqa: E712 (SQLAlchemy requires ==)
    ]
    if error_type:
        conditions.append(UserProblemHistory.error_type == error_type)

    stmt = (
        select(UserProblemHistory)
        .where(and_(*conditions))
        .order_by(UserProblemHistory.solved_at.desc())
        .limit(limit)
    )
    res = await db.execute(stmt)
    history = res.scalars().all()

    return [
        {
            "history_id": h.id,
            "problem_id": h.problem_id,
            "submission_id": h.submission_id,
            "error_type": h.error_type,
            "solved_at": h.solved_at.isoformat(),
        }
        for h in history
    ]
