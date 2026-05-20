from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


class LearningReport(BaseModel):
    user_id: str
    total_problems: int
    correct_rate: float
    weak_concepts: list[str]
    error_type_distribution: dict[str, int]
    study_streak: int           # 연속 학습일
    mastered_concepts: list[str]
    weekly_summary: list[dict]


class ConceptMastery(BaseModel):
    concept_id: str
    concept_name: str
    mastery_level: int          # 0~100
    last_practiced: str
    correct_count: int
    total_count: int


@router.get("/users/{user_id}/report", response_model=LearningReport)
async def get_learning_report(user_id: str, period: str = "week"):
    """
    사용자 학습 리포트 조회
    period: week / month / all
    """
    # TODO: DB에서 학습 이력 집계
    pass


@router.get("/users/{user_id}/mastery", response_model=list[ConceptMastery])
async def get_concept_mastery(user_id: str):
    """개념별 습득 현황 조회"""
    # TODO: DB에서 개념 습득 현황 조회
    pass


@router.get("/users/{user_id}/wrong-notes")
async def get_wrong_notes(user_id: str, limit: int = 50):
    """오답 노트 조회"""
    # TODO: 오답 이력 반환
    pass
