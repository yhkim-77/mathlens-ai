# MathLens AI — 통합 제품 요구사항 문서 (PRD)

**문서 버전:** v3.0 (통합본)  
**작성일:** 2026년 5월 21일  
**문서 유형:** Product Requirements Document (PRD)  
**작성자:** MathLens AI 제품팀  
**상태:** 초안 (Draft)  

---

## 문서 변경 이력

| 버전 | 날짜 | 파일명 (구) | 주요 변경 내용 |
|------|------|-------------|----------------|
| v1.0 | 2026-05-21 | `PRD.md` | 최초 작성 — 제품 비전, 사용자 페르소나, 사용자 스토리, 기능 요구사항, 기술 아키텍처 결정사항, 화면 흐름, API 명세, 데이터 모델, 출시 기준, 성공 지표(KPI) 포함 |
| v1.5 | 2026-05-21 | `PRD_ProblemServing_PenRecognition.md` | 서브시스템 PRD 분리 — 백엔드 문제 출제 시스템(문제은행, LLM 생성, 추천 엔진), 펜 입력 캡처·전송, AI 인식 파이프라인에 대한 상세 기능 요구사항 별도 기술 |
| v2.0 | 2026-05-21 | `PRD_통합본.md` | **통합본**: 문제 출제·펜 입력·AI 인식 파이프라인 서브시스템 PRD를 메인 PRD에 통합. 오류 처리(11장), 테스트(12장), 배포(13장) 챕터 추가 |
| v3.0 | 2026-05-21 | `PRD_통합본.md` | 마일스톤 섹션(17장) 추가 (날짜·완료 기준·스프린트 계획 포함), React/React Native 기술 호환성 검토 섹션(18장) 추가. 이전 버전 파일 삭제 후 통합본으로 일원화 |

> **참고**: v1.0~v1.5 문서 파일은 이 통합본으로 대체되어 삭제되었습니다. 원본 내용은 위 변경 이력 및 Git 커밋 히스토리에서 확인할 수 있습니다.

---

## 목차

