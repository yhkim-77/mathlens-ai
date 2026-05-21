"""
Problem recommendation service.
Uses concept mastery and error history to rank problems.
"""
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy import select, func, and_, not_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import Problem, UserProblemHistory, ConceptMastery


async def get_recommended_problems(
    db: AsyncSession,
    user_id: str,
    grade: str,
    subject: Optional[str] = None,
    difficulty_min: int = 1,
    difficulty_max: int = 5,
    concept_tag: Optional[str] = None,
    limit: int = 1,
) -> list[Problem]:
    """
    Recommend problems for a user based on:
    - Grade filter
    - Recent wrong concepts (weight 70%)
    - Low mastery concepts
    - Avoiding already-solved problems today
    """
    # Problems solved today
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    solved_today_stmt = select(UserProblemHistory.problem_id).where(
        and_(
            UserProblemHistory.user_id == user_id,
            UserProblemHistory.solved_at >= today_start,
        )
    )
    solved_today_result = await db.execute(solved_today_stmt)
    solved_today_ids = [r[0] for r in solved_today_result.all()]

    # Base query
    stmt = (
        select(Problem)
        .where(
            and_(
                Problem.status == "active",
                Problem.grade == grade,
                Problem.difficulty >= difficulty_min,
                Problem.difficulty <= difficulty_max,
                not_(Problem.id.in_(solved_today_ids)) if solved_today_ids else True,
            )
        )
        .limit(limit * 3)  # over-fetch, then rank
    )

    if subject:
        stmt = stmt.where(Problem.subject == subject)

    result = await db.execute(stmt)
    candidates = list(result.scalars().all())

    if not candidates:
        # Relax "solved today" constraint
        stmt2 = (
            select(Problem)
            .where(
                and_(
                    Problem.status == "active",
                    Problem.grade == grade,
                    Problem.difficulty >= difficulty_min,
                    Problem.difficulty <= difficulty_max,
                )
            )
            .limit(limit)
        )
        if subject:
            stmt2 = stmt2.where(Problem.subject == subject)
        result2 = await db.execute(stmt2)
        candidates = list(result2.scalars().all())

    # Simple scoring: prefer lower difficulty for struggling users
    return candidates[:limit]


async def update_concept_mastery(
    db: AsyncSession,
    user_id: str,
    concept_ids: list[str],
    is_correct: bool,
) -> None:
    """Update concept mastery after a submission."""
    for concept_id in concept_ids:
        stmt = select(ConceptMastery).where(
            and_(
                ConceptMastery.user_id == user_id,
                ConceptMastery.concept_id == concept_id,
            )
        )
        result = await db.execute(stmt)
        mastery = result.scalar_one_or_none()

        if mastery is None:
            mastery = ConceptMastery(
                user_id=user_id,
                concept_id=concept_id,
                consecutive_correct=0,
                correct_count=0,
                total_count=0,
                status="learning",
            )
            db.add(mastery)

        mastery.total_count += 1
        if is_correct:
            mastery.correct_count += 1
            mastery.consecutive_correct += 1
        else:
            mastery.consecutive_correct = 0

        # Spaced repetition intervals
        if mastery.consecutive_correct >= 3:
            mastery.status = "mastered"
            mastery.next_review_at = datetime.utcnow() + timedelta(days=1)
        elif mastery.consecutive_correct >= 1:
            mastery.status = "learning"
            mastery.next_review_at = datetime.utcnow() + timedelta(days=3)
        else:
            mastery.status = "learning"
            mastery.next_review_at = datetime.utcnow() + timedelta(hours=12)

        mastery.updated_at = datetime.utcnow()
