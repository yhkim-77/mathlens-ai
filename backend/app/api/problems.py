from fastapi import APIRouter, Query, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.models import Problem
from app.services.analysis import generate_similar_problem
from app.services.problems import get_recommended_problems

router = APIRouter()


class ProblemOut(BaseModel):
    id: str
    title: str
    content_text: str
    subject: str
    grade: str
    difficulty: int
    concept_tags: list[str]
    error_type_tags: list[str]
    source: str
    status: str
    estimated_solve_time_min: int
    image_url: Optional[str] = None

    class Config:
        from_attributes = True


class ProblemCreate(BaseModel):
    title: str
    content_text: str
    subject: str
    grade: str
    difficulty: int = 3
    concept_tags: list[str] = []
    error_type_tags: list[str] = []
    answer_latex: Optional[str] = None
    curriculum_code: Optional[str] = None


class GenerateProblemRequest(BaseModel):
    concept_tags: list[str]
    difficulty: int
    error_type: str
    grade: str
    source_problem_id: Optional[str] = None


class RecommendResponse(BaseModel):
    problems: list[dict]
    recommendation_meta: dict


@router.get("/problems", response_model=list[ProblemOut])
async def get_problems(
    grade: Optional[str] = Query(None),
    subject: Optional[str] = Query(None),
    difficulty: Optional[int] = Query(None),
    concept_tag: Optional[str] = Query(None),
    status: Optional[str] = Query("active"),
    limit: int = Query(20, le=100),
    db: AsyncSession = Depends(get_db),
):
    """List problems with optional filters."""
    conditions = []
    if grade:
        conditions.append(Problem.grade == grade)
    if subject:
        conditions.append(Problem.subject == subject)
    if difficulty:
        conditions.append(Problem.difficulty == difficulty)
    if status:
        conditions.append(Problem.status == status)

    stmt = select(Problem)
    if conditions:
        stmt = stmt.where(and_(*conditions))
    stmt = stmt.limit(limit)

    result = await db.execute(stmt)
    problems = result.scalars().all()

    return [
        ProblemOut(
            id=p.id,
            title=p.title,
            content_text=p.content_text,
            subject=p.subject,
            grade=p.grade,
            difficulty=p.difficulty,
            concept_tags=p.concept_tags or [],
            error_type_tags=p.error_type_tags or [],
            source=p.source,
            status=p.status,
            estimated_solve_time_min=p.estimated_solve_time_min,
        )
        for p in problems
    ]


@router.get("/problems/recommend", response_model=RecommendResponse)
async def recommend_problems(
    user_id: str = Query(...),
    grade: str = Query(...),
    subject: Optional[str] = Query(None),
    difficulty_min: int = Query(1, ge=1, le=5),
    difficulty_max: int = Query(5, ge=1, le=5),
    concept_tag: Optional[str] = Query(None),
    limit: int = Query(1, le=10),
    db: AsyncSession = Depends(get_db),
):
    """Recommend personalized problems for a user."""
    problems = await get_recommended_problems(
        db=db,
        user_id=user_id,
        grade=grade,
        subject=subject,
        difficulty_min=difficulty_min,
        difficulty_max=difficulty_max,
        concept_tag=concept_tag,
        limit=limit,
    )

    return RecommendResponse(
        problems=[
            {
                "problem_id": p.id,
                "title": p.title,
                "content_text": p.content_text,
                "subject": p.subject,
                "grade": p.grade,
                "difficulty": p.difficulty,
                "concept_tags": p.concept_tags or [],
                "estimated_solve_time_min": p.estimated_solve_time_min,
            }
            for p in problems
        ],
        recommendation_meta={
            "reason": "개념 기반 추천",
            "algorithm_version": "1.0",
        },
    )


@router.get("/problems/{problem_id}", response_model=ProblemOut)
async def get_problem(problem_id: str, db: AsyncSession = Depends(get_db)):
    """Get a specific problem by ID."""
    result = await db.execute(select(Problem).where(Problem.id == problem_id))
    problem = result.scalar_one_or_none()
    if not problem:
        raise HTTPException(status_code=404, detail="PROBLEM_NOT_FOUND")
    return ProblemOut(
        id=problem.id,
        title=problem.title,
        content_text=problem.content_text,
        subject=problem.subject,
        grade=problem.grade,
        difficulty=problem.difficulty,
        concept_tags=problem.concept_tags or [],
        error_type_tags=problem.error_type_tags or [],
        source=problem.source,
        status=problem.status,
        estimated_solve_time_min=problem.estimated_solve_time_min,
    )


@router.post("/problems", response_model=ProblemOut, status_code=201)
async def create_problem(body: ProblemCreate, db: AsyncSession = Depends(get_db)):
    """Create a new problem in the problem bank."""
    problem = Problem(
        title=body.title,
        content_text=body.content_text,
        subject=body.subject,
        grade=body.grade,
        difficulty=body.difficulty,
        concept_tags=body.concept_tags,
        error_type_tags=body.error_type_tags,
        answer_latex=body.answer_latex,
        curriculum_code=body.curriculum_code,
        source="bank",
        status="active",
    )
    db.add(problem)
    await db.flush()
    return ProblemOut(
        id=problem.id,
        title=problem.title,
        content_text=problem.content_text,
        subject=problem.subject,
        grade=problem.grade,
        difficulty=problem.difficulty,
        concept_tags=problem.concept_tags or [],
        error_type_tags=problem.error_type_tags or [],
        source=problem.source,
        status=problem.status,
        estimated_solve_time_min=problem.estimated_solve_time_min,
    )


@router.post("/problems/generate")
async def generate_problem(request: GenerateProblemRequest, db: AsyncSession = Depends(get_db)):
    """Generate a similar problem using AI (GPT-4o)."""
    # Optionally look up the source problem text
    source_text: Optional[str] = None
    if request.source_problem_id:
        result = await db.execute(
            select(Problem).where(Problem.id == request.source_problem_id)
        )
        src = result.scalar_one_or_none()
        if src:
            source_text = src.content_text

    generated = await generate_similar_problem(
        concept_tags=request.concept_tags,
        difficulty=request.difficulty,
        error_type=request.error_type,
        grade=request.grade,
        source_problem_text=source_text,
    )

    # Save to DB
    problem = Problem(
        title=generated.get("title", "AI 생성 문제"),
        content_text=generated.get("content_text", ""),
        answer_latex=generated.get("answer_latex"),
        subject=request.concept_tags[0] if request.concept_tags else "algebra",
        grade=request.grade,
        difficulty=request.difficulty,
        concept_tags=generated.get("concept_tags", request.concept_tags),
        source="llm_generated",
        status="active",
    )
    db.add(problem)
    await db.flush()

    return {
        "problem_id": problem.id,
        "problem_latex": generated.get("content_text"),
        "answer_latex": generated.get("answer_latex"),
        "hint": generated.get("hint"),
        "concept_ids": generated.get("concept_tags", request.concept_tags),
    }
