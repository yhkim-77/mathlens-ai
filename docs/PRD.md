# MathLens AI — 제품 요구사항 명세서 (PRD)

**문서 버전:** v1.0  
**작성일:** 2026년 5월 21일  
**문서 유형:** Product Requirements Document (PRD)  
**담당:** MathLens AI Product Team  

---

## 목차

1. [제품 개요](#1-제품-개요)
2. [사용자 스토리 및 시나리오](#2-사용자-스토리-및-시나리오)
3. [백엔드–모바일 문제 전달 설계](#3-백엔드모바일-문제-전달-설계)
4. [펜 입력 정답 전송 설계 (AI 인가 후 서버 전달)](#4-펜-입력-정답-전송-설계-ai-인가-후-서버-전달)
5. [문제 풀이 과정 점검 파이프라인](#5-문제-풀이-과정-점검-파이프라인)
6. [개념 부족 추론 및 맞춤 질문/설명 엔진](#6-개념-부족-추론-및-맞춤-질문설명-엔진)
7. [데이터 모델](#7-데이터-모델)
8. [API 명세](#8-api-명세)
9. [비기능 요구사항](#9-비기능-요구사항)
10. [보안 및 개인정보 보호](#10-보안-및-개인정보-보호)
11. [수락 기준 (Acceptance Criteria)](#11-수락-기준-acceptance-criteria)

---

## 1. 제품 개요

### 1.1 제품 목적

MathLens AI는 학습자가 스마트 기기 화면 위에 펜 또는 손가락으로 수학 풀이를 작성하면, 온디바이스 AI가 1차 인식 및 인가(Authentication)를 수행하고, 백엔드 서버의 멀티모달 LLM이 풀이 과정 전체를 심층 분석하여 **어느 개념이 부족한지를 추론**하고 맞춤형 개념 설명 및 질문을 제공하는 교육용 모바일 애플리케이션이다.

### 1.2 핵심 가치 제안

| 가치 | 설명 |
|------|------|
| 실시간 펜 입력 인식 | 펜 스트로크를 온디바이스에서 즉시 처리, 지연 없는 UX |
| AI 인가 후 정답 전송 | 클라이언트가 1차 인식 결과를 검증한 뒤 서버에 전달, 네트워크 효율 극대화 |
| 풀이 과정 단계별 점검 | 정답 여부가 아닌 **풀이 경로**의 수학적 타당성 검증 |
| 개념 부족 추론 | 오류 패턴 분석 → 부족한 선수 개념 식별 → 우선 학습 개념 추천 |
| 맞춤 대화형 설명 | 소크라테스식 질문으로 학습자 스스로 개념을 발견하도록 유도 |

### 1.3 용어 정의

| 용어 | 정의 |
|------|------|
| 온디바이스 AI (On-device AI) | 모바일 기기 내부에서 실행되는 경량 추론 모델 (Core ML / TFLite) |
| AI 인가 (AI Authentication) | 온디바이스 AI가 펜 입력을 수식으로 변환하고 그 결과의 신뢰도를 검증하는 단계 |
| HTR | Handwritten Text Recognition — 손글씨를 디지털 텍스트/수식으로 변환 |
| LaTeX | 수학 수식을 구조적으로 표현하는 조판 언어 |
| 개념 지식 그래프 | 수학 개념 간 선수 학습 관계를 그래프로 모델링한 구조 |
| 마스터리 (Mastery) | 동일 유형 연속 3회 정답으로 판정되는 개념 습득 완료 상태 |
| 소크라테스 모드 | 정답을 직접 알려주지 않고 질문을 통해 학습자 사고를 유도하는 AI 대화 방식 |

---

## 2. 사용자 스토리 및 시나리오

### 2.1 핵심 사용자 여정 (Happy Path)

```
학생 "지수"(고등학교 2학년) 시나리오

1. 앱 실행 → 오늘의 추천 문제 수신 (서버 → 모바일)
2. 이차함수 최댓값 문제 선택
3. 펜으로 풀이 작성 시작
4. [온디바이스 AI] 필기 실시간 인식 → LaTeX 변환 → 신뢰도 검증
5. "제출" 버튼 클릭
6. [서버 전송] 인식된 LaTeX + 원본 스트로크 이미지 → 백엔드
7. [서버 분석] 풀이 단계 파서 → LLM 오류 분류 → 개념 부족 추론
8. 결과 수신: "꼭짓점 공식을 x좌표에만 적용하고 y값 대입을 빠뜨렸습니다"
9. AI 튜터: "이차함수 f(x)=a(x-p)²+q에서 꼭짓점의 y좌표는 무엇인가요?"
10. 지수가 답변 → AI가 정오 확인 → 개념 설명 + 유사 문제 제시
```

### 2.2 사용자 스토리

| ID | 역할 | 원하는 것 | 이유 |
|----|------|-----------|------|
| US-01 | 학생 | 수학 문제를 앱에서 펜으로 풀고 싶다 | 종이와 동일한 필기 경험 제공 |
| US-02 | 학생 | 틀린 이유를 구체적으로 알고 싶다 | 단순 오답 표시가 아닌 근본 원인 파악 |
| US-03 | 학생 | 내가 모르는 개념을 AI가 질문으로 알려줬으면 한다 | 스스로 생각하며 개념 체득 |
| US-04 | 학생 | 비슷한 문제를 반복 연습하고 싶다 | 약점 개념 완전 학습 |
| US-05 | 학부모 | 자녀의 취약 개념 현황을 보고 싶다 | 학습 지원 방향 파악 |
| US-06 | 교사 | 학생 오답 유형 통계를 보고 싶다 | 수업 내용 조정 |

---

## 3. 백엔드–모바일 문제 전달 설계

### 3.1 문제 전달 흐름 개요

```
┌──────────────────────────────────────────────────────┐
│                  모바일 클라이언트                      │
│                                                      │
│  [홈 화면 진입]                                       │
│       │                                              │
│       ▼                                              │
│  GET /api/v1/problems/today                          │
│  (JWT Bearer Token)                                  │
└──────────────────────────────────────────────────────┘
              │  HTTPS/REST
              ▼
┌──────────────────────────────────────────────────────┐
│               백엔드 API Gateway                       │
│                                                      │
│  1. JWT 검증                                         │
│  2. 사용자 학습 이력 조회 (Redis 캐시 우선)            │
│  3. 개념 숙달도 기반 문제 추천 알고리즘 실행           │
│  4. 문제 JSON 직렬화 (문제 + 메타데이터)              │
└──────────────────────────────────────────────────────┘
              │  JSON Response
              ▼
┌──────────────────────────────────────────────────────┐
│               모바일 클라이언트 (수신)                  │
│                                                      │
│  1. 문제 데이터 로컬 캐시 저장 (오프라인 대비)          │
│  2. 수식 렌더링 (LaTeX → 화면 표시)                   │
│  3. 펜 입력 캔버스 활성화                             │
└──────────────────────────────────────────────────────┘
```

### 3.2 문제 데이터 구조 (Problem Schema)

```json
{
  "problem_id": "prob_20260521_001",
  "version": 3,
  "metadata": {
    "grade": "high_2",
    "subject": "수학I",
    "unit": "이차함수",
    "topic": "이차함수의 최댓값·최솟값",
    "difficulty": 3,
    "estimated_time_sec": 180,
    "curriculum_code": "10수학-2-1-3"
  },
  "content": {
    "statement_latex": "이차함수 $f(x) = -2x^2 + 8x - 3$ 의 최댓값을 구하시오.",
    "statement_text": "이차함수 f(x) = -2x² + 8x - 3 의 최댓값을 구하시오.",
    "hints": [
      "이차함수를 완전제곱식으로 변환해 보세요.",
      "꼭짓점의 좌표를 구하면 최댓값을 알 수 있습니다."
    ],
    "figures": [],
    "answer": {
      "value": "5",
      "answer_latex": "5",
      "solution_steps": [
        "f(x) = -2(x^2 - 4x) - 3",
        "f(x) = -2(x-2)^2 + 8 - 3",
        "f(x) = -2(x-2)^2 + 5",
        "꼭짓점 (2, 5), a < 0이므로 최댓값 = 5"
      ]
    }
  },
  "concepts_required": ["완전제곱식", "이차함수의 꼭짓점", "최댓값·최솟값"],
  "prerequisite_concepts": ["인수분해", "이차함수의 그래프"],
  "expires_at": null
}
```

### 3.3 문제 전달 프로토콜 상세

#### 3.3.1 초기 문제 로딩 (REST)

| 항목 | 내용 |
|------|------|
| 프로토콜 | HTTPS REST |
| 엔드포인트 | `GET /api/v1/problems/today` |
| 인증 | `Authorization: Bearer <JWT>` |
| 응답 형식 | JSON, `Content-Type: application/json` |
| 캐시 전략 | `Cache-Control: max-age=3600` (1시간) |
| 응답 크기 | 단일 문제 ~2KB, 목록(10개) ~20KB |

#### 3.3.2 실시간 문제 스트리밍 (WebSocket — Phase 2)

```
ws://api.mathlens.ai/ws/v1/session/{session_id}

연결 시퀀스:
Client → Server: { "type": "session_init", "token": "<JWT>", "device_info": {...} }
Server → Client: { "type": "session_ready", "session_id": "...", "heartbeat_interval": 30 }

문제 전달:
Server → Client: {
  "type": "problem_push",
  "problem": { ...Problem Schema... },
  "reason": "adaptive_recommendation"
}

상태 동기화 (30초마다):
Client → Server: { "type": "heartbeat", "canvas_state": "idle|writing|submitted" }
```

#### 3.3.3 오프라인 지원

- 앱 실행 시 최대 **10개 문제**를 로컬 SQLite에 선캐시
- 네트워크 단절 시 캐시된 문제로 학습 지속
- 재연결 시 오프라인 풀이 결과를 큐에 저장하여 일괄 서버 전송

---

## 4. 펜 입력 정답 전송 설계 (AI 인가 후 서버 전달)

### 4.1 전체 흐름

```
┌──────────────────────────────────────────────────────────────┐
│                    모바일 클라이언트                           │
│                                                              │
│  [1] 펜 스트로크 수집                                         │
│      ├─ 좌표 (x, y), 필압, 타임스탬프 → stroke buffer        │
│      └─ 실시간 잉크 렌더링 (PencilKit / Android Ink API)     │
│                                                              │
│  [2] 온디바이스 AI 인가 (On-device HTR)                       │
│      ├─ 경량 수식 인식 모델 (Core ML / TFLite)               │
│      ├─ LaTeX 변환 + 신뢰도 점수(confidence) 산출            │
│      └─ confidence ≥ 0.85 → 인가 완료                       │
│          confidence < 0.85 → 사용자에게 재확인 요청           │
│                                                              │
│  [3] 사용자 "제출" 버튼 클릭                                  │
│      └─ Submission Payload 구성                              │
│                                                              │
│  [4] HTTPS POST → 백엔드                                     │
└──────────────────────────────────────────────────────────────┘
                    │
                    ▼ HTTPS POST /api/v1/submissions
┌──────────────────────────────────────────────────────────────┐
│                    백엔드 서버                                 │
│                                                              │
│  [5] 서버 수신 및 검증                                        │
│      ├─ JWT 인증                                             │
│      ├─ 페이로드 스키마 검증                                  │
│      └─ 문제 ID 유효성 확인                                   │
│                                                              │
│  [6] HTR 재검증 (서버측)                                      │
│      ├─ 클라이언트 LaTeX vs 서버 HTR 결과 비교               │
│      └─ 불일치 시: 이미지 기반 MathPix/Pix2tex 재처리        │
│                                                              │
│  [7] AI 분석 파이프라인 투입 (→ 섹션 5)                      │
└──────────────────────────────────────────────────────────────┘
```

### 4.2 온디바이스 AI 인가 상세

#### 4.2.1 인가 기준

| 조건 | 처리 |
|------|------|
| confidence ≥ 0.85 | 자동 인가 통과, 제출 허용 |
| 0.60 ≤ confidence < 0.85 | UI에 "인식된 수식이 맞나요?" 확인 팝업 표시 |
| confidence < 0.60 | "다시 써주세요" 안내 + 캔버스 초기화 옵션 |

#### 4.2.2 온디바이스 모델 사양

```
모델: MathScript-Lite v2
아키텍처: MobileViT + CTC Decoder (파인튜닝)
입력: 스트로크 시퀀스 또는 224×224 이미지
출력: LaTeX 토큰 시퀀스 + confidence score
모델 크기: ~12MB (Core ML), ~15MB (TFLite INT8)
추론 시간: < 200ms (iPhone 13 이상 / Galaxy S22 이상)
```

#### 4.2.3 인가 결과 구조

```json
{
  "recognition_result": {
    "latex": "-2(x-2)^2 + 5",
    "confidence": 0.92,
    "tokens": [
      { "token": "-2", "confidence": 0.98 },
      { "token": "(x-2)^2", "confidence": 0.91 },
      { "token": "+5", "confidence": 0.87 }
    ],
    "low_confidence_regions": []
  },
  "authenticated": true,
  "auth_timestamp": "2026-05-21T10:23:45.123Z"
}
```

### 4.3 서버 전송 페이로드

```json
{
  "submission_id": "sub_uuid_v4",
  "problem_id": "prob_20260521_001",
  "user_id": "user_abc123",
  "session_id": "sess_xyz789",
  "submitted_at": "2026-05-21T10:23:50.000Z",
  "device_info": {
    "platform": "iOS",
    "os_version": "17.4",
    "model": "iPhone 15 Pro",
    "input_device": "apple_pencil_2"
  },
  "handwriting_data": {
    "canvas_image_url": "s3://mathlens-submissions/sub_uuid_v4/canvas.png",
    "canvas_image_hash": "sha256:abc...",
    "stroke_data": {
      "format": "inkml",
      "url": "s3://mathlens-submissions/sub_uuid_v4/strokes.inkml",
      "total_strokes": 24,
      "total_duration_ms": 95400
    }
  },
  "client_recognition": {
    "full_solution_latex": "f(x)=-2x^2+8x-3\n=-2(x^2-4x)-3\n=-2(x-2)^2+5\n\\therefore \\text{최댓값}=5",
    "steps": [
      { "step": 1, "latex": "f(x)=-2x^2+8x-3", "confidence": 0.97 },
      { "step": 2, "latex": "=-2(x^2-4x)-3",   "confidence": 0.93 },
      { "step": 3, "latex": "=-2(x-2)^2+5",    "confidence": 0.91 },
      { "step": 4, "latex": "\\therefore \\text{최댓값}=5", "confidence": 0.89 }
    ],
    "final_answer_latex": "5",
    "overall_confidence": 0.925,
    "auth_passed": true
  },
  "time_spent_sec": 127,
  "hints_used": 0
}
```

### 4.4 이미지 업로드 방식 (Pre-signed URL)

네트워크 효율을 위해 이미지/잉크 파일은 S3 Pre-signed URL로 클라이언트가 직접 업로드한다:

```
1. Client → Server:  POST /api/v1/submissions/upload-url
   요청: { "problem_id": "...", "files": ["canvas.png", "strokes.inkml"] }
   응답: { "upload_urls": { "canvas.png": "https://s3.../presigned...", ... } }

2. Client → S3:     PUT <presigned_url> (이미지/잉크 직접 업로드)

3. Client → Server: POST /api/v1/submissions (위 4.3 페이로드 전송)
```

---

## 5. 문제 풀이 과정 점검 파이프라인

### 5.1 파이프라인 전체 흐름

```
[서버 수신 완료]
        │
        ▼
┌───────────────────────────────────────────┐
│  Step 1: HTR 재검증 및 정규화              │
│  ─────────────────────────────────────── │
│  • 클라이언트 LaTeX 수신                  │
│  • 서버측 HTR (MathPix / Pix2tex) 재처리  │
│  • 두 결과 비교 → 신뢰도 가중 앙상블      │
│  • 최종 정규화 LaTeX 확정                 │
└───────────────┬───────────────────────────┘
                │
                ▼
┌───────────────────────────────────────────┐
│  Step 2: 풀이 단계 파서                    │
│  ─────────────────────────────────────── │
│  • 개행/줄 단위 LaTeX 분리                │
│  • 각 줄을 수식 또는 텍스트로 분류        │
│  • 단계 번호 부여 (step_1 … step_n)       │
│  • SymPy로 각 단계 수식 파싱 검증         │
└───────────────┬───────────────────────────┘
                │
                ▼
┌───────────────────────────────────────────┐
│  Step 3: 수학적 타당성 검증                │
│  ─────────────────────────────────────── │
│  • 각 단계 간 등호/부등호 관계 검증        │
│    - step_k → step_{k+1} 변환 유효성      │
│  • 대입 검산 (최종 답을 원식에 대입)       │
│  • 부호 오류, 이항 오류 자동 탐지         │
└───────────────┬───────────────────────────┘
                │
                ▼
┌───────────────────────────────────────────┐
│  Step 4: LLM 심층 분석                    │
│  ─────────────────────────────────────── │
│  • 입력: 문제 + 정규화 풀이 + 검증 결과   │
│  • 모델: GPT-4o / Claude Sonnet           │
│  • 프롬프트: 오류 분류 + 개념 추론 지시   │
│  • 출력: 구조화 JSON (오류 목록, 개념 태그)│
└───────────────┬───────────────────────────┘
                │
                ▼
┌───────────────────────────────────────────┐
│  Step 5: 결과 저장 및 응답                 │
│  ─────────────────────────────────────── │
│  • DB에 분석 결과 저장                    │
│  • 학습 이력 업데이트                     │
│  • 클라이언트에 분석 결과 JSON 전송        │
└───────────────────────────────────────────┘
```

### 5.2 풀이 단계 파서 상세

#### 5.2.1 단계 분리 규칙

```python
# 단계 분리 로직 예시
def parse_solution_steps(full_latex: str) -> list[SolutionStep]:
    """
    풀이 LaTeX를 논리적 단계로 분리한다.
    분리 기준: 개행(\\n), \\therefore, 등호 시작 줄
    """
    lines = full_latex.split("\\n")
    steps = []
    for i, line in enumerate(lines):
        step = SolutionStep(
            step_number=i + 1,
            raw_latex=line.strip(),
            step_type=classify_step_type(line),  # equation|expression|text|conclusion
            parsed_expr=safe_parse_latex(line)
        )
        steps.append(step)
    return steps
```

#### 5.2.2 단계 유형 분류

| 유형 | 설명 | 예시 |
|------|------|------|
| `equation` | 등식 또는 변환 단계 | `f(x) = -2(x-2)^2 + 5` |
| `expression` | 수식 전개 중간 단계 | `= -2(x^2-4x) - 3` |
| `conclusion` | 최종 답 도출 | `∴ 최댓값 = 5` |
| `text` | 한글/영문 설명 | "꼭짓점 공식 적용" |
| `figure` | 그래프/도형 스케치 | (이미지 영역) |

### 5.3 수학적 타당성 검증 상세

#### 5.3.1 단계 간 변환 검증

```python
def verify_step_transition(step_k: str, step_k1: str, problem_context: dict) -> VerifyResult:
    """
    step_k에서 step_k+1로의 변환이 수학적으로 유효한지 검증
    """
    expr_k  = parse_latex(step_k)
    expr_k1 = parse_latex(step_k1)

    # 수치 검증: 양변에 랜덤 값 대입 후 동치 여부 확인
    for _ in range(5):
        test_vals = {sym: random_value() for sym in expr_k.free_symbols}
        lhs = float(expr_k.subs(test_vals).evalf())
        rhs = float(expr_k1.subs(test_vals).evalf())
        if abs(lhs - rhs) > 1e-6:
            return VerifyResult(valid=False, error_type="algebraic_error",
                                detail=f"step {k}→{k+1} 등가 불성립")
    return VerifyResult(valid=True)
```

#### 5.3.2 오류 유형 자동 분류

```
오류 탐지 규칙 트리

풀이 제출
  ├── [단계 파싱 실패] → HTR 인식 오류 (재요청)
  ├── [단계 간 등가 실패]
  │     ├── 부호 반전 오류 → 이항 부호 실수 (Procedural)
  │     ├── 계수 오류      → 산술 계산 실수 (Computational)
  │     └── 구조적 오류   → 개념 오류 (Conceptual)
  ├── [공식 패턴 불일치] → LLM에 공식 오적용 여부 추론 위임
  ├── [최종 답 불일치]
  │     ├── 풀이 과정은 정상, 마지막 단계만 오류 → 계산 실수
  │     └── 중간 단계부터 오류 → 개념/절차 오류
  └── [풀이 미완성] → 특정 단계에서 진행 불가 → 막힌 지점 개념 부족
```

### 5.4 LLM 분석 프롬프트 구조

```python
ANALYSIS_SYSTEM_PROMPT = """
당신은 수학 교육 전문 AI 분석가입니다.
학생의 수학 풀이를 분석하여 다음을 JSON 형식으로 출력하세요:
1. 각 단계의 오류 여부 및 오류 유형
2. 오류의 근본 원인이 되는 수학 개념
3. 학생이 부족한 선수 개념 목록
4. 첫 번째로 가르쳐야 할 개념과 그 이유

출력 형식은 반드시 아래 JSON 스키마를 따르세요.
"""

ANALYSIS_USER_PROMPT = """
[문제]
{problem_statement}

[학생 풀이 (단계별)]
{step_by_step_solution}

[수학적 검증 결과]
{verification_results}

[학생 학습 이력]
- 최근 오답 개념: {recent_weak_concepts}
- 현재 학년: {grade}
- 학습 레벨: {learning_level}
"""
```

---

## 6. 개념 부족 추론 및 맞춤 질문/설명 엔진

### 6.1 개념 지식 그래프 구조

수학 개념 간의 선수 학습 관계를 방향성 그래프로 모델링한다.

```
개념 지식 그래프 예시 (이차함수 영역)

        [수의 계산]
             │ 선수
             ▼
        [다항식 전개]
             │ 선수
             ▼
        [인수분해]
             │ 선수
      ┌──────┴──────┐
      ▼             ▼
[완전제곱식]   [이차방정식]
      │             │
      └──────┬──────┘
             ▼
    [이차함수의 그래프]
             │
             ▼
    [이차함수의 꼭짓점]
             │
             ▼
    [최댓값·최솟값 문제]   ← 현재 실패 지점
```

#### 6.1.1 개념 노드 스키마

```json
{
  "concept_id": "C042",
  "name": "이차함수의 꼭짓점",
  "description": "f(x)=a(x-p)²+q 형태에서 꼭짓점은 (p, q)임을 이해한다",
  "grade": "high_1",
  "curriculum_code": "10수학-3-2-1",
  "prerequisites": ["C039", "C040"],
  "mastery_threshold": 3,
  "related_errors": ["꼭짓점_좌표_혼동", "부호_오류"]
}
```

### 6.2 개념 부족 추론 알고리즘

#### 6.2.1 추론 과정

```
1. 오류 발생 지점 확인
   └─ 오류가 발생한 단계의 수학적 조작 식별
      (예: "완전제곱식 변환 단계에서 오류")

2. 오류 개념 태그 매핑
   └─ 오류 유형 → 관련 개념 조회 (개념 지식 그래프)
      (예: "완전제곱식" → concept_id: C040)

3. 선수 개념 역추적 (Backward Traversal)
   └─ 오류 개념의 모든 선수 개념 그래프 탐색
      BFS/DFS로 필요 선수 지식 트리 구성

4. 학습 이력 교차 검증
   └─ 해당 선수 개념들의 마스터리 상태 조회
      미습득 개념 = 약점 개념 후보

5. 우선순위 산출
   └─ 점수 = (오류 빈도) × (그래프 깊이의 역수) × (최근성 가중치)
      가장 높은 점수의 개념 → 즉시 학습 대상
```

#### 6.2.2 추론 결과 구조

```json
{
  "analysis_id": "ana_uuid_v4",
  "problem_id": "prob_20260521_001",
  "submission_id": "sub_uuid_v4",
  "is_correct": false,
  "final_answer_correct": true,
  "process_correct": false,
  "error_summary": {
    "error_count": 1,
    "primary_error": {
      "step": 2,
      "error_type": "Procedural",
      "error_subtype": "단계_누락",
      "description": "완전제곱식 변환 시 상수항 처리를 누락했습니다",
      "student_latex": "-2(x-2)^2 - 3",
      "correct_latex":  "-2(x-2)^2 + 5",
      "concept_tags": ["C040", "C042"]
    }
  },
  "concept_gap_analysis": {
    "weak_concepts": [
      {
        "concept_id": "C040",
        "name": "완전제곱식 변환",
        "confidence_score": 0.35,
        "priority": 1,
        "reason": "완전제곱식 전개 후 상수항 보정 미수행"
      },
      {
        "concept_id": "C039",
        "name": "인수분해 기본",
        "confidence_score": 0.72,
        "priority": 2,
        "reason": "완전제곱식의 선수 개념, 과거 오답 이력 있음"
      }
    ],
    "immediate_learning_target": "C040"
  },
  "tutoring_plan": {
    "mode": "socratic",
    "first_question": "f(x) = -2(x² - 4x) - 3 에서, (x²-4x)를 완전제곱식으로 만들기 위해 어떤 수를 더하고 빼야 할까요?",
    "concept_to_explain": "C040",
    "explanation_level": "medium"
  }
}
```

### 6.3 맞춤 질문/설명 엔진 (Adaptive Tutoring Engine)

#### 6.3.1 소크라테스 모드 대화 흐름

```
[AI 튜터 시작]
        │
        ▼
[개념 탐색 질문]
"f(x) = -2(x²-4x) - 3에서,
 (x²-4x)를 완전제곱식으로 만들기 위해
 어떤 수를 더하고 빼야 할까요?"
        │
        ├─ [정답 응답] ───────────────────────────────→ [다음 단계 질문]
        │
        ├─ [오답 응답]
        │       │
        │       ▼
        │   [힌트 제공 1]
        │   "(x ± a)² = x² ± 2ax + a² 공식을 생각해보세요"
        │       │
        │       ├─ [정답] → [다음 단계 질문]
        │       └─ [오답]
        │               │
        │               ▼
        │           [힌트 제공 2]
        │           "계수 -4의 절반인 -2를 제곱하면?"
        │               │
        │               ├─ [정답] → [다음 단계 질문]
        │               └─ [3회 실패]
        │                       │
        │                       ▼
        │                   [직접 설명 모드로 전환]
        │                   개념 카드 + 예제 제시
        │
        └─ [무응답/건너뛰기] → [직접 설명 모드]

[모든 질문 완료]
        │
        ▼
[개념 습득 확인 퀴즈]
        │
        ├─ [통과] → 마스터리 카운터 +1, 유사 문제 제시
        └─ [미통과] → 동일 개념 다른 접근법으로 재설명
```

#### 6.3.2 질문 생성 LLM 프롬프트

```python
TUTORING_QUESTION_PROMPT = """
당신은 수학 개인 튜터입니다. 소크라테스식 문답법으로 학생이 스스로 개념을 발견하도록 안내하세요.

[학생이 틀린 개념]: {concept_name}
[학생 오류 내용]: {error_description}
[학생 학년/수준]: {grade} / {level}
[현재 대화 단계]: {dialogue_step} / {max_steps}
[이전 학생 답변]: {previous_answer}

규칙:
1. 정답을 직접 알려주지 마세요 (힌트 2회까지)
2. 질문은 한 번에 하나만 하세요
3. 학생 수준에 맞는 용어를 사용하세요
4. 칭찬과 격려를 포함하세요
5. 3회 실패 시에만 직접 설명으로 전환하세요

출력: { "question": "...", "hint_level": 0|1|2, "switch_to_explain": true|false }
"""
```

#### 6.3.3 개념 설명 레벨 체계

| 레벨 | 대상 | 특징 |
|------|------|------|
| `basic` | 중학교 1~2학년 수준 | 일상 언어 + 시각적 예시 중심 |
| `medium` | 중학교 3학년 ~ 고등학교 1학년 | 수학적 언어 + 예제 2개 |
| `advanced` | 고등학교 2~3학년 | 수학적 정의 + 증명 개요 + 예제 |
| `exam` | 수능/모의고사 대비 | 출제 패턴 + 빠른 풀이 전략 |

### 6.4 학습 이력 반영 메커니즘

```
개념 마스터리 상태 머신

        ┌────────────────────────────────────────┐
        │                                        │
 [미학습]──[1회 정답]──[2회 정답]──[3회 연속 정답]──[마스터리]
   │         │             │              │           │
   │      [오답]         [오답]         [오답]        │
   │         │             │              │           │
   └─────────┴─────────────┴──────────────┘           │
                     개념 재학습 큐 투입               │
                                                       │
                                             [간격 반복 스케줄]
                                             3일 → 7일 → 14일 → 30일
                                             복습 문제 재등장
```

---

## 7. 데이터 모델

### 7.1 핵심 엔티티

```sql
-- 사용자
CREATE TABLE users (
    user_id     UUID PRIMARY KEY,
    email       VARCHAR(255) UNIQUE NOT NULL,
    grade       VARCHAR(20),          -- 'middle_1' ~ 'high_3'
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- 문제
CREATE TABLE problems (
    problem_id       VARCHAR(50) PRIMARY KEY,
    version          INTEGER DEFAULT 1,
    subject          VARCHAR(50),
    unit             VARCHAR(100),
    topic            VARCHAR(100),
    difficulty       SMALLINT CHECK (difficulty BETWEEN 1 AND 5),
    statement_latex  TEXT NOT NULL,
    answer_latex     TEXT NOT NULL,
    solution_steps   JSONB,
    concepts_required VARCHAR(20)[] REFERENCES concepts(concept_id),
    created_at       TIMESTAMPTZ DEFAULT NOW()
);

-- 수학 개념
CREATE TABLE concepts (
    concept_id       VARCHAR(20) PRIMARY KEY,
    name             VARCHAR(100) NOT NULL,
    description      TEXT,
    grade            VARCHAR(20),
    prerequisite_ids VARCHAR(20)[],
    mastery_threshold SMALLINT DEFAULT 3
);

-- 제출 및 분석 결과
CREATE TABLE submissions (
    submission_id    UUID PRIMARY KEY,
    user_id          UUID REFERENCES users(user_id),
    problem_id       VARCHAR(50) REFERENCES problems(problem_id),
    submitted_at     TIMESTAMPTZ DEFAULT NOW(),
    client_latex     TEXT,
    canvas_image_url TEXT,
    stroke_data_url  TEXT,
    time_spent_sec   INTEGER,
    hints_used       SMALLINT DEFAULT 0
);

CREATE TABLE analysis_results (
    analysis_id      UUID PRIMARY KEY,
    submission_id    UUID REFERENCES submissions(submission_id),
    is_correct       BOOLEAN,
    process_correct  BOOLEAN,
    error_data       JSONB,
    weak_concepts    VARCHAR(20)[],
    tutoring_plan    JSONB,
    analyzed_at      TIMESTAMPTZ DEFAULT NOW()
);

-- 개념별 마스터리 상태
CREATE TABLE concept_mastery (
    user_id          UUID REFERENCES users(user_id),
    concept_id       VARCHAR(20) REFERENCES concepts(concept_id),
    correct_streak   SMALLINT DEFAULT 0,
    mastered         BOOLEAN DEFAULT FALSE,
    mastered_at      TIMESTAMPTZ,
    next_review_at   TIMESTAMPTZ,
    PRIMARY KEY (user_id, concept_id)
);

-- 튜터링 대화 세션
CREATE TABLE tutoring_sessions (
    session_id       UUID PRIMARY KEY,
    analysis_id      UUID REFERENCES analysis_results(analysis_id),
    concept_id       VARCHAR(20),
    dialogue_turns   JSONB,   -- [{role, content, timestamp}]
    completed        BOOLEAN DEFAULT FALSE,
    created_at       TIMESTAMPTZ DEFAULT NOW()
);
```

---

## 8. API 명세

### 8.1 문제 전달 API

| Method | Endpoint | 설명 |
|--------|----------|------|
| `GET` | `/api/v1/problems/today` | 오늘의 추천 문제 목록 (최대 10개) |
| `GET` | `/api/v1/problems/{problem_id}` | 특정 문제 상세 조회 |
| `GET` | `/api/v1/problems/by-concept/{concept_id}` | 특정 개념 관련 문제 목록 |
| `POST` | `/api/v1/problems/generate` | 유사 문제 동적 생성 |

**GET /api/v1/problems/today 응답 예시**

```json
{
  "recommended_problems": [ /* Problem Schema 배열 */ ],
  "review_problems": [ /* 간격 반복 복습 문제 */ ],
  "total_count": 8,
  "generated_at": "2026-05-21T09:00:00Z"
}
```

### 8.2 제출 및 분석 API

| Method | Endpoint | 설명 |
|--------|----------|------|
| `POST` | `/api/v1/submissions/upload-url` | S3 Pre-signed URL 발급 |
| `POST` | `/api/v1/submissions` | 풀이 제출 (분석 요청) |
| `GET` | `/api/v1/submissions/{submission_id}/status` | 분석 처리 상태 조회 (polling) |
| `GET` | `/api/v1/submissions/{submission_id}/result` | 분석 결과 조회 |

**POST /api/v1/submissions 응답 예시**

```json
{
  "submission_id": "sub_uuid_v4",
  "status": "processing",
  "estimated_seconds": 5,
  "polling_url": "/api/v1/submissions/sub_uuid_v4/status",
  "websocket_channel": "ws://api.mathlens.ai/ws/analysis/sub_uuid_v4"
}
```

### 8.3 튜터링 API

| Method | Endpoint | 설명 |
|--------|----------|------|
| `POST` | `/api/v1/tutoring/start` | 튜터링 세션 시작 |
| `POST` | `/api/v1/tutoring/{session_id}/respond` | 학생 답변 제출 |
| `GET` | `/api/v1/tutoring/{session_id}/next` | 다음 질문/설명 요청 |
| `POST` | `/api/v1/tutoring/{session_id}/complete` | 세션 완료 처리 |

### 8.4 학습 이력 API

| Method | Endpoint | 설명 |
|--------|----------|------|
| `GET` | `/api/v1/users/{user_id}/concepts` | 개념 마스터리 현황 전체 |
| `GET` | `/api/v1/users/{user_id}/weak-concepts` | 취약 개념 목록 (우선순위 순) |
| `GET` | `/api/v1/users/{user_id}/report/weekly` | 주간 학습 리포트 |
| `GET` | `/api/v1/users/{user_id}/report/monthly` | 월간 학습 리포트 |

### 8.5 분석 결과 WebSocket 이벤트

실시간 분석 진행 상황을 클라이언트에 스트리밍:

```
ws://api.mathlens.ai/ws/analysis/{submission_id}

이벤트 시퀀스:
{ "event": "htr_complete",     "step": 1, "progress": 20 }
{ "event": "parsing_complete", "step": 2, "progress": 40 }
{ "event": "verify_complete",  "step": 3, "progress": 60 }
{ "event": "llm_complete",     "step": 4, "progress": 85 }
{ "event": "analysis_done",    "step": 5, "progress": 100,
  "result_url": "/api/v1/submissions/{id}/result" }
```

---

## 9. 비기능 요구사항

### 9.1 성능 요구사항

| 항목 | 목표 | 최대 허용 |
|------|------|-----------|
| 온디바이스 HTR 추론 | < 200ms | 500ms |
| 서버 HTR 재검증 | < 1s | 2s |
| 풀이 단계 파싱 | < 500ms | 1s |
| LLM 분석 (전체) | < 5s | 10s |
| 문제 목록 API 응답 | < 300ms | 1s |
| WebSocket 이벤트 지연 | < 100ms | 300ms |

### 9.2 가용성 및 확장성

- **API 서버 가용성**: 99.9% SLA (월 다운타임 < 44분)
- **오토스케일링**: 동시 사용자 10,000명까지 자동 확장
- **LLM API 장애 대응**: Fallback LLM 설정 (Claude ↔ GPT-4o)
- **CDN**: 문제 이미지 및 개념 설명 리소스는 CloudFront 배포

### 9.3 오프라인 동작

- 문제 캐시: 최대 10문제 로컬 저장
- 온디바이스 HTR: 네트워크 없이 동작
- 오프라인 제출 큐: 재연결 시 자동 업로드

---

## 10. 보안 및 개인정보 보호

### 10.1 데이터 전송 보안

| 항목 | 요구사항 |
|------|---------|
| 전송 암호화 | TLS 1.3 필수 (TLS 1.2 이하 차단) |
| API 인증 | JWT (RS256, 만료 1시간) + Refresh Token (7일) |
| 이미지 업로드 | S3 Pre-signed URL (유효시간 5분) |
| WebSocket | WSS (WebSocket Secure) 전용 |

### 10.2 개인정보 처리

- 미성년자(만 14세 미만) 데이터: 법정대리인 동의 필수
- 풀이 이미지: S3 암호화 저장 (SSE-KMS), 사용자 계정 삭제 시 30일 내 영구 삭제
- 개인 식별 정보(PII)와 학습 데이터 분리 저장
- 학습 데이터의 AI 모델 재학습 사용 시 명시적 동의 획득

### 10.3 OWASP Mobile Top 10 대응

| 위협 | 대응 방안 |
|------|-----------|
| M1 부적절한 자격증명 사용 | Keychain (iOS) / KeyStore (Android)에 토큰 저장 |
| M2 불충분한 공급망 보안 | 의존성 취약점 스캔 (Dependabot) |
| M4 인증 및 권한 부여 불충분 | 모든 API 엔드포인트 JWT 필수 검증 |
| M8 보안 구성 오류 | Certificate Pinning 적용 |

---

## 11. 수락 기준 (Acceptance Criteria)

### 11.1 문제 전달

- [ ] 홈 화면 진입 후 3초 이내 추천 문제 목록이 표시된다
- [ ] 오프라인 상태에서도 캐시된 문제로 학습이 가능하다
- [ ] 재연결 후 오프라인 제출 결과가 자동 서버 전송된다

### 11.2 펜 입력 인가 및 전송

- [ ] 펜 입력 완료 후 200ms 이내 LaTeX 변환 결과가 화면에 표시된다
- [ ] confidence < 0.85인 경우 사용자 확인 팝업이 표시된다
- [ ] 제출 버튼 클릭 후 5초 이내 "분석 중" 첫 이벤트가 WebSocket으로 수신된다

### 11.3 풀이 과정 점검

- [ ] 틀린 단계가 빨간 하이라이트로 화면에 표시된다
- [ ] 오류 유형(개념/절차/계산/문제이해)이 배지로 명시된다
- [ ] 분석 결과에 오류 개념 태그가 1개 이상 포함된다

### 11.4 개념 부족 추론 및 튜터링

- [ ] 분석 완료 후 취약 개념 우선순위 목록이 제공된다
- [ ] AI 튜터가 정답을 직접 알려주지 않고 소크라테스식 질문으로 시작한다
- [ ] 3회 실패 시 자동으로 직접 설명 모드로 전환된다
- [ ] 동일 개념 연속 3회 정답 시 마스터리로 처리되어 개념 맵에 반영된다

---

*본 문서는 MathLens AI v1.0 개발 범위를 기준으로 작성되었으며, Phase 2 이후 기능은 별도 PRD로 보완된다.*

*© 2026 MathLens AI Project. All rights reserved.*
