from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Optional
import base64

router = APIRouter()


class AnalyzeRequest(BaseModel):
    image_base64: str          # 손글씨 풀이 이미지 (base64)
    problem_id: Optional[str] = None
    problem_text: Optional[str] = None
    user_id: str


class ErrorDetail(BaseModel):
    step: int                  # 오류 발생 단계
    error_type: str            # 개념오류 / 절차오류 / 계산실수 / 문제이해오류
    description: str           # 오류 설명
    correct_expression: str    # 올바른 수식


class AnalyzeResponse(BaseModel):
    is_correct: bool
    recognized_latex: str      # 인식된 수식 (LaTeX)
    steps: list[str]           # 분해된 풀이 단계
    errors: list[ErrorDetail]
    concept_understanding: str # 개념 이해도 요약
    feedback: str              # 맞춤형 피드백
    concept_explanation: str   # 개념 재설명
    similar_problem_id: str    # 유사 문제 ID


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_solution(request: AnalyzeRequest):
    """
    손글씨 수학 풀이를 분석하여 오답 원인 및 맞춤 피드백 반환
    """
    # TODO: HTR 엔진으로 손글씨 → LaTeX 변환
    # TODO: LLM으로 풀이 단계 분석 및 오류 분류
    # TODO: 맞춤형 피드백 생성
    # TODO: 유사 문제 생성 요청
    raise HTTPException(status_code=501, detail="구현 예정")


@router.post("/analyze/image")
async def analyze_image(
    file: UploadFile = File(...),
    user_id: str = "",
    problem_id: str = ""
):
    """
    이미지 파일로 직접 업로드하여 풀이 분석
    """
    contents = await file.read()
    image_base64 = base64.b64encode(contents).decode("utf-8")
    # TODO: analyze_solution 로직 호출
    raise HTTPException(status_code=501, detail="구현 예정")
