from fastapi import APIRouter, Query, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.models import Concept

router = APIRouter()


class ConceptOut(BaseModel):
    id: str
    name: str
    subject: str
    grade: str
    description: Optional[str]
    formula: Optional[str]
    prerequisites: list[str]
    related_concepts: list[str]

    class Config:
        from_attributes = True


class ConceptCreate(BaseModel):
    name: str
    subject: str
    grade: str
    description: Optional[str] = None
    formula: Optional[str] = None
    prerequisites: list[str] = []
    related_concepts: list[str] = []


@router.get("/concepts", response_model=list[ConceptOut])
async def get_concepts(
    grade: Optional[str] = Query(None),
    subject: Optional[str] = Query(None),
    limit: int = Query(50, le=200),
    db: AsyncSession = Depends(get_db),
):
    """List math concepts with optional filters."""
    conditions = []
    if grade:
        conditions.append(Concept.grade == grade)
    if subject:
        conditions.append(Concept.subject == subject)

    stmt = select(Concept)
    if conditions:
        stmt = stmt.where(and_(*conditions))
    stmt = stmt.limit(limit)

    result = await db.execute(stmt)
    concepts = result.scalars().all()
    return [
        ConceptOut(
            id=c.id,
            name=c.name,
            subject=c.subject,
            grade=c.grade,
            description=c.description,
            formula=c.formula,
            prerequisites=c.prerequisites or [],
            related_concepts=c.related_concepts or [],
        )
        for c in concepts
    ]


@router.get("/concepts/{concept_id}", response_model=ConceptOut)
async def get_concept(concept_id: str, db: AsyncSession = Depends(get_db)):
    """Get a specific concept by ID."""
    result = await db.execute(select(Concept).where(Concept.id == concept_id))
    concept = result.scalar_one_or_none()
    if not concept:
        raise HTTPException(status_code=404, detail="CONCEPT_NOT_FOUND")
    return ConceptOut(
        id=concept.id,
        name=concept.name,
        subject=concept.subject,
        grade=concept.grade,
        description=concept.description,
        formula=concept.formula,
        prerequisites=concept.prerequisites or [],
        related_concepts=concept.related_concepts or [],
    )


@router.post("/concepts", response_model=ConceptOut, status_code=201)
async def create_concept(body: ConceptCreate, db: AsyncSession = Depends(get_db)):
    """Create a new concept entry."""
    concept = Concept(
        name=body.name,
        subject=body.subject,
        grade=body.grade,
        description=body.description,
        formula=body.formula,
        prerequisites=body.prerequisites,
        related_concepts=body.related_concepts,
    )
    db.add(concept)
    await db.flush()
    return ConceptOut(
        id=concept.id,
        name=concept.name,
        subject=concept.subject,
        grade=concept.grade,
        description=concept.description,
        formula=concept.formula,
        prerequisites=concept.prerequisites or [],
        related_concepts=concept.related_concepts or [],
    )


@router.get("/concepts/{concept_id}/explanation")
async def get_concept_explanation(
    concept_id: str,
    grade: str = Query("middle_3"),
    db: AsyncSession = Depends(get_db),
):
    """Get a grade-appropriate concept explanation (AI-generated when API key is set)."""
    result = await db.execute(select(Concept).where(Concept.id == concept_id))
    concept = result.scalar_one_or_none()
    if not concept:
        raise HTTPException(status_code=404, detail="CONCEPT_NOT_FOUND")

    from app.core.config import settings

    if settings.OPENAI_API_KEY:
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            response = await client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "당신은 수학 교육 전문가입니다. 학생 수준에 맞춰 쉽게 설명하세요.",
                    },
                    {
                        "role": "user",
                        "content": (
                            f"학년: {grade}\n"
                            f"개념: {concept.name}\n"
                            f"기본 설명: {concept.description or ''}\n"
                            f"공식: {concept.formula or ''}\n\n"
                            f"이 개념을 {grade} 수준에 맞게 300자 이내로 쉽게 설명해주세요."
                        ),
                    },
                ],
                temperature=0.5,
                max_tokens=500,
            )
            explanation = response.choices[0].message.content
        except Exception:
            explanation = concept.description or "설명을 불러올 수 없습니다."
    else:
        explanation = concept.description or f"{concept.name}에 대한 설명입니다. (데모)"

    return {
        "concept_id": concept_id,
        "concept_name": concept.name,
        "grade": grade,
        "explanation": explanation,
        "formula": concept.formula,
    }