1. [제품 비전 및 목표](#1-제품-비전-및-목표)
2. [사용자 페르소나](#2-사용자-페르소나)
3. [사용자 스토리 및 핵심 시나리오](#3-사용자-스토리-및-핵심-시나리오)
4. [기능 요구사항](#4-기능-요구사항)
   - 4.1 [펜 입력 캔버스](#41-펜-입력-캔버스)
   - 4.2 [수식 인식 엔진 (MyScript iink + MathPix)](#42-수식-인식-엔진)
   - 4.3 [AI 풀이 분석 엔진](#43-ai-풀이-분석-엔진)
   - 4.4 [맞춤형 피드백 화면](#44-맞춤형-피드백-화면)
   - 4.5 [반복 학습 시스템](#45-반복-학습-시스템)
   - 4.6 [문제 입력 및 문제은행](#46-문제-입력-및-문제은행)
   - 4.7 [학습 리포트 및 대시보드](#47-학습-리포트-및-대시보드)
   - 4.8 [계정 및 인증](#48-계정-및-인증)
5. [비기능 요구사항](#5-비기능-요구사항)
6. [기술 아키텍처 결정사항](#6-기술-아키텍처-결정사항)
   - 6.6 [무료·오픈소스 모델 활용 방안](#66-무료오픈소스-모델-활용-방안-adr-006)
7. [화면 흐름 (User Flow)](#7-화면-흐름-user-flow)
8. [API 명세 (핵심)](#8-api-명세-핵심)
9. [데이터 모델](#9-데이터-모델)
10. [출시 기준 (Definition of Done)](#10-출시-기준-definition-of-done)
11. [오류 처리 및 예외 시나리오](#11-오류-처리-및-예외-시나리오)
12. [테스트 요구사항](#12-테스트-요구사항)
13. [배포 및 운영 요구사항](#13-배포-및-운영-요구사항)
14. [리스크 및 완화 방안](#14-리스크-및-완화-방안)
15. [성공 지표 (KPI)](#15-성공-지표-kpi)
16. [변경 이력](#16-변경-이력)
17. [마일스톤](#17-마일스톤)
18. [React / React Native 기술 호환성 검토](#18-react--react-native-기술-호환성-검토)

---

## 1. 제품 비전 및 목표

### 1.1 제품 비전

> "학생이 스마트 기기에 펜으로 수학 풀이를 쓰는 것만으로, AI가 어느 단계에서 무엇을 잘못 이해했는지 진단하고 완전 학습까지 이끄는 개인 수학 튜터"

### 1.2 제품 목표 (Phase 1 기준)

| 번호 | 목표 | 측정 지표 |
|------|------|-----------|
| G1 | 펜 입력 수식 인식 정확도 95% 달성 | iink 인식 결과 vs 정답 수식 정확도 |
| G2 | 오답 원인 분류 정확도 90% 달성 | AI 분류 결과 vs 전문 교사 레이블 일치율 |
| G3 | 풀이 제출 후 피드백까지 5초 이내 | P95 응답 시간 |
| G4 | 동일 유형 3회 이내 정답률 70% 이상 | 반복 학습 완료 후 성공률 |
| G5 | 30일 유지율(Retention) 40% 이상 | D30 Retention Rate |
| G6 | 전체 처리 파이프라인 10초 이내 완료 | P95 파이프라인 완료 시간 |

### 1.3 제품 범위 (In Scope / Out of Scope)

| 항목 | Phase 1 | Phase 2 | Phase 3 |
|------|---------|---------|---------|
| 펜 수식 인식 (iink SDK) | ✅ | ✅ | ✅ |
| AI 오답 분석 (GPT-4o) | ✅ | ✅ | ✅ |
| 유사 문제 자동 생성 | ✅ | ✅ | ✅ |
| 카메라 문제 인식 | ✅ | ✅ | ✅ |
| 문제 출제 백엔드 | ✅ | ✅ | ✅ |
| 학부모 대시보드 | ❌ | ✅ | ✅ |
| 교사 문제 출제 도구 | ❌ | ❌ | ✅ |
| 오프라인 AI 추론 | ❌ | ❌ | ✅ |
| 실시간 협업 | ❌ | ❌ | ✅ |

---

## 2. 사용자 페르소나

### 페르소나 1: 중학생 학습자 — 김민준 (14세)

| 항목 | 내용 |
|------|------|
| 상황 | 중학교 2학년, 수학 성적 중위권. 학원을 다니지만 풀이 과정에서 실수가 잦음 |
| 목표 | 어디서 틀리는지 빠르게 파악하고 싶음 |
| 불편함 | 문제를 틀려도 왜 틀렸는지 설명해주는 사람이 없음 |
| 기기 | iPad + Apple Pencil (부모님 선물) |
| 핵심 니즈 | 즉각적인 오답 피드백, 이해하기 쉬운 설명 |

### 페르소나 2: 고등학생 학습자 — 이서연 (17세)

| 항목 | 내용 |
|------|------|
| 상황 | 고등학교 2학년, 수능 준비 중. 미적분·확률통계 취약 |
| 목표 | 취약 단원 집중 보완 |
| 불편함 | 오답 노트를 직접 만들기 번거롭고, 비슷한 문제를 찾기 어려움 |
| 기기 | Samsung Galaxy Tab + S-Pen |
| 핵심 니즈 | 자동 오답 노트, 유사 문제 즉시 제공 |

### 페르소나 3: 학부모 — 박지현 (45세)

| 항목 | 내용 |
|------|------|
| 상황 | 자녀의 수학 학습 진도가 궁금하지만 직접 가르치기 어려움 |
| 목표 | 자녀가 어떤 개념을 어려워하는지 파악 |
| 불편함 | 학원 성적표만으로는 어디가 취약한지 알 수 없음 |
| 기기 | iPhone (모니터링 앱 사용) |
| 핵심 니즈 | 간단한 학습 리포트, 알림 |

---

## 3. 사용자 스토리 및 핵심 시나리오

### 3.1 핵심 학습 루프 시나리오

```
시나리오: 학생이 문제를 풀고 AI 피드백을 받아 재학습하는 흐름

1. 학생이 앱을 열고 문제를 선택 (문제은행 또는 카메라 촬영)
2. 풀이 화면에서 펜으로 풀이 과정을 작성
   → iink SDK가 실시간으로 수식을 LaTeX로 변환하여 미리보기 표시
3. "제출" 버튼 탭
4. 서버에 LaTeX + 원본 이미지 전송 (202 즉시 응답)
5. WebSocket으로 단계별 처리 상태 수신
6. GPT-4o가 오답 유형 분류 + 피드백 문장 생성 (3~5초)
7. 피드백 화면에서 틀린 단계 하이라이팅 + 개념 설명 카드 표시
8. "다시 풀기" 탭 → 같은 유형 다른 숫자의 문제 자동 생성
9. 연속 3회 정답 시 "해당 개념 습득 완료" 배지 표시
```

### 3.2 사용자 스토리 목록

#### 3.2.1 학습자

| ID | As a... | I want to... | So that... | 우선순위 |
|----|---------|-------------|------------|---------|
| US-01 | 학생 | 펜으로 수학 풀이를 쓰면 실시간으로 수식이 인식되는 것을 보고 싶다 | 인식 오류를 즉시 확인하고 수정할 수 있다 | P0 |
| US-02 | 학생 | 앱을 열었을 때 오늘 내 수준에 맞는 문제를 즉시 받아보고 싶다 | 별도 선택 없이 바로 학습을 시작할 수 있다 | P0 |
| US-03 | 학생 | 풀이를 제출하면 어느 단계에서 틀렸는지 정확히 알고 싶다 | 단순 정오가 아닌 원인을 파악할 수 있다 | P0 |
| US-04 | 학생 | 내 수준에 맞는 설명으로 틀린 개념을 다시 배우고 싶다 | 개념 오류를 스스로 교정할 수 있다 | P0 |
| US-05 | 학생 | 틀린 문제와 비슷한 유형의 문제를 바로 다시 풀고 싶다 | 같은 실수를 반복하지 않는지 확인할 수 있다 | P0 |
| US-06 | 학생 | 교재 문제를 카메라로 찍어 앱에 입력하고 싶다 | 별도로 문제를 입력하는 번거로움이 없다 | P0 |
| US-07 | 학생 | 인식된 수식이 틀렸다면 직접 수정할 수 있어야 한다 | 잘못 인식된 부분을 보정하고 정확히 분석받을 수 있다 | P1 |
| US-08 | 학생 | 내가 자주 틀리는 개념이 어떤 것인지 한눈에 보고 싶다 | 취약점을 집중 보완할 수 있다 | P1 |
| US-09 | 학생 | 이전에 풀었던 손글씨 답안을 다시 볼 수 있어야 한다 | 학습 이력을 확인하고 복습할 수 있다 | P2 |
| US-10 | 학생 | 인터넷이 없어도 캔버스가 부드럽게 동작해야 한다 | 장소에 구애받지 않고 공부할 수 있다 | P2 |

#### 3.2.2 교사 / 학부모

| ID | As a... | I want to... | So that... | 우선순위 |
|----|---------|-------------|------------|---------|
| US-11 | 학부모 | 자녀의 주간 학습 현황과 취약 개념을 요약해서 보고 싶다 | 학습 관리를 적극적으로 할 수 있다 | Should Have (Phase 2) |
| US-12 | 교사 | 학생이 제출한 손글씨 풀이 이미지를 확인할 수 있어야 한다 | 개별 학생 지도에 활용할 수 있다 | Should Have (Phase 2) |

---

## 4. 기능 요구사항

### 4.1 펜 입력 캔버스

#### FR-CANVAS-01: 스타일러스 및 터치 입력 지원

| 항목 | 내용 |
|------|------|
| 설명 | Apple Pencil (1/2세대), Samsung S-Pen, 일반 스타일러스, 손가락 터치 모두 지원 |
| iOS 구현 | PencilKit (PKCanvasView) — 필압·속도·방향 데이터 수집 |
| Android 구현 | Jetpack Compose Canvas + MotionEvent (ACTION_DOWN/MOVE/UP) |
| 필압 지원 | iOS: PKStroke.path의 pressure 값 활용 / Android: MotionEvent.getPressure() |
| 수락 기준 | 스타일러스로 쓴 획과 손가락 터치 획이 모두 캔버스에 자연스럽게 렌더링됨 |

#### FR-CANVAS-02: 도구 모음

| 도구 | 옵션 |
|------|------|
| 펜 | 굵기 3단계, 색상 5가지 (검정, 파랑, 빨강, 초록, 주황) |
| 형광펜 | 굵기 1단계, 반투명 |
| 지우개 | 획 단위 지우기, 점 단위 지우기 |
| 올가미 | 선택 영역 이동/삭제 |
| 실행 취소/재실행 | 최대 50단계 |
| 전체 지우기 | 확인 팝업 후 초기화 |

#### FR-CANVAS-03: 캔버스 뷰포트 조작

- 두 손가락 핀치: 확대/축소 (50% ~ 300%)
- 두 손가락 스크롤: 캔버스 이동
- Apple Pencil 더블 탭: 이전 도구 전환 (iOS)
- 줌 초기화 버튼 제공

#### FR-CANVAS-04: 성능 요구사항

- 렌더링 지연: **16ms 이하** (60 FPS 이상 유지)
- 필압 지원 스타일러스 사용 시 필압에 따른 선 굵기 변화 반영
- 팜 리젝션: 스타일러스 입력 감지 시 터치 입력 무시

#### FR-CANVAS-05: 자동 저장

- 스트로크 입력 중 30초마다 로컬 임시 저장 (`UserDefaults` / `Room DB`)
- 앱 재시작 시 미제출 풀이 복원 여부 사용자에게 안내

#### FR-CANVAS-06: 이미지 캡처 및 전처리

```
[캔버스 캡처]
    │
    ▼
[잉크 바운딩 박스 계산]  ← 스트로크 좌표 컬렉션에서 min/max 추출
    │
    ▼
[여백 추가 크롭]  ← 바운딩 박스 ±20px 패딩
    │
    ▼
[해상도 표준화]  ← 장변 1024px 기준 리사이징 (비율 유지)
    │
    ▼
[JPEG 압축 (품질 85%)]  ← 용량 2MB 초과 시 품질 자동 하향 조정
    │
    ▼
[Base64 인코딩]
```

---

### 4.2 수식 인식 엔진

> **핵심 기술 결정**: 실시간 수식 인식에 **MyScript iink SDK**를, 배치(이미지) 수식 인식 Fallback에 **MathPix OCR API**를 사용합니다.

#### FR-RECOG-01: MyScript iink SDK 실시간 인식

| 항목 | 내용 |
|------|------|
| 설명 | 학생이 획을 그을 때마다 iink SDK가 실시간으로 수식을 인식하여 LaTeX로 변환 |
| SDK 설정 | Math 모드 활성화, 출력 포맷: LaTeX |
| 미리보기 UI | 캔버스 우측 또는 상단에 인식된 수식을 KaTeX로 렌더링하여 실시간 표시 |
| 인식 지연 | 획 입력 후 200ms 이내 미리보기 업데이트 |
| 수정 UI | 인식 결과 탭 시 기호 선택 팝업 표시 (iink SDK 내장 correction UI 활용) |
| 수락 기준 | 중학교~고등학교 수준 수식 95% 이상 정확 인식 |

#### FR-RECOG-02: MathPix API Fallback

| 항목 | 내용 |
|------|------|
| 발동 조건 | iink SDK가 인식 실패(오류 코드 반환) 시, 또는 복잡도 높은 수식으로 분류될 때 |
| 구현 | 캔버스 이미지(PNG) → 백엔드 → MathPix `/v3/text` 호출 → LaTeX 반환 |
| 응답 시간 | 제출 후 3초 이내 LaTeX 결과 표시 |
| 오류 처리 | MathPix API도 실패 시, 원본 이미지를 GPT-4o Vision에 직접 전달하여 수식 해석 |

#### FR-RECOG-03: 인식 결과 수동 수정

| 항목 | 내용 |
|------|------|
| 설명 | 학생이 인식된 LaTeX 결과를 직접 수정할 수 있는 인터페이스 제공 |
| 구현 | 수정된 LaTeX → KaTeX 즉시 렌더링 미리보기 |
| 데이터 활용 | 수정 이력은 인식 품질 개선 데이터로 수집 (사용자 동의 하에) |

#### FR-RECOG-04: 한글/영문 주석 인식

| 항목 | 내용 |
|------|------|
| 설명 | 풀이 과정에 포함된 한글/영문 설명 텍스트 인식 |
| iOS 구현 | VNRecognizeTextRequest (Vision Framework), 한국어 모델 |
| Android 구현 | Google ML Kit Text Recognition v2 (Korean 지원) |
| 출력 | 인식된 텍스트를 LaTeX 내 `\text{}` 블록으로 삽입 |

---

### 4.3 AI 풀이 분석 엔진

> **핵심 기술 결정**: GPT-4o (멀티모달) 또는 Claude 3.5 Sonnet API를 사용합니다. 입력은 LaTeX 텍스트 + 원본 캔버스 이미지를 함께 전달합니다.

#### FR-AI-01: 비동기 처리 구조

```
[POST /submissions]
    │ 즉시 응답 (202 Accepted, submission_id 반환)
    │
    ▼
[Celery Task 생성 → Redis 큐]
    │
    ▼
[Worker 실행]
    ├── Step 1: 이미지 전처리 (OpenCV)
    ├── Step 2: HTR 실행 (iink / MathPix)
    ├── Step 3: LaTeX 후처리 (SymPy 검증)
    ├── Step 4: 분석 엔진 호출 (GPT-4o / Claude)
    └── Step 5: 결과 저장 + WebSocket 푸시
```

각 단계 완료 시 WebSocket으로 클라이언트에 상태 전송.

#### FR-AI-02: 타임아웃 처리

| 단계 | 타임아웃 | 타임아웃 시 처리 |
|------|----------|----------------|
| 이미지 전처리 | 5초 | 원본 이미지로 HTR 진행 |
| HTR API 호출 | 10초 | 재시도 1회 후 실패 처리 |
| LLM 분석 | 30초 | 재시도 1회 후 실패 처리 |

#### FR-AI-03: 풀이 단계 분해

| 항목 | 내용 |
|------|------|
| 설명 | 인식된 LaTeX 풀이를 논리적 단계로 자동 분리 |
| 구현 | 백엔드 파서 (정규식 + LLM 보완): 등호/부등호 기준 단계 분리 |
| 출력 형식 | `[{"step": 1, "latex": "2x + 3 = 7", "type": "equation"}, ...]` |

#### FR-AI-04: 오답 유형 분류

| 항목 | 내용 |
|------|------|
| 설명 | GPT-4o에게 문제 + 풀이 단계 + 원본 이미지를 전달하여 오답 원인 분류 |
| 분류 체계 | 개념 오류 / 절차 오류 / 계산 실수 / 문제 이해 오류 (4대 유형, 12 세부 항목) |
| 출력 형식 | `{"error_type": "conceptual", "error_subtype": "formula_confusion", "error_step": 2, "confidence": 0.92}` |
| 정확도 목표 | 전문 교사 레이블 대비 90% 일치 |

#### FR-AI-05: 피드백 문장 생성

| 항목 | 내용 |
|------|------|
| 설명 | 오류 유형 및 학년 수준에 맞는 한국어 개념 설명 생성 |
| 입력 | 오류 유형, 관련 개념 ID, 학습자 학년, 이전 오답 이력 |
| 출력 | 설명 텍스트 (500자 이내) + 관련 공식 LaTeX + 예제 풀이 LaTeX |
| 말투 | 학생이 이해하기 쉬운 구어체 (반말 설정 가능) |

#### FR-AI-06: LLM 입력 구성

```python
messages = [
    {
        "role": "system",
        "content": f"""
당신은 수학 교육 전문 AI 튜터입니다.
학습자 정보: {grade}, 최근 오답 유형: {recent_error_types}
풀이를 단계별로 분석하고, 오류 유형과 위치를 명확히 판별하세요.
"""
    },
    {
        "role": "user",
        "content": [
            {"type": "text", "text": f"문제: {problem_text}\n\n인식된 풀이(LaTeX):\n{latex_steps}"},
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_base64}"}}
        ]
    }
]
```

#### FR-AI-07: LLM 출력 스키마

```json
{
  "is_correct": false,
  "error_steps": [
    {
      "step_order": 2,
      "error_type": "procedural_error",
      "error_subtype": "sign_error",
      "description": "이항 시 부호가 반전되지 않았습니다.",
      "correct_expression": "(2x - 1)(x + 5) = 0"
    }
  ],
  "concept_understanding_summary": "이차방정식의 인수분해 접근은 올바르나, 이항 부호 처리 규칙이 불명확합니다.",
  "feedback_message": "이항할 때 부호를 바꾸는 이유를 다시 확인해 보세요.",
  "concept_explanation": "...",
  "recommended_concept_tags": ["이차방정식", "이항"]
}
```

#### FR-AI-08: LaTeX 후처리 및 정답 판별

```python
from sympy.parsing.latex import parse_latex
from sympy import simplify

def is_mathematically_equivalent(student_latex: str, correct_latex: str) -> bool:
    try:
        student_expr = parse_latex(student_latex)
        correct_expr = parse_latex(correct_latex)
        diff = simplify(student_expr - correct_expr)
        return diff == 0
    except Exception:
        return None  # 판별 불가 → LLM에 위임
```

#### FR-AI-09: 유사 문제 생성

| 항목 | 내용 |
|------|------|
| 설명 | 오답 문제와 동일 개념·유형이지만 숫자/조건이 다른 문제 자동 생성 |
| 구현 | GPT-4o + 수학 문제 템플릿 엔진 |
| 교육과정 준수 | 2022 개정 교육과정 범위 내로 제한 (프롬프트 규칙 + 후처리 검증) |
| 검증 | 생성된 문제를 수식 파서로 유효성 검사 후 DB 저장 |

---

### 4.4 맞춤형 피드백 화면

#### FR-FEEDBACK-01: 오류 위치 하이라이팅

| 항목 | 내용 |
|------|------|
| 설명 | 틀린 단계를 원본 캔버스 이미지 위에 오버레이로 표시 |
| 구현 | AI가 반환한 `error_step` 기반으로 해당 수식 영역 빨간 테두리 표시 |
| 입력 | 바운딩 박스 좌표 (iink SDK 또는 MathPix API 반환값 활용) |

#### FR-FEEDBACK-02: 개념 설명 카드

- 오류 유형 배지 (색상 코딩: 개념 오류=빨강, 절차 오류=주황, 계산 실수=노랑, 문제 이해=보라)
- AI 생성 설명 텍스트
- 관련 공식 KaTeX 렌더링
- 핵심 예제 2개 (접이식 펼침)
- TTS 버튼 (한국어 음성 읽기, AVSpeechSynthesizer / Android TextToSpeech 활용)

#### FR-FEEDBACK-03: 정석 풀이 제시

- 올바른 풀이 단계를 순차적으로 애니메이션으로 표시 (단계별 페이드인)
- 각 단계에 설명 툴팁 옵션

#### FR-FEEDBACK-04: 다음 행동 버튼

| 버튼 | 동작 |
|------|------|
| 다시 풀기 | 동일 문제 캔버스 초기화 |
| 유사 문제 | AI 생성 유사 문제로 이동 |
| 개념 더 보기 | 개념 상세 화면으로 이동 |
| 넘어가기 | 다음 문제로 이동 |

---

### 4.5 반복 학습 시스템

#### FR-REPEAT-01: 완전 학습 판별

- 동일 개념 유형 연속 3회 정답 → 해당 개념 "습득 완료" 처리
- 습득 완료 시 배지 애니메이션 표시

#### FR-REPEAT-02: 간격 반복 복습 스케줄

| 복습 간격 | 기준 |
|-----------|------|
| 1일 후 | 첫 번째 습득 후 |
| 3일 후 | 두 번째 복습 성공 후 |
| 7일 후 | 세 번째 복습 성공 후 |
| 14일, 30일... | 에빙하우스 망각 곡선 기반 지수적 간격 증가 |

#### FR-REPEAT-03: 오답 노트 자동 생성

- 틀린 문제 자동 저장 (문제 이미지 + 오류 유형 + AI 설명 포함)
- 오답 노트 필터: 날짜별, 오류 유형별, 개념별
- PDF/이미지 내보내기

---

### 4.6 문제 입력 및 문제은행

#### FR-PROBLEM-01: 카메라 촬영 입력

| 항목 | 내용 |
|------|------|
| 설명 | 교재/시험지를 카메라로 촬영하여 문제 인식 |
| 구현 | 촬영 이미지 → MathPix API `/v3/text` → 문제 LaTeX 추출 |
| 자르기 가이드 | 문제 영역 자동 감지 및 크롭 안내 |
| 수락 기준 | 표준 교재 수준 인쇄체 문제 90% 이상 인식 |

#### FR-PROBLEM-02: 앱 내 문제은행

- 과목 / 단원 / 난이도 (하/중/상) 필터
- 2022 개정 교육과정 중·고등 수학 전 범위 커버
- 즐겨찾기, 최근 푼 문제

#### FR-PROBLEM-03: 직접 입력 (수식 에디터)

- 가상 수학 키보드 (분수, 루트, 적분 기호 버튼 포함)
- LaTeX 직접 입력 모드 (고급 사용자용)

#### FR-PROBLEM-04: 개인화 문제 추천

추천 엔진 입력 데이터 활용:

| 입력 데이터 | 활용 방식 |
|-------------|-----------|
| 사용자 학년 | 학년 필터 적용 |
| 최근 오답 개념 태그 (최근 30일) | 오답 개념 우선 출제 (가중치 70%) |
| 개념별 정답률 | 정답률 낮은 개념 우선 |
| 직전 연속 정답 횟수 | 난이도 자동 상향 (연속 3회 정답 시 +1 난이도) |
| 당일 이미 출제된 문제 ID 목록 | 중복 제외 |
| 취약/강점 개념 비율 | 취약:강점 = 7:3 비율 유지 |

#### FR-PROBLEM-05: 문제은행 관리

- 문제 상태: `draft` → `review` → `active` → `archived`
- `active` 상태 문제만 학습자에게 출제
- 문제 수정 시 이전 버전 보존 (이미 제출 이력이 있는 문제의 원본 보호)
- 각 문제에 `concept_tags` 및 `error_type_tags` 부착 필수

---

### 4.7 학습 리포트 및 대시보드

#### FR-REPORT-01: 학생 대시보드 (홈 화면)

- 오늘의 학습 목표 (문제 수) 및 달성 현황
- 최근 7일 연속 학습일 (스트릭)
- 취약 개념 TOP 3
- 추천 복습 문제 카드 (간격 반복 스케줄 기반)

#### FR-REPORT-02: 주간/월간 리포트

- 풀이 문제 수, 정답률, 학습 시간 추이 그래프
- 오답 유형 분포 파이 차트
- 개념별 습득 현황 히트맵

#### FR-REPORT-03: 개념 맵 (Phase 2)

- 교육과정 개념 간 선후관계 시각화
- 습득/미습득/취약 개념 색상 구분

---

### 4.8 계정 및 인증

#### FR-AUTH-01: 소셜 로그인

| 제공자 | 플랫폼 |
|--------|--------|
| Apple Login | iOS 필수 |
| Google Login | iOS + Android |
| Kakao Login | iOS + Android |

#### FR-AUTH-02: 프로필 설정

- 학년 설정 (중1 ~ 고3 / 재수생 / 기타)
- 일일 학습 목표 (문제 수)
- 알림 설정

#### FR-AUTH-03: 학부모 연동 (Phase 2)

- QR 코드 또는 초대 코드로 자녀 계정 연동
- 학부모 계정: 조회 전용 (학습 리포트, 오답 유형)

---

## 5. 비기능 요구사항

### 5.1 성능

| 지표 | 요구 수준 |
|------|-----------|
| 수식 인식 미리보기 지연 | 획 입력 후 200ms 이내 (iink SDK, 온디바이스) |
| 풀이 제출 접수 응답 (202) | P99 기준 500ms 이내 |
| HTR 처리 시간 (서버 기준) | P95 기준 4,000ms 이내 |
| 전체 파이프라인 완료 | P95 기준 10,000ms 이내 |
| 풀이 제출 후 AI 분석 완료 | P95 기준 5초 이내 |
| 문제 추천 API 응답 시간 | P99 기준 1,000ms 이내 |
| 앱 콜드 스타트 | 3초 이내 (iOS/Android) |
| API 서버 응답 시간 | P99 기준 2초 이내 (AI 분석 제외) |
| 캔버스 렌더링 프레임 속도 | ≥ 60 FPS (≤ 16ms/frame) |
| 동시 접속자 | 1,000 CCU 이상 처리 |
| 동시 처리 제출 수 | 500건/분 이상 |

### 5.2 신뢰성

- 서비스 가용성: 99.5% 이상 (월 기준)
- AI API 다운 시: MathPix Fallback → GPT-4o Fallback → 수동 확인 모드 순서로 대체
- 로컬 캐시: 마지막 10개 문제 및 피드백 결과 로컬 저장 (오프라인 열람)
- Celery Worker 장애 시 작업 재시도: 최대 3회 (exponential backoff)
- 다중 AZ 배포 (AWS Multi-AZ RDS, Redis Cluster)

### 5.3 보안

- 전송 암호화: TLS 1.3
- 인증: JWT (Access Token 1시간, Refresh Token 30일)
- 미성년자 개인정보: 수집 최소화, 법정대리인 동의 프로세스
- 풀이 이미지: 분석 후 30일 경과 시 자동 삭제 (설정 가능)
- MathPix API 호출 시 사용자 식별 정보 포함 금지
- S3 이미지: Pre-signed URL (유효기간 1시간) 또는 서버 프록시 전달
- SQL Injection 방지: ORM(SQLAlchemy) 파라미터 바인딩 사용
- Rate Limiting: 사용자당 제출 60건/시간, IP당 추천 API 100건/분
- OWASP Mobile Top 10 기준 보안 설계

### 5.4 접근성

- 다크모드 지원
- 글자 크기: 시스템 Dynamic Type (iOS) / 텍스트 크기 조절 (Android) 연동
- 고대비 모드 지원
- VoiceOver / TalkBack 핵심 UI 지원

### 5.5 현지화

- 1차 출시: 한국어 전용
- 2차 확장 고려: 영어, 일본어 (데이터 구조 i18n 설계)

### 5.6 모니터링 및 관측성

- 각 파이프라인 단계별 처리 시간 메트릭 수집 (Prometheus)
- HTR 신뢰도 분포 대시보드 (Grafana)
- 오류율 알림: 에러율 > 1% 시 Slack/PagerDuty 알림
- 분산 트레이싱: `submission_id`를 Correlation ID로 모든 로그에 포함

---

## 6. 기술 아키텍처 결정사항

### 6.1 수식 인식 엔진 결정 (ADR-001)

| 결정 | MyScript iink SDK (실시간) + MathPix API (Fallback) |
|------|-----|
| 이유 | iink SDK: 온디바이스, 실시간, 오프라인 지원, 업계 최고 정확도. MathPix: 이미지 기반 고정밀 백업. 자체 ML 훈련은 Phase 1 비현실적 |
| 대안 검토 | Google ML Kit (수식 미지원), Tesseract (손글씨 정확도 부족), GPT-4o 단독 (복잡 수식 정확도 부족) |
| 리뷰 시점 | Phase 3 온디바이스 전환 시 재검토 |

### 6.2 AI 분석 엔진 결정 (ADR-002)

| 결정 | OpenAI GPT-4o (멀티모달) 우선, Anthropic Claude 3.5 백업 |
|------|-----|
| 이유 | LaTeX + 이미지 동시 처리, 한국어 수학 설명 품질, API 안정성 |
| 무료 대안 | DeepSeek-Math 7B, Qwen2.5-Math 7B 자체 호스팅으로 대체 가능 (섹션 6.7 참조) |

### 6.3 수식 렌더링 결정 (ADR-003)

| 결정 | KaTeX (WebView 또는 네이티브 바인딩) |
|------|-----|
| 이유 | MathJax 대비 렌더링 속도 10배 이상 빠름, 모바일 최적화 |
| iOS | WKWebView 내 KaTeX JS 렌더링 또는 iosMath 라이브러리 |
| Android | WebView 내 KaTeX JS 렌더링 |

### 6.4 백엔드 프레임워크 결정 (ADR-004)

| 결정 | Python FastAPI |
|------|-----|
| 이유 | 비동기 처리 (asyncio), 자동 OpenAPI 문서, AI/ML 생태계 연동 용이 |

### 6.5 비동기 작업 처리 결정 (ADR-005)

| 결정 | Celery + Redis |
|------|-----|
| 이유 | AI 파이프라인(HTR + LLM)의 긴 처리 시간을 비동기 처리, 실패 시 재시도 지원 |
| 클라이언트 통신 | WebSocket으로 단계별 진행 상태 실시간 전달 |

### 6.6 무료·오픈소스 모델 활용 방안 (ADR-006)

상용 API 없이 무료로 사용 가능한 오픈소스 모델을 활용하면 인터넷 의존도를 낮추고 자체 인프라에서 운영할 수 있다.

#### 수식 인식 (HTR) — 무료 옵션

| 모델 | 라이선스 | 특징 | 호스팅 |
|------|----------|------|--------|
| **Pix2tex (LaTeX-OCR)** | MIT | 수식 이미지 → LaTeX 직접 변환, MathPix 무료 대체 | Python 서버, Docker |
| **TrOCR** (Microsoft) | MIT | Hugging Face 모델 허브 제공, 손글씨 범용 | Hugging Face Inference API, 자체 서버 |
| **nougat** (Meta) | CC-BY-NC 4.0 | 논문·수식 이미지 특화 LaTeX 변환 | 자체 서버 (GPU 권장) |
| **Google ML Kit** | 무료 (SDK) | 온디바이스, 일반 텍스트·숫자 인식 | 온디바이스 |
| **Apple Vision** | 무료 (내장) | iOS 온디바이스, 일반 텍스트 인식 | 온디바이스 (iOS 전용) |

#### AI 분석 LLM — 무료 옵션

| 모델 | 라이선스 | 특징 | 호스팅 |
|------|----------|------|--------|
| **DeepSeek-Math 7B** | MIT | 수학 특화, 한국어 지원 | Ollama, vLLM, Hugging Face |
| **Qwen2.5-Math 7B** (Alibaba) | Apache 2.0 | 수학 특화, 한국어 지원 강함 | Ollama, Hugging Face |
| **Llama 3.1 8B / 70B** (Meta) | Llama 3.1 무료 라이선스 | 범용 고성능, 한국어 중상 품질 | Ollama, vLLM |
| **Gemma 2 2B / 9B** (Google) | Apache 2.0 | 경량 고성능, Hugging Face 제공 | Ollama, Hugging Face Inference API |
| **Phi-3 Mini** (Microsoft) | MIT | 3.8B 초경량, 수학 영어 강점 | Ollama, 온디바이스(ONNX/CoreML) |
| **Mistral 7B** | Apache 2.0 | 범용 고성능, 지시 추종 우수 | Ollama, vLLM |

#### 자체 호스팅 도구

| 도구 | 설명 |
|------|------|
| **Ollama** | 서버에서 LLM 원클릭 실행, REST API 제공 (`/api/generate`) |
| **vLLM** | 고성능 GPU 추론 서버, OpenAI 호환 API |
| **llama.cpp** | CPU 기반 4-bit 양자화 추론, 저사양 서버 가능 |
| **Hugging Face Inference API** | 무료 티어 제공 (속도 제한 있음), 프로토타입에 적합 |

> **Phase별 전환 전략**: Phase 1은 GPT-4o(주) + DeepSeek-Math(fallback), Phase 2는 Qwen2.5-Math 또는 Llama 3.1 70B 자체 호스팅 비중 확대, Phase 3은 Phi-3 Mini 또는 Gemma 2B 온디바이스 추론으로 완전 오프라인·무료 구조 달성 가능.

---

## 7. 화면 흐름 (User Flow)

### 7.1 핵심 학습 플로우

```
[앱 실행]
    │
    ▼
[홈 대시보드]
    │
    ├── 오늘의 추천 문제 탭
    │       ↓
    │   [문제 선택 화면]
    │       ↓
    │   [풀이 화면] ← 핵심 화면
    │     · PencilKit / iink 캔버스
    │     · 실시간 수식 미리보기 (LaTeX → KaTeX 렌더링)
    │     · 도구 모음
    │       ↓ (제출)
    │   [분석 중 로딩] (WebSocket 진행 상태 표시)
    │       ↓
    │   [인식 결과 확인] ← iink 인식 LaTeX 확인·수정
    │       ↓
    │   [AI 피드백 화면]
    │     · 오류 하이라이팅
    │     · 개념 설명 카드
    │     · TTS 재생
    │       ↓
    │   [다시 풀기 / 유사 문제 / 넘어가기]
    │
    ├── 카메라 아이콘 탭
    │       ↓
    │   [카메라 촬영] → MathPix 인식 → [문제 확인 화면] → [풀이 화면]
    │
    └── 학습 리포트 탭
            ↓
        [주간 그래프 / 오답 분포 / 개념 맵]
```

---

## 8. API 명세 (핵심)

### 8.1 문제 추천 API

```
GET /api/v1/problems/recommend
Authorization: Bearer {JWT}
```

**요청 파라미터:**

| 파라미터 | 타입 | 필수 | 설명 |
|----------|------|------|------|
| `user_id` | string | ✅ | 학습자 UUID |
| `grade` | string | ✅ | 학년 코드 (예: `middle_1`, `high_2`) |
| `subject` | string | ❌ | 과목 필터 |
| `difficulty_min` | int | ❌ | 최소 난이도 (1~5) |
| `difficulty_max` | int | ❌ | 최대 난이도 (1~5) |
| `concept_tag` | string | ❌ | 특정 개념 태그 강제 |
| `limit` | int | ❌ | 반환 수 (기본 1, 최대 10) |

**응답 (200 OK):**

```json
{
  "problems": [
    {
      "problem_id": "uuid",
      "title": "이차방정식 풀기",
      "content_text": "다음 이차방정식을 풀어라. $2x^2 + 3x - 5 = 0$",
      "content_image_url": null,
      "subject": "algebra",
      "grade": "middle_3",
      "difficulty": 3,
      "concept_tags": ["이차방정식", "인수분해"],
      "estimated_solve_time_min": 5
    }
  ],
  "recommendation_meta": {
    "reason": "최근 이차방정식 오답 패턴 기반 추천",
    "algorithm_version": "1.2"
  }
}
```

---

### 8.2 유사 문제 생성 API

```
POST /api/v1/problems/generate
Authorization: Bearer {JWT}
```

**요청:**

```json
{
  "source_problem_id": "prob_12345",
  "error_type": "procedural",
  "concept_id": "concept_linear_equation",
  "difficulty": "medium",
  "student_grade": "middle_2"
}
```

**응답:**

```json
{
  "problem_id": "prob_gen_11111",
  "problem_latex": "3x - 5 = 10",
  "answer_latex": "x = 5",
  "hint": "이항할 때 부호 변화에 주의하세요.",
  "concept_ids": ["concept_linear_equation"]
}
```

---

### 8.3 풀이 제출 API

```
POST /api/v1/submissions
Authorization: Bearer {JWT}
Content-Type: application/json
```

**요청 바디:**

```json
{
  "user_id": "string",
  "problem_id": "string",
  "session_id": "string",
  "image_base64": "string (Base64)",
  "image_mime_type": "image/png",
  "stroke_metadata": {
    "stroke_count": 42,
    "total_duration_ms": 35000,
    "canvas_size": { "width": 1080, "height": 1440 },
    "input_type": "stylus"
  },
  "client_timestamp": "2026-05-21T10:00:00+09:00",
  "device_info": {
    "platform": "ios",
    "os_version": "17.4",
    "app_version": "1.0.0"
  }
}
```

**응답 (202 Accepted):**

```json
{
  "submission_id": "uuid",
  "status": "received",
  "websocket_url": "wss://api.mathlens.ai/ws/v1/submissions/{submission_id}",
  "estimated_processing_time_ms": 5000
}
```

---

### 8.4 처리 상태 WebSocket 메시지

| 단계 | 메시지 |
|------|--------|
| 이미지 수신 | `{"stage": "received", "ts": "..."}` |
| 전처리 완료 | `{"stage": "preprocessed", "ts": "..."}` |
| HTR 완료 | `{"stage": "htr_done", "latex_preview": "...", "confidence": 0.96, "ts": "..."}` |
| 분석 완료 | `{"stage": "analysis_done", "result_id": "uuid", "is_correct": true, "ts": "..."}` |
| 오류 발생 | `{"stage": "error", "error_code": "HTR_TIMEOUT", "message": "...", "ts": "..."}` |

---

### 8.5 AI 풀이 분석 API

```
POST /api/v1/solutions/analyze
Authorization: Bearer {JWT}
```

**요청:**

```json
{
  "problem_id": "prob_12345",
  "canvas_image_base64": "<Base64 PNG>",
  "recognized_latex": "2x + 3 = 7 \\\\ 2x = 4 \\\\ x = 3",
  "student_grade": "middle_2"
}
```

**응답:**

```json
{
  "analysis_id": "ana_67890",
  "is_correct": false,
  "error_step": 2,
  "error_type": "procedural",
  "error_subtype": "sign_error",
  "error_description": "이항할 때 부호가 바뀌지 않았어요.",
  "feedback_text": "등식의 성질을 다시 확인해봐요. 좌변의 +3을 우변으로 이항할 때는 -3이 됩니다.",
  "related_concept_id": "concept_linear_equation",
  "correct_solution_latex": "2x + 3 = 7 \\\\ 2x = 7 - 3 \\\\ 2x = 4 \\\\ x = 2",
  "confidence": 0.94,
  "processing_time_ms": 3120
}
```

---

### 8.6 인식 결과 조회 API

```
GET /api/v1/results/{submission_id}
Authorization: Bearer {JWT}
```

**응답 (200 OK):**

```json
{
  "submission_id": "uuid",
  "problem_id": "uuid",
  "user_id": "uuid",
  "submitted_at": "ISO8601",
  "htr_result": {
    "raw_latex": "2x^{2} + 3x - 5 = 0",
    "steps": [
      { "order": 1, "latex": "2x^{2} + 3x - 5 = 0", "confidence": 0.97 }
    ],
    "overall_confidence": 0.95
  },
  "analysis_result": { "..." },
  "image_url": "https://...",
  "status": "completed"
}
```

---

### 8.7 학습 리포트 API

```
GET /api/v1/users/{user_id}/report
Authorization: Bearer {JWT}
```

**응답 (요약):**

```json
{
  "user_id": "usr_abc",
  "period": "2026-05-01 ~ 2026-05-21",
  "total_problems": 87,
  "correct_rate": 0.71,
  "error_distribution": {
    "conceptual": 0.40,
    "procedural": 0.35,
    "computational": 0.20,
    "comprehension": 0.05
  },
  "weak_concepts": ["이차방정식", "인수분해", "삼각함수"],
  "mastered_concepts": ["일차방정식", "연립방정식"],
  "streak_days": 7
}
```

---

## 9. 데이터 모델

### 9.1 주요 테이블 (PostgreSQL)

```sql
-- 사용자
users (
  id UUID PRIMARY KEY,
  email VARCHAR UNIQUE,
  grade VARCHAR,              -- middle_1 ~ high_3, reexaminee
  created_at TIMESTAMP,
  last_active_at TIMESTAMP
)

-- 문제
problems (
  id UUID PRIMARY KEY,
  title VARCHAR,
  content_text TEXT NOT NULL, -- LaTeX 포함
  content_image_key TEXT,     -- S3 key
  answer_latex TEXT,
  solution_steps JSONB,
  subject VARCHAR,            -- algebra, geometry, calculus, statistics
  grade VARCHAR,
  difficulty SMALLINT,        -- 1(하) ~ 5(상)
  concept_tags TEXT[],
  error_type_tags TEXT[],
  curriculum_code VARCHAR,
  source VARCHAR,             -- bank | llm_generated | textbook
  status VARCHAR,             -- draft | review | active | archived
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)

-- 제출
submissions (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users,
  problem_id UUID REFERENCES problems,
  session_id UUID,
  image_s3_key TEXT,
  stroke_metadata JSONB,
  device_info JSONB,
  status VARCHAR,             -- received | processing | completed | failed
  submitted_at TIMESTAMP,
  processed_at TIMESTAMP
)

-- AI 인식 결과
recognition_results (
  id UUID PRIMARY KEY,
  submission_id UUID REFERENCES submissions UNIQUE,
  htr_raw_latex TEXT,
  htr_steps JSONB,
  htr_confidence FLOAT,
  is_correct BOOLEAN,
  error_type VARCHAR,         -- conceptual|procedural|computational|comprehension
  error_subtype VARCHAR,
  error_step SMALLINT,
  error_steps JSONB,
  feedback_text TEXT,
  correct_solution_latex TEXT,
  concept_tags_inferred TEXT[],
  llm_model_version VARCHAR,  -- gpt-4o | claude-3.5-sonnet
  prompt_template_id UUID,
  confidence FLOAT,
  created_at TIMESTAMP
)

-- 개념 습득 현황
concept_mastery (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users,
  concept_id UUID,
  status VARCHAR,             -- learning | mastered | review_due
  consecutive_correct SMALLINT,
  next_review_at TIMESTAMP,
  updated_at TIMESTAMP
)

-- 사용자 문제 이력
user_problem_history (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users,
  problem_id UUID REFERENCES problems,
  submission_id UUID REFERENCES submissions,
  is_correct BOOLEAN,
  error_type VARCHAR,
  solved_at TIMESTAMP
)
```

### 9.2 인덱스 전략

| 테이블 | 인덱스 컬럼 | 이유 |
|--------|------------|------|
| `problems` | `(grade, subject, difficulty, status)` | 추천 필터 쿼리 |
| `problems` | `concept_tags` GIN 인덱스 | 태그 기반 검색 |
| `submissions` | `(user_id, submitted_at)` | 사용자별 이력 조회 |
| `user_problem_history` | `(user_id, problem_id)` | 중복 출제 방지 조회 |
| `user_problem_history` | `(user_id, error_type, solved_at)` | 오답 유형 통계 |
| `concept_mastery` | `(user_id, status, next_review_at)` | 복습 스케줄 조회 |

---

## 10. 출시 기준 (Definition of Done)

### Phase 1 MVP 출시 기준

#### 기능 완성도
- [ ] 펜 입력 캔버스: PencilKit (iOS) + Android Canvas 구현 완료
- [ ] iink SDK 수식 인식: 중·고등 수식 95% 이상 정확도 테스트 통과
- [ ] MathPix API Fallback 연동 완료
- [ ] GPT-4o 오답 분석: 5대 오류 유형 분류 정확도 90% 이상 (테스트셋 100문항 기준)
- [ ] 유사 문제 자동 생성 기능 동작 확인
- [ ] 카메라 촬영 문제 인식 기능 동작 확인
- [ ] 인식 결과 확인·수정 UI 구현 완료
- [ ] 학습 리포트 기본 화면 구현 완료
- [ ] 소셜 로그인 3종 (Apple, Google, Kakao) 정상 동작
- [ ] 문제 추천 API 및 문제은행 (중학교 전 단원) 구축 완료
- [ ] WebSocket 기반 처리 상태 실시간 전달 동작 확인

#### 품질 기준
- [ ] 크래시율: < 0.1% (Firebase Crashlytics 기준)
- [ ] 앱 스토어 심사 가이드라인 준수 (특히 아동 개인정보 처리)
- [ ] 성능: 풀이 제출 → AI 분석 P95 < 5초
- [ ] 성능: 전체 파이프라인 P95 < 10초
- [ ] 보안: OWASP Mobile Top 10 취약점 점검 완료

#### 콘텐츠 기준
- [ ] 문제은행: 중학교 1~3학년 각 단원별 최소 50문제 이상
- [ ] 개념 설명 DB: 중학교 수학 전 단원 커버

---

## 11. 오류 처리 및 예외 시나리오

### 11.1 오류 코드 정의

| 오류 코드 | HTTP 상태 | 설명 | 클라이언트 대응 |
|-----------|-----------|------|----------------|
| `SUBMISSION_IMAGE_TOO_LARGE` | 400 | 이미지 2MB 초과 | 압축 후 재전송 안내 |
| `SUBMISSION_EMPTY_CANVAS` | 400 | 스트로크 없는 빈 캔버스 | "풀이를 작성해 주세요" 안내 |
| `HTR_LOW_CONFIDENCE` | 200 | HTR 신뢰도 0.8 미만 | 인식 결과 확인 및 수정 UI 표시 |
| `HTR_TIMEOUT` | 200 | HTR API 타임아웃 | 재처리 또는 수동 입력 옵션 제공 |
| `HTR_UNSUPPORTED_SYMBOL` | 200 | 미지원 수식 기호 | 해당 구간 수동 입력 요청 |
| `PROBLEM_NOT_FOUND` | 404 | 문제 ID 없음 | 홈으로 돌아가기 |
| `QUOTA_EXCEEDED` | 429 | 제출 횟수 초과 | 재시도 가능 시간 안내 |
| `AI_SERVICE_UNAVAILABLE` | 503 | LLM/HTR 서비스 장애 | 잠시 후 재시도 안내 + 풀이 보존 |

### 11.2 네트워크 불안정 시나리오

- 제출 중 연결 끊김: 로컬 임시 저장 후 재연결 시 자동 재전송
- WebSocket 연결 실패: 폴링 방식으로 자동 전환 (`GET /submissions/{id}/status` 3초 간격)
- 타임아웃 후 결과 미수신: 5분 후 상태 재조회 허용
- 재전송 정책: 지수 백오프 (1초 → 2초 → 4초, 최대 3회)

### 11.3 HTR 인식 실패 시 폴백

```
HTR 인식 실패 또는 신뢰도 낮음
        │
        ▼
[1차 폴백] 원본 이미지를 멀티모달 LLM에 직접 전달
        │ 실패 시
        ▼
[2차 폴백] 사용자에게 LaTeX 직접 입력 UI 표시
        │ 사용자 입력 후
        ▼
[제출 재개]
```

---

## 12. 테스트 요구사항

### 12.1 단위 테스트

| 모듈 | 테스트 항목 |
|------|------------|
| 문제 추천 엔진 | 오답 기반 가중치 계산, 난이도 스캐폴딩 로직, 중복 제외 |
| LLM 문제 생성 | 생성 검증 로직 (LaTeX 파싱 성공 여부) |
| 이미지 전처리 | 이진화, 기울기 보정 결과 검증 (샘플 이미지 비교) |
| LaTeX 동치 판별 | SymPy 기반 판별 정확도 (100개 샘플 쌍) |
| HTR 결과 파서 | 단계 분리 로직 |
| 수식 렌더링 | KaTeX 렌더링 정상 출력 확인 |

### 12.2 통합 테스트

- 문제 추천 → 클라이언트 수신 → 캔버스 렌더링 → 제출 → HTR → 결과 반환 전체 흐름
- 다양한 필기체 스타일 샘플 (표준/비표준/어린 학생/성인) 각 50개 이상
- Fallback 시나리오: iink 실패 → MathPix → GPT-4o Vision 순서 동작 확인

### 12.3 성능 테스트

- 동시 500건 제출 처리 (k6 또는 Locust 시나리오)
- HTR API 응답 시간 p50/p95/p99 측정
- 메모리 누수 테스트 (24시간 연속 부하)

### 12.4 HTR 정확도 테스트 데이터셋

| 유형 | 샘플 수 | 기준 |
|------|---------|------|
| 중학 수준 수식 (표준 필기) | 200 | CER ≤ 5% |
| 고등 수준 수식 (표준 필기) | 200 | CER ≤ 5% |
| 비표준 필기 (성인) | 100 | CER ≤ 15% |
| 혼합 (수식 + 한글 텍스트) | 100 | 단어 정확도 ≥ 90% |

---

## 13. 배포 및 운영 요구사항

### 13.1 환경 구성

| 환경 | 목적 |
|------|------|
| `development` | 로컬 개발 (Docker Compose) |
| `staging` | QA 및 성능 테스트 |
| `production` | 실서비스 (AWS Multi-AZ) |

### 13.2 CI/CD

- GitHub Actions: PR 생성 시 단위 테스트 자동 실행
- Staging 배포: `main` 브랜치 머지 시 자동
- Production 배포: 수동 승인 후 블루-그린 배포

### 13.3 인프라 구성

| 구성 | 기술 |
|------|------|
| 클라우드 | AWS (ECS + RDS + S3 + CloudFront) |
| 데이터베이스 | PostgreSQL Multi-AZ RDS |
| 캐시/큐 | Redis Cluster |
| 이미지 스토리지 | AWS S3 (AES-256 암호화) |
| CDN | AWS CloudFront |
| 컨테이너 | Docker + ECS Auto Scaling |
| 모니터링 | Grafana + Prometheus, Sentry |

---

## 14. 리스크 및 완화 방안

| 리스크 | 가능성 | 영향도 | 완화 방안 |
|--------|--------|--------|-----------|
| 수식 인식 정확도 미달 (95% 미만) | 중 | 높음 | 인식 결과 수동 수정 UI 필수 제공, 사용자 교정 데이터 누적 |
| 미성년자 개인정보 규제 이슈 | 낮음 | 매우 높음 | 법무팀 사전 검토, 개인정보 수집 최소화 설계 |
| OpenAI API 다운타임 | 낮음 | 높음 | Claude API 또는 오픈소스 LLM(DeepSeek-Math, Qwen2.5-Math) Fallback 구성, 서킷 브레이커 패턴 적용 |
| 앱스토어 심사 거절 | 낮음 | 중 | Apple/Google 가이드라인 사전 검토, 심사 2주 여유 |
| HTR API 응답 지연 급증 | 중 | 중 | Fallback 체인 구성(iink → Pix2tex → MathPix), 사용자에게 진행 상태 투명하게 표시 |

---

## 15. 성공 지표 (KPI)

### 15.1 제품 성능 지표

| KPI | 목표 (Phase 1 출시 3개월 후) |
|-----|------|
| 수식 인식 정확도 | ≥ 95% |
| AI 오답 분류 정확도 | ≥ 90% |
| 풀이 분석 P95 응답 시간 | ≤ 5초 |
| 전체 파이프라인 P95 완료 시간 | ≤ 10초 |
| 앱 크래시율 | ≤ 0.1% |
| 일일 활성 사용자 중 문제 풀이 완료율 | ≥ 70% |

### 15.2 비즈니스 지표

| KPI | 목표 (출시 3개월 후) |
|-----|------|
| MAU | 10,000 이상 |
| D7 Retention | ≥ 50% |
| D30 Retention | ≥ 30% |
| 일 평균 풀이 제출 수 | MAU × 2 이상 |
| 유료 전환율 (프리미엄) | ≥ 5% |

### 15.3 학습 효과 지표

| KPI | 목표 |
|-----|------|
| 동일 유형 3회 이내 정답률 | ≥ 70% |
| 개념 습득 완료 후 2주 복습 정답률 | ≥ 80% |
| 사용자 만족도 (NPS) | ≥ 40 |

---

## 16. 변경 이력

| 버전 | 날짜 | 변경 내용 | 작성자 |
|------|------|-----------|--------|
| v1.0 | 2026-05-21 | 최초 작성 — RFP v2.0 기반 PRD 전면 작성 | MathLens AI 제품팀 |
| v2.0 | 2026-05-21 | 통합본 — 문제 출제·펜 입력·AI 인식 파이프라인 서브시스템 통합. 오류 처리(11), 테스트(12), 배포(13) 챕터 추가 | MathLens AI 제품팀 |
| v3.0 | 2026-05-21 | 마일스톤 섹션(17장) 추가, React/React Native 기술 호환성 검토 섹션(18장) 추가. 이전 버전 파일(PRD.md, PRD_ProblemServing_PenRecognition.md) 삭제 후 통합본 일원화 | MathLens AI 제품팀 |

---

## 17. 마일스톤

> 프로젝트 시작일을 D+0(기산일)로 산정합니다. 각 마일스톤은 이전 마일스톤 완료를 전제로 하며, 미충족 시 이해관계자 협의 후 일정 조정.

### 17.1 마일스톤 목록

| 마일스톤 | 기간 (기산일 기준) | 완료 기준 | 담당 |
|----------|------|-----------|------|
| **M0 — 프로젝트 킥오프** | D+0 | 팀 구성 완료, 개발 환경(GitHub, Docker, CI/CD) 셋업 완료 | PM |
| **M1 — 설계 완료 (Design Freeze)** | D+60 | DB 스키마 확정, API 명세 초안 승인, iink SDK PoC 성공 (수식 5종 인식 확인), 시스템 설계서 이해관계자 승인 | 기술 리드 |
| **M2 — 문제 출제 API 완료** | D+90 | `GET /problems/recommend` P95 ≤ 300ms, LLM 문제 생성 API 정상 응답 확인, 중학 1학년 전 단원 문제은행 단원별 최소 50문항 등록 | 백엔드 팀 |
| **M3 — 펜 입력 캔버스 + 이미지 전송 완료** | D+120 | iOS(PencilKit)/Android(Canvas) 펜 입력 → 서버 이미지 수신 확인, 60 FPS 이상 캔버스 렌더링, 스트로크 → 이미지 변환 및 S3 업로드 정상 동작 | 클라이언트 팀 |
| **M4 — HTR 파이프라인 완료** | D+150 | iink SDK 실시간 인식 + MathPix Fallback 파이프라인 동작, 샘플 100문항 수식 인식 정확도 ≥ 95%, LaTeX 출력 파싱 성공률 ≥ 98% | AI/HTR 팀 |
| **M5 — AI 분석 엔진 통합 완료** | D+180 | GPT-4o 오답 5대 유형 분류 정확도 ≥ 90% (100문항 테스트셋), WebSocket 단계별 상태 전달 동작, 전체 파이프라인 P95 ≤ 10초, SymPy 동치 판별 정확도 ≥ 99% | AI 팀 |
| **M6 — Phase 1 기능 완성** | D+195 | 출시 기준(Section 10) 기능 완성도 체크리스트 100% 충족, 소셜 로그인 3종 정상 동작, 학습 리포트 화면 구현 완료 | 전체 팀 |
| **M7 — 알파 테스트 완료** | D+210 | 내부 테스터 20명 이상 참여, 크리티컬/블로킹 버그 0건, 크래시율 < 0.1%, HTR 정확도 재측정 기준 충족 | QA 팀 |
| **M8 — 베타 테스트 완료** | D+270 | 실사용자 100명 이상 베타 참여, D7 Retention ≥ 40%, NPS ≥ 30, 인식 오류 패턴 개선 반영 완료, 성능 P95 기준 충족 | 전체 팀 |
| **M9 — Phase 1 출시 (MVP)** | D+300 | 앱스토어/플레이스토어 심사 통과, OWASP Mobile Top 10 보안 점검 완료, 아동 개인정보 처리 법무 검토 완료, 출시 기준(Section 10) 품질 기준 전체 충족 | PM + 전체 팀 |
| **M10 — Phase 2 완료** | D+450 | 학부모/교사 대시보드, 고등 수학 전 범위, 개념 맵 시각화, 푸시 알림 기능 출시 | 전체 팀 |
| **M11 — Phase 3 완료** | D+630 | 온디바이스 AI 추론(CoreML/TFLite), 실시간 협업 풀이, 교사 맞춤 출제 도구 출시 | 전체 팀 |

### 17.2 스프린트 계획 (Phase 1 상세, 2주 단위)

| Sprint | 기간 (기산일 기준) | 주요 목표 | 완료 기준 |
|--------|------|-----------|-----------|
| Sprint 0 | D+0~D+14 | 환경 구성, 기술 검증 (iink PoC, DB 설계) | Docker Compose 로컬 환경 구동, iink SDK 수식 3종 인식 확인 |
| Sprint 1 | D+14~D+28 | 백엔드 기반 구축 (FastAPI, PostgreSQL, Redis, JWT 인증) | `/health`, `/auth/login` API 정상 응답 |
| Sprint 2 | D+28~D+42 | 문제은행 DB 구축, 문제 추천 API (`GET /problems/recommend`) | 중학 1학년 1단원 50문항 등록, 추천 API P95 ≤ 300ms |
| Sprint 3 | D+42~D+56 | LLM 문제 생성 API, 소셜 로그인 (Apple, Google, Kakao) | 문제 생성 API LaTeX 검증 통과율 ≥ 95%, 로그인 3종 동작 |
| Sprint 4 | D+56~D+70 | 모바일 캔버스 UI (iOS PencilKit + Android Canvas), 이미지 업로드 | 60 FPS 캔버스, S3 업로드 성공 |
| Sprint 5 | D+70~D+84 | iink SDK 통합 (네이티브 모듈 브리지), 실시간 인식 결과 미리보기 | iink SDK 중등 수식 10종 인식 성공 |
| Sprint 6 | D+84~D+98 | MathPix Fallback 파이프라인, Celery 비동기 큐 | Fallback 시나리오 자동 전환 동작 확인 |
| Sprint 7 | D+98~D+112 | GPT-4o 오답 분석 통합, WebSocket 상태 전달 | 오답 분류 정확도 ≥ 85% (50문항 샘플 기준) |
| Sprint 8 | D+112~D+126 | 피드백 UI (오류 하이라이팅, 개념 설명 카드), 유사 문제 재출제 | 피드백 UI 시연 가능 |
| Sprint 9 | D+126~D+140 | 학습 리포트, 인식 결과 수정 UI, TTS | 리포트 기본 화면 구현 완료 |
| Sprint 10 | D+140~D+154 | 성능 최적화 (Redis 캐싱, 이미지 압축), 오류 처리 안정화 | 전체 파이프라인 P95 ≤ 10초 |
| Sprint 11 | D+154~D+168 | 보안 점검 (OWASP), 크래시율 측정, 알파 준비 | 크래시율 < 0.1%, 보안 취약점 0건 (High/Critical) |

### 17.3 Phase별 핵심 기능 범위

| 기능 | Phase 1 (MVP) | Phase 2 | Phase 3 |
|------|:---:|:---:|:---:|
| 펜 입력 캔버스 (iink SDK) | ✅ | ✅ | ✅ |
| MathPix Fallback 인식 | ✅ | ✅ | ✅ |
| AI 오답 분석 (GPT-4o) | ✅ (5대 유형) | ✅ (전체 유형) | ✅ |
| 유사 문제 재출제 | ✅ | ✅ | ✅ |
| 소셜 로그인 3종 | ✅ | ✅ | ✅ |
| 학습 리포트 (기본) | ✅ | ✅ | ✅ |
| 학부모/교사 대시보드 | ❌ | ✅ | ✅ |
| 개념 맵 시각화 | ❌ | ✅ | ✅ |
| 고등 수학 전 범위 | ❌ | ✅ | ✅ |
| 오프라인 모드 (iink) | ❌ | ❌ | ✅ |
| 온디바이스 AI (CoreML/TFLite) | ❌ | ❌ | ✅ |
| 실시간 협업 풀이 | ❌ | ❌ | ✅ |
| 교사 맞춤 출제 도구 | ❌ | ❌ | ✅ |

---

## 18. React / React Native 기술 호환성 검토

> **검토 목적**: 본 PRD에 명시된 기능 요구사항 및 기술 결정사항이 React(웹) 및 React Native(모바일 크로스플랫폼) 환경에서 구현 가능한지 검토합니다.  
> **범례**: ✅ 완전 호환 | ⚠️ 부분 호환 (대안 필요) | ❌ 미호환 (대체 기술 사용 필수)

### 18.1 핵심 기능별 React Native 호환성

| 기능 요구사항 | 현재 기술 결정 | React Native 호환성 | 구현 방안 |
|------|------|------|-----------|
| 펜 입력 캔버스 (FR-CANVAS) | PencilKit (iOS) + Android Canvas API | ⚠️ 직접 미지원 | `@shopify/react-native-skia` (React Native 새 아키텍처 기반, 60FPS 달성 가능) + 필요 시 커스텀 네이티브 모듈 |
| 실시간 수식 인식 (FR-HTR-01) | MyScript iink SDK (네이티브) | ⚠️ 공식 RN 패키지 없음 | **방안 A**: 커스텀 네이티브 모듈로 iOS Swift/Android Kotlin iink SDK 브리징 (권장, 추가 공수 ~3주) **방안 B**: `react-native-webview` + `@myscript/iink-js` 웹 SDK (성능 제한 있음) |
| 이미지 기반 수식 인식 (MathPix Fallback) | MathPix OCR REST API | ✅ 완전 호환 | React Native에서 `fetch`로 직접 REST API 호출 가능 |
| 수식 렌더링 (KaTeX) | KaTeX via WebView / iosMath | ✅ 완전 호환 | `react-native-webview` + KaTeX JS, 또는 `react-native-math-view` 라이브러리 사용 |
| iosMath (iOS 네이티브 렌더링) | iosMath 라이브러리 | ❌ React Native 미지원 | `react-native-math-view` 또는 KaTeX via WebView로 완전 대체 가능 |
| WebSocket 실시간 통신 | WebSocket (네이티브) | ✅ 완전 호환 | React Native 런타임 내장 `WebSocket` API 그대로 사용 |
| 카메라 촬영 (문제 스캔) | AVFoundation / CameraX | ✅ 완전 호환 | `react-native-vision-camera` 또는 `expo-camera` |
| 소셜 로그인 — Apple | ASAuthorizationController | ✅ 완전 호환 | `@invertase/react-native-apple-authentication` |
| 소셜 로그인 — Google | Google Sign-In SDK | ✅ 완전 호환 | `@react-native-google-signin/google-signin` |
| 소셜 로그인 — Kakao | Kakao SDK | ⚠️ 비공식 지원 | `react-native-kakao-login` (커뮤니티 유지관리) 또는 OAuth WebView 방식 |
| 푸시 알림 (Phase 2) | APNs / FCM | ✅ 완전 호환 | `@react-native-firebase/messaging` |
| 크래시 모니터링 | Firebase Crashlytics | ✅ 완전 호환 | `@react-native-firebase/crashlytics` |
| 오류 트래킹 | Sentry | ✅ 완전 호환 | `@sentry/react-native` |
| 온디바이스 AI — CoreML (Phase 3) | CoreML (iOS 전용) | ⚠️ 직접 미지원 | `react-native-fast-tflite` + TFLite 크로스플랫폼 모델 사용 (iOS에서 CoreML 백엔드 활용 가능) |
| 온디바이스 AI — TFLite (Phase 3) | TFLite (Android) | ✅ 완전 호환 | `react-native-fast-tflite` 공식 지원 |
| 실행 취소/재실행 (50단계) | 네이티브 Undo 스택 | ✅ 구현 가능 | React 상태 관리로 직접 구현 (Redux/Zustand undo history 패턴) |

### 18.2 백엔드 기술 호환성

백엔드는 REST API / WebSocket으로만 통신하므로 클라이언트 기술과 완전히 독립적입니다.

| 기술 결정 | React Native 호환성 | 비고 |
|------|------|------|
| ADR-001: MyScript iink SDK + MathPix (서버 측 처리) | ✅ 완전 호환 | 서버 변경 없음 |
| ADR-002: OpenAI GPT-4o API | ✅ 완전 호환 | 서버 변경 없음 |
| ADR-003: KaTeX 수식 렌더링 | ✅ 완전 호환 | 클라이언트에서 WebView 방식 사용 |
| ADR-004: Python FastAPI 백엔드 | ✅ 완전 호환 | 서버 변경 없음 |
| ADR-005: Celery + Redis 비동기 처리 | ✅ 완전 호환 | 서버 변경 없음 |

### 18.3 React(웹) 호환성 — 관리자/학부모/교사 포털

| 기능 | React(웹) 호환성 | 구현 방안 |
|------|------|-----------|
| 수식 렌더링 (KaTeX) | ✅ 완전 호환 | `react-katex` 또는 KaTeX JS 직접 사용 |
| 펜 입력 캔버스 (웹) | ✅ 완전 호환 | `@myscript/iink-js` React용 공식 지원 (웹에서 iink 캔버스 완전 구현 가능) |
| WebSocket 통신 | ✅ 완전 호환 | 브라우저 내장 `WebSocket` API, React에서 직접 사용 |
| 학습 리포트 차트 | ✅ 완전 호환 | `recharts`, `chart.js`, `victory` 등 React 생태계 풍부 |
| 소셜 로그인 | ✅ 완전 호환 | `@react-oauth/google`, Kakao JS SDK, Apple Sign In JS |
| 카메라 촬영 | ✅ 완전 호환 | `react-webcam` 또는 MediaDevices Web API |

### 18.4 주요 이슈 및 PRD 차원의 권고사항

#### 이슈 1: iink SDK React Native 브리징 — M1에서 PoC 필수 ⚠️

FR-HTR-01 (실시간 수식 인식)은 MyScript iink SDK에 의존하며, 공식 React Native 패키지가 없습니다.  
**PRD 요구사항**: M1(설계 완료, D+60) 단계에서 iink SDK 네이티브 모듈 브리지 PoC를 반드시 검증해야 하며, 검증 실패 시 WebView 방식으로 전환하여 일정을 즉시 조정합니다.

#### 이슈 2: 펜 캔버스 60 FPS — 신 아키텍처 필수 ⚠️

FR-CANVAS 요구사항(16ms/frame 이하)을 React Native에서 달성하려면 React Native 새 아키텍처(Fabric 렌더러 + JSI)와 `@shopify/react-native-skia` v1.0 이상이 필수입니다. 구버전 React Native(Bridge 기반)에서는 달성이 어렵습니다.  
**PRD 요구사항**: React Native 0.73 이상 + 새 아키텍처 활성화를 프로젝트 설정 단계(D+0~D+14)에서 확정합니다.

#### 이슈 3: 소셜 로그인 Kakao — 안정성 검토 필요 ⚠️

Kakao 소셜 로그인의 React Native 라이브러리는 비공식 커뮤니티 패키지입니다.  
**PRD 요구사항**: Kakao 로그인 미지원 시 OAuth 2.0 WebView 방식(카카오 공식 웹 인증 페이지)으로 대체하며, 이 경우에도 US-08(소셜 로그인) 요구사항을 충족합니다.

### 18.5 React / React Native 채택 시 추가 공수 요약

| 항목 | 추가 공수 | 비고 |
|------|-----------|------|
| iink SDK 네이티브 모듈 브리지 개발 | 2~3주 | iOS + Android 각각 개발 필요 |
| React Native 새 아키텍처 환경 구성 | 0.5주 | 프로젝트 초기 한 번만 |
| `@shopify/react-native-skia` 캔버스 구현 | 1~2주 | PencilKit 대비 추가 구현 |
| Kakao 로그인 검증 또는 대체 구현 | 0.5주 | WebView 방식은 즉시 구현 가능 |
| **합계** | **약 4~6주** | Phase 1 일정에 반영 필요 |

> **결론**: React Native 환경에서 본 PRD의 모든 핵심 기능을 구현하는 것은 가능합니다. 단, **iink SDK 브리징**, **Skia 캔버스 성능 최적화**, **새 아키텍처 적용**에 약 4~6주의 추가 공수가 필요하며, 이를 Phase 1 스프린트 계획에 반드시 반영해야 합니다.

---

*본 문서는 내부 참고용입니다.*

*© 2026 MathLens AI Project. All rights reserved.*
