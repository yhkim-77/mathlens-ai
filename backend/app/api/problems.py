from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


class Problem(BaseModel):
    id: str
    title: str
    content: str
    subject: str       # 수학 과목 (대수, 기하, 미적분 등)
    grade: str         # 학년 (중1 ~ 고3)
    difficulty: int    # 난이도 1~5
    concept_tags: list[str]
    image_url: Optional[str] = None


class GenerateProblemRequest(BaseModel):
    concept_tags: list[str]   # 출제할 개념 태그
    difficulty: int           # 난이도
    error_type: str           # 오답 유형 기반 출제
    grade: str


@router.get("/problems", response_model=list[Problem])
async def get_problems(
    grade: Optional[str] = Query(None),
    subject: Optional[str] = Query(None),
    difficulty: Optional[int] = Query(None),
    concept_tag: Optional[str] = Query(None),
    limit: int = Query(20, le=100)
):
    """문제 목록 조회"""
    # TODO: DB에서 조건에 맞는 문제 조회
    return []


@router.get("/problems/{problem_id}", response_model=Problem)
async def get_problem(problem_id: str):
    """특정 문제 조회"""
    # TODO: DB에서 문제 조회
    pass


@router.post("/problems/generate", response_model=Problem)
async def generate_similar_problem(request: GenerateProblemRequest):
    """
    오답 유형 기반 유사 문제 자동 생성 (LLM 활용)
    """
    # TODO: LLM으로 유사 문제 생성
    pass
