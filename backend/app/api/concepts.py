from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


class Concept(BaseModel):
    id: str
    name: str
    subject: str
    grade: str
    description: str
    formula: Optional[str] = None      # LaTeX 수식
    prerequisites: list[str]           # 선수 개념 ID 목록
    related_concepts: list[str]


@router.get("/concepts", response_model=list[Concept])
async def get_concepts(
    grade: Optional[str] = Query(None),
    subject: Optional[str] = Query(None)
):
    """개념 목록 조회"""
    # TODO: DB에서 개념 목록 반환
    return []


@router.get("/concepts/{concept_id}", response_model=Concept)
async def get_concept(concept_id: str):
    """특정 개념 상세 조회"""
    # TODO: DB에서 개념 조회
    pass


@router.get("/concepts/{concept_id}/explanation")
async def get_concept_explanation(concept_id: str, grade: str = "middle3"):
    """
    학년 수준에 맞는 개념 설명 반환 (LLM 생성)
    """
    # TODO: LLM으로 학년 맞춤 설명 생성
    pass
