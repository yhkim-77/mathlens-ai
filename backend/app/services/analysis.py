"""
AI Analysis Service — calls OpenAI GPT-4o to analyze math solutions.
Falls back to a rule-based mock when the API key is not configured.
"""
import json
import time
import logging
from typing import Optional

from app.core.config import settings

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """당신은 수학 교육 전문 AI 튜터입니다.
학생의 수학 풀이를 단계별로 분석하고, 오류 유형과 위치를 명확히 판별하세요.
반드시 아래 JSON 형식으로만 응답하세요.
{
  "is_correct": <true|false>,
  "recognized_latex": "<풀이 수식 LaTeX>",
  "steps": ["단계1 LaTeX", "단계2 LaTeX"],
  "error_steps": [
    {
      "step_order": <int>,
      "error_type": "<conceptual|procedural|computational|comprehension>",
      "error_subtype": "<세부 오류 유형>",
      "description": "<오류 설명>",
      "correct_expression": "<올바른 수식>"
    }
  ],
  "concept_understanding_summary": "<개념 이해도 요약>",
  "feedback_message": "<학생에게 전달할 피드백>",
  "concept_explanation": "<관련 개념 설명 (500자 이내)>",
  "recommended_concept_tags": ["태그1", "태그2"],
  "confidence": <0.0~1.0>
}"""


def _mock_analysis(problem_text: Optional[str], recognized_latex: str) -> dict:
    """Rule-based mock for when OpenAI API key is not set."""
    return {
        "is_correct": False,
        "recognized_latex": recognized_latex or "x = 1",
        "steps": [recognized_latex] if recognized_latex else ["x = 1"],
        "error_steps": [
            {
                "step_order": 1,
                "error_type": "computational",
                "error_subtype": "arithmetic_error",
                "description": "계산 과정에서 오류가 발생했습니다. (데모 응답)",
                "correct_expression": "x = 2",
            }
        ],
        "concept_understanding_summary": "기본 개념은 이해하고 있으나 계산 실수가 있습니다. (데모 응답)",
        "feedback_message": "계산 과정을 한 번 더 확인해보세요. (데모 응답)",
        "concept_explanation": "이 문제에서 사용된 개념을 다시 한번 살펴보겠습니다. (데모 응답)",
        "recommended_concept_tags": ["일차방정식"],
        "confidence": 0.75,
    }


async def analyze_solution(
    image_base64: str,
    problem_text: Optional[str],
    recognized_latex: str,
    student_grade: str = "middle_2",
    recent_error_types: Optional[list] = None,
) -> dict:
    """Analyze a math solution using GPT-4o (or mock if no API key)."""
    start_ms = int(time.time() * 1000)

    if not settings.OPENAI_API_KEY:
        logger.warning("OPENAI_API_KEY not set — using mock analysis")
        result = _mock_analysis(problem_text, recognized_latex)
        result["processing_time_ms"] = int(time.time() * 1000) - start_ms
        return result

    try:
        from openai import AsyncOpenAI

        client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

        user_content: list = [
            {
                "type": "text",
                "text": (
                    f"학습자 학년: {student_grade}\n"
                    f"최근 오답 유형: {recent_error_types or []}\n\n"
                    f"문제: {problem_text or '(문제 없음)'}\n\n"
                    f"인식된 풀이(LaTeX):\n{recognized_latex}"
                ),
            }
        ]

        if image_base64:
            user_content.append(
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{image_base64}"},
                }
            )

        response = await client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_content},
            ],
            temperature=0.2,
            max_tokens=1500,
            response_format={"type": "json_object"},
        )

        raw = response.choices[0].message.content
        result = json.loads(raw)
        result["processing_time_ms"] = int(time.time() * 1000) - start_ms
        return result

    except Exception as exc:
        logger.error("OpenAI analysis failed: %s", exc)
        result = _mock_analysis(problem_text, recognized_latex)
        result["processing_time_ms"] = int(time.time() * 1000) - start_ms
        return result


async def generate_similar_problem(
    concept_tags: list,
    difficulty: int,
    error_type: str,
    grade: str,
    source_problem_text: Optional[str] = None,
) -> dict:
    """Generate a similar math problem using GPT-4o."""
    if not settings.OPENAI_API_KEY:
        return {
            "title": f"유사 문제 ({grade}, 난이도 {difficulty})",
            "content_text": f"다음을 풀어라: $x + 1 = 2$ (데모 문제)",
            "answer_latex": "x = 1",
            "hint": "이항을 이용하세요.",
            "concept_tags": concept_tags,
            "difficulty": difficulty,
            "grade": grade,
        }

    try:
        from openai import AsyncOpenAI

        client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

        prompt = (
            f"학년: {grade}, 난이도: {difficulty}/5, 오류 유형: {error_type}\n"
            f"개념 태그: {', '.join(concept_tags)}\n"
            f"원본 문제: {source_problem_text or '없음'}\n\n"
            "위 조건에 맞는 새로운 수학 문제를 2022 개정 교육과정 범위 내에서 생성하세요.\n"
            "반드시 JSON 형식으로만 응답하세요:\n"
            '{"title": "...", "content_text": "...(LaTeX $...$ 포함)...", '
            '"answer_latex": "...", "hint": "...", "concept_tags": [...], '
            '"difficulty": int, "grade": "..."}'
        )

        response = await client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "당신은 수학 문제 출제 전문가입니다. JSON으로만 응답하세요.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=600,
            response_format={"type": "json_object"},
        )

        return json.loads(response.choices[0].message.content)

    except Exception as exc:
        logger.error("Problem generation failed: %s", exc)
        return {
            "title": f"유사 문제 ({grade})",
            "content_text": f"다음을 풀어라: $x + 1 = 2$",
            "answer_latex": "x = 1",
            "hint": "이항을 이용하세요.",
            "concept_tags": concept_tags,
            "difficulty": difficulty,
            "grade": grade,
        }
