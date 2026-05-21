# 백엔드 문제 출제 및 펜 입력 AI 인식 시스템 — 제품 요구사항 명세서 (PRD)

**문서 버전:** v1.0  
**작성일:** 2026년 5월 21일  
**문서 유형:** Product Requirements Document (PRD)  
**관련 프로젝트:** MathLens AI  
**관련 RFP:** `RFP_ProblemServing_PenRecognition.md`

---

## 목차

1. [제품 개요](#1-제품-개요)
2. [목표 및 성공 지표](#2-목표-및-성공-지표)
3. [사용자 스토리](#3-사용자-스토리)
4. [시스템 아키텍처](#4-시스템-아키텍처)
5. [기능 요구사항 — 백엔드 문제 출제](#5-기능-요구사항--백엔드-문제-출제)
6. [기능 요구사항 — 클라이언트 펜 입력](#6-기능-요구사항--클라이언트-펜-입력)
7. [기능 요구사항 — AI 인식 파이프라인](#7-기능-요구사항--ai-인식-파이프라인)
8. [API 계약](#8-api-계약)
9. [데이터 모델](#9-데이터-모델)
10. [비기능 요구사항](#10-비기능-요구사항)
11. [오류 처리 및 예외 시나리오](#11-오류-처리-및-예외-시나리오)
12. [테스트 요구사항](#12-테스트-요구사항)
13. [배포 및 운영 요구사항](#13-배포-및-운영-요구사항)
14. [변경 이력](#14-변경-이력)

---

## 1. 제품 개요

### 1.1 목적

본 PRD는 MathLens AI 앱에서 다음 두 서브시스템의 구현 요구사항을 정의합니다.

1. **문제 출제 서브시스템**: 백엔드 서버가 학습자 맞춤형 수학 문제를 선정·생성하여 클라이언트에 전달
2. **펜 입력 AI 인식 서브시스템**: 사용자가 펜으로 작성한 답안을 캡처하여 AI 엔진이 수식으로 인식

### 1.2 두 서브시스템의 관계

```
문제 출제                펜 입력 제출              AI 인식
─────────────           ─────────────             ─────────────
문제 DB + 추천 로직  →  사용자 펜으로 답안 작성  →  HTR + LLM 분석
문제 ID 발급         →  이미지 캡처·전송          →  LaTeX 변환 + 채점
```

두 서브시스템은 `problem_id`와 `submission_id`를 통해 연결됩니다.

### 1.3 스코프 외 항목

- 오답 원인 분석 세부 로직 (별도 PRD 참조)
- 맞춤형 피드백 및 개념 설명 생성 (별도 PRD 참조)
- 학습 리포트 및 대시보드 (별도 PRD 참조)

---

## 2. 목표 및 성공 지표

### 2.1 제품 목표

| 번호 | 목표 |
|------|------|
| G1 | 학습자가 매 세션마다 자신의 수준에 맞는 문제를 자동으로 받아볼 수 있다 |
| G2 | 종이에 쓰는 것과 동일한 자연스러운 필기 경험을 제공한다 |
| G3 | 펜으로 작성한 수식을 3초 이내에 95% 이상 정확도로 AI가 인식한다 |
| G4 | 전체 처리 파이프라인이 10초 이내에 완료된다 |

### 2.2 성공 지표 (KPI)

| 지표 | 기준값 | 측정 방법 |
|------|--------|-----------|
| 수식 HTR 정확도 | ≥ 95% | 100개 샘플 LaTeX CER 측정 |
| 전체 파이프라인 지연 (p95) | ≤ 10초 | 서버 APM 측정 |
| 문제 추천 API 응답 시간 (p99) | ≤ 1,000ms | 서버 APM 측정 |
| 사용자 제출 성공률 | ≥ 99% | 에러율 모니터링 |
| 캔버스 렌더링 지연 | ≤ 16ms/frame | 프로파일러 측정 |
| 일일 활성 사용자 중 문제 풀이 완료율 | ≥ 70% | 앱 이벤트 분석 |

---

## 3. 사용자 스토리

### 3.1 학습자

| ID | 사용자 스토리 | 우선순위 |
|----|--------------|----------|
| US-01 | 학습자로서, 앱을 열었을 때 오늘 내 수준에 맞는 문제를 즉시 받아보고 싶다 | P0 |
| US-02 | 학습자로서, 펜으로 수학 풀이를 자연스럽게 쓸 수 있는 큰 캔버스가 필요하다 | P0 |
| US-03 | 학습자로서, 쓴 내용을 지우고 다시 쓸 수 있어야 한다 | P0 |
| US-04 | 학습자로서, 풀이를 제출하면 AI가 정확히 인식했는지 확인할 수 있어야 한다 | P1 |
| US-05 | 학습자로서, 인식된 수식이 틀렸다면 직접 수정할 수 있어야 한다 | P1 |
| US-06 | 학습자로서, 틀린 문제와 비슷한 문제를 바로 다음에 풀고 싶다 | P1 |
| US-07 | 학습자로서, 인터넷이 느려도 캔버스가 부드럽게 동작해야 한다 | P2 |
| US-08 | 학습자로서, 이전에 풀었던 손글씨 답안을 다시 볼 수 있어야 한다 | P2 |

### 3.2 교사 / 학부모

| ID | 사용자 스토리 | 우선순위 |
|----|--------------|----------|
| US-09 | 교사로서, 학생이 제출한 손글씨 풀이 이미지를 확인할 수 있어야 한다 | P2 |
| US-10 | 학부모로서, 자녀가 어떤 문제를 풀었는지 기록이 남아야 한다 | P2 |

---

## 4. 시스템 아키텍처

### 4.1 컴포넌트 다이어그램

```
┌──────────────────────────────────────────────────────────────────┐
│                        모바일 클라이언트                           │
│                                                                   │
│  ┌─────────────────┐    ┌──────────────────────────────────────┐ │
│  │  문제 표시 뷰    │    │          펜 입력 캔버스                │ │
│  │  (ProblemView)  │    │  ┌─────────┐  ┌────────────────────┐ │ │
│  │                 │    │  │ 스트로크 │  │  도구 모음          │ │ │
│  │  - 문제 텍스트  │    │  │ 렌더러  │  │ (펜/지우개/되돌리기)│ │ │
│  │  - 문제 이미지  │    │  └────┬────┘  └────────────────────┘ │ │
│  └────────┬────────┘    │       │                               │ │
│           │             │  [제출 버튼]                           │ │
│           │             │       │                               │ │
│           │             │  ┌────▼───────────────────────────┐  │ │
│           │             │  │ ImageCaptureService             │  │ │
│           │             │  │ - 캔버스 → PNG                  │  │ │
│           │             │  │ - 크롭 + 리사이징                │  │ │
│           │             │  │ - Base64 인코딩                 │  │ │
│           │             │  └────────────────────────────────┘  │ │
│           │             └──────────────────────────────────────┘ │
└───────────┼─────────────────────────────────┼────────────────────┘
            │  GET /problems/recommend         │  POST /submissions
            ▼                                  ▼
┌───────────────────────────────────────────────────────────────────┐
│                         API Gateway (FastAPI)                      │
└──────────┬───────────────────────────────────────┬────────────────┘
           │                                       │
     ┌─────▼──────────────┐              ┌─────────▼──────────────┐
     │  문제 출제 서비스   │              │  제출 수신 서비스       │
     │                    │              │                        │
     │ ┌────────────────┐ │              │ ┌────────────────────┐ │
     │ │ 문제 추천 엔진 │ │              │ │ 이미지 S3 저장     │ │
     │ │ (Rule + ML)    │ │              │ │ submission_id 발급 │ │
     │ └────────────────┘ │              │ │ Celery 큐 등록     │ │
     │ ┌────────────────┐ │              │ └────────────────────┘ │
     │ │ LLM 문제 생성  │ │              └────────────┬───────────┘
     │ └────────────────┘ │                           │
     │ ┌────────────────┐ │                           ▼
     │ │  문제은행 DB   │ │              ┌────────────────────────┐
     │ │ (PostgreSQL)   │ │              │    AI 인식 Worker      │
     │ └────────────────┘ │              │  (Celery + Redis)      │
     └────────────────────┘              │                        │
                                         │ ┌──────────────────┐  │
                                         │ │ 이미지 전처리     │  │
                                         │ │ (OpenCV)         │  │
                                         │ └──────────────────┘  │
                                         │ ┌──────────────────┐  │
                                         │ │ HTR 엔진          │  │
                                         │ │ (수식+텍스트)    │  │
                                         │ └──────────────────┘  │
                                         │ ┌──────────────────┐  │
                                         │ │ LaTeX 후처리      │  │
                                         │ │ (SymPy 검증)     │  │
                                         │ └──────────────────┘  │
                                         │ ┌──────────────────┐  │
                                         │ │ 멀티모달 LLM     │  │
                                         │ │ 분석 요청        │  │
                                         │ └──────────────────┘  │
                                         └────────────┬───────────┘
                                                      │
                                         ┌────────────▼───────────┐
                                         │ 결과 저장 + 클라이언트  │
                                         │ WebSocket 푸시          │
                                         └────────────────────────┘
```

### 4.2 기술 스택

| 영역 | 기술 | 버전 |
|------|------|------|
| 백엔드 API | Python FastAPI | 0.110+ |
| 비동기 작업 큐 | Celery + Redis | Celery 5.x |
| 주 DB | PostgreSQL | 16+ |
| 캐시 | Redis | 7+ |
| 이미지 저장 | AWS S3 (또는 호환) | — |
| 이미지 처리 | OpenCV, Pillow | OpenCV 4.x |
| LaTeX 수식 처리 | SymPy | 1.12+ |
| HTR 엔진 | MathPix API / MyScript | — |
| LLM | OpenAI GPT-4o / Claude | — |
| iOS 클라이언트 | Swift + SwiftUI + PencilKit | iOS 16+ |
| Android 클라이언트 | Kotlin + Jetpack Compose + Ink API | Android 10+ |

---

## 5. 기능 요구사항 — 백엔드 문제 출제

### 5.1 문제은행 관리

#### FR-PB-01: 문제 CRUD

- 관리자 API를 통해 문제 생성·수정·삭제·조회 가능
- 문제 상태: `draft` → `review` → `active` → `archived`
- `active` 상태 문제만 학습자에게 출제

#### FR-PB-02: 문제 태깅

- 각 문제에 `concept_tags` (교육과정 단원 기반)와 `error_type_tags` (오답 유형 기반) 부착 필수
- 태그 체계는 국내 2022 개정 교육과정 중·고등학교 수학 단원 코드 기준

#### FR-PB-03: 문제 버전 관리

- 문제 수정 시 이전 버전 보존 (이미 제출 이력이 있는 문제의 원본 보호)

### 5.2 개인화 문제 추천

#### FR-REC-01: 추천 알고리즘

추천 엔진은 다음 입력 데이터를 활용합니다.

| 입력 데이터 | 활용 방식 |
|-------------|-----------|
| 사용자 학년 | 학년 필터 적용 |
| 최근 오답 개념 태그 (최근 30일) | 오답 개념 우선 출제 (가중치 70%) |
| 개념별 정답률 | 정답률 낮은 개념 우선 |
| 직전 연속 정답 횟수 | 난이도 자동 상향 (연속 3회 정답 시 +1 난이도) |
| 당일 이미 출제된 문제 ID 목록 | 중복 제외 |
| 취약/강점 개념 비율 | 취약:강점 = 7:3 비율 유지 |

#### FR-REC-02: 추천 요청/응답

- 요청 시 `limit` 개수만큼 문제 목록 반환 (기본 1, 최대 10)
- 응답에 문제 본문, 이미지 URL, 메타데이터 포함
- 추천 이유(concept_tags 기준)를 선택적 필드로 반환 (디버그용)

#### FR-REC-03: 동일 문제 재출제 제한

- 동일 `user_id` + `problem_id` 조합은 24시간 내 재출제 금지
- 단, 교사/관리자가 강제 재출제 지정 시 예외 허용

### 5.3 LLM 기반 문제 동적 생성

#### FR-GEN-01: 유사 문제 생성 트리거

다음 조건에서 자동 트리거:
- 문제은행에서 조건을 충족하는 문제가 `limit` 수를 채우지 못할 때
- 분석 엔진이 유사 문제 생성을 명시적으로 요청할 때 (`POST /problems/generate`)

#### FR-GEN-02: 생성 프롬프트 구성

LLM 프롬프트에 포함되는 필수 요소:
1. 원본 문제 전문 및 정답
2. 변형 유형 (`number_change` / `condition_change` / `context_change`)
3. 대상 학년 및 난이도
4. 2022 개정 교육과정 범위 준수 지시
5. LaTeX 형식으로 문제 및 정답 출력 지시

#### FR-GEN-03: 생성 결과 검증

생성된 문제는 자동 검증 파이프라인 통과 후 문제은행에 저장:
1. LaTeX 수식 문법 파싱 성공 여부 확인 (SymPy)
2. 정답이 수치적으로 계산 가능한지 확인
3. 원본 문제와 동일 개념 태그 포함 확인
4. 검증 실패 시 `draft` 상태로 저장 후 수동 검토 대기

---

## 6. 기능 요구사항 — 클라이언트 펜 입력

### 6.1 캔버스 기본 기능

#### FR-CV-01: 실시간 스트로크 렌더링

- 렌더링 지연: **16ms 이하** (60 FPS 이상 유지)
- 필압 지원 스타일러스 사용 시 필압에 따른 선 굵기 변화 반영
- 팜 리젝션: 스타일러스 입력 감지 시 터치 입력 무시

#### FR-CV-02: 도구 모음

| 도구 | 기능 |
|------|------|
| 펜 | 굵기 3단계, 색상 3종 이상 (검정·파랑·빨강 필수) |
| 지우개 | 스트로크 단위 지우개, 픽셀 지우개 선택 가능 |
| 전체 지우기 | 확인 다이얼로그 후 캔버스 초기화 |
| 실행취소 | 마지막 스트로크 제거 (무제한) |
| 재실행 | 실행취소 복원 (무제한) |

#### FR-CV-03: 캔버스 뷰포트 조작

- 핀치 줌: 1.0x ~ 3.0x 확대 (줌 시 문제 영역 숨기지 않음)
- 스크롤: 캔버스가 화면보다 클 경우 두 손가락 스크롤
- 줌 초기화 버튼 제공

#### FR-CV-04: 자동 저장

- 스트로크 입력 중 30초마다 로컬 임시 저장 (`UserDefaults` / `Room DB`)
- 앱 재시작 시 미제출 풀이 복원 여부 사용자에게 안내

### 6.2 이미지 캡처 및 전처리

#### FR-CAP-01: 캔버스 캡처

- 제출 버튼 탭 시 캔버스를 `UIImage` (iOS) 또는 `Bitmap` (Android)으로 변환
- 배경색: 흰색 고정
- 해상도: 디바이스 화면 밀도 기준 최소 1080×1440 논리픽셀 해당 크기

#### FR-CAP-02: 클라이언트 전처리 파이프라인

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

#### FR-CAP-03: 스트로크 메타데이터 수집

제출 데이터에 다음 메타데이터를 선택적으로 포함:

```json
{
  "stroke_count": 42,
  "total_duration_ms": 35000,
  "canvas_size": { "width": 1080, "height": 1440 },
  "input_type": "stylus"
}
```

### 6.3 서버 전송

#### FR-TX-01: 전송 방식

- HTTP POST 멀티파트 또는 JSON body (Base64 이미지)
- 전송 전 네트워크 상태 확인 (오프라인 시 로컬 큐 저장 후 재전송)
- 재전송 정책: 지수 백오프 (1초 → 2초 → 4초, 최대 3회)

#### FR-TX-02: 전송 피드백

- 전송 중 로딩 인디케이터 표시
- 접수 완료(202) 수신 시 "AI가 분석 중입니다..." 상태 표시
- WebSocket 연결 후 단계별 진행 상태 업데이트

#### FR-TX-03: 인식 결과 표시

AI 인식이 완료되면 클라이언트는:
1. 인식된 LaTeX를 렌더링하여 사용자에게 표시
2. "이 인식이 맞나요?" 확인 UI 제공
3. 오인식 구간 직접 수정 기능 제공 (LaTeX 편집 또는 재작성)
4. 사용자 확인 후 분석 결과 화면으로 전환

---

## 7. 기능 요구사항 — AI 인식 파이프라인

### 7.1 파이프라인 오케스트레이션

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
    ├── Step 1: 이미지 전처리
    ├── Step 2: HTR 실행
    ├── Step 3: LaTeX 후처리
    ├── Step 4: 분석 엔진 호출
    └── Step 5: 결과 저장 + 푸시
```

각 단계 완료 시 WebSocket으로 클라이언트에 상태 전송.

#### FR-AI-02: 타임아웃 처리

| 단계 | 타임아웃 | 타임아웃 시 처리 |
|------|----------|----------------|
| 이미지 전처리 | 5초 | 원본 이미지로 HTR 진행 |
| HTR API 호출 | 10초 | 재시도 1회 후 실패 처리 |
| LLM 분석 | 30초 | 재시도 1회 후 실패 처리 |

### 7.2 서버 사이드 이미지 전처리

#### FR-PP-01: 전처리 단계

| 단계 | 알고리즘 | 파라미터 |
|------|----------|----------|
| 1. 그레이스케일 변환 | `cv2.cvtColor(BGR2GRAY)` | — |
| 2. 이진화 | Otsu's Threshold | `cv2.THRESH_BINARY + THRESH_OTSU` |
| 3. 노이즈 제거 | 가우시안 블러 | 커널 (3,3), σ=0 |
| 4. 기울기 보정 | Hough Line Transform | threshold=100 |
| 5. 행 분리 | Horizontal Projection Profile | 행 간격 최소 10px |
| 6. 수식/텍스트 분류 | 좌측→우측 스캔 기반 규칙 또는 YOLO 모델 | — |

#### FR-PP-02: 수식 영역 추출

- 인식 정확도 향상을 위해 수식 영역을 크롭하여 HTR에 개별 전달
- 각 크롭 이미지에 위치 정보(좌표) 유지하여 원본 이미지에 오버레이 가능하도록 저장

### 7.3 HTR 엔진

#### FR-HTR-01: 수식 인식

- 입력: 전처리된 이미지 (PNG)
- 출력: LaTeX 문자열 + 신뢰도 점수 (0.0 ~ 1.0)
- 신뢰도 < 0.8 구간: 클라이언트에 "인식 불확실" 표시 및 수정 요청

#### FR-HTR-02: 텍스트 인식

- 한글/영문 손글씨 텍스트를 UTF-8 문자열로 변환
- 수식과 텍스트 영역이 혼재 시 영역별 독립 처리 후 순서대로 병합

#### FR-HTR-03: 결과 구조

```json
{
  "htr_result": {
    "raw_latex": "2x^{2} + 3x - 5 = 0",
    "steps": [
      { "order": 1, "latex": "2x^{2} + 3x - 5 = 0", "confidence": 0.97 },
      { "order": 2, "latex": "(2x - 1)(x + 5) = 0", "confidence": 0.94 },
      { "order": 3, "latex": "x = \\frac{1}{2} \\quad \\text{또는} \\quad x = -5", "confidence": 0.96 }
    ],
    "text_blocks": [
      { "order": 1, "text": "인수분해를 이용해 풀면", "confidence": 0.91 }
    ],
    "overall_confidence": 0.95
  }
}
```

### 7.4 LaTeX 후처리 및 정답 판별

#### FR-LATEX-01: AST 파싱

- SymPy `parse_latex()`로 LaTeX → 수식 객체 변환
- 파싱 실패 시 오류 로그 기록, 원본 LaTeX 그대로 LLM에 전달

#### FR-LATEX-02: 수학적 동치 판별

```python
from sympy.parsing.latex import parse_latex
from sympy import simplify, Symbol

def is_mathematically_equivalent(student_latex: str, correct_latex: str) -> bool:
    try:
        student_expr = parse_latex(student_latex)
        correct_expr = parse_latex(correct_latex)
        diff = simplify(student_expr - correct_expr)
        return diff == 0
    except Exception:
        return None  # 판별 불가 → LLM에 위임
```

#### FR-LATEX-03: 풀이 단계 구조화

- 인식된 LaTeX에서 등호·줄바꿈·번호 패턴 기반으로 풀이 단계 분리
- 분리된 각 단계에 순번 부여
- 전체 LaTeX와 단계별 LaTeX를 분석 엔진에 전달

### 7.5 멀티모달 LLM 연동

#### FR-LLM-01: 입력 구성

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

#### FR-LLM-02: 출력 스키마

LLM 응답은 다음 JSON 스키마를 따라야 합니다.

```json
{
  "is_correct": true,
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

#### FR-LLM-03: 프롬프트 버전 관리

- 프롬프트 템플릿은 DB에 버전 관리하여 저장
- A/B 테스트를 통해 피드백 품질 비교 가능하도록 프롬프트 ID를 결과에 기록

---

## 8. API 계약

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

### 8.2 풀이 제출 API

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

### 8.3 처리 상태 WebSocket 메시지

| 단계 | 메시지 |
|------|--------|
| 이미지 수신 | `{"stage": "received", "ts": "..."}` |
| 전처리 완료 | `{"stage": "preprocessed", "ts": "..."}` |
| HTR 완료 | `{"stage": "htr_done", "latex_preview": "...", "confidence": 0.96, "ts": "..."}` |
| 분석 완료 | `{"stage": "analysis_done", "result_id": "uuid", "is_correct": true, "ts": "..."}` |
| 오류 발생 | `{"stage": "error", "error_code": "HTR_TIMEOUT", "message": "...", "ts": "..."}` |

### 8.4 인식 결과 조회 API

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
  "htr_result": { ... },
  "analysis_result": { ... },
  "image_url": "https://...",
  "status": "completed"
}
```

---

## 9. 데이터 모델

### 9.1 테이블 ERD 요약

```
problems
├── problem_id (PK, UUID)
├── title
├── content_text
├── content_image_key (S3 key)
├── answer_latex
├── solution_steps (JSONB)
├── subject (enum)
├── grade (enum)
├── difficulty (int, 1-5)
├── concept_tags (text[])
├── error_type_tags (text[])
├── curriculum_code
├── source (enum: bank|llm_generated|textbook)
├── status (enum: draft|review|active|archived)
├── created_at, updated_at

submissions
├── submission_id (PK, UUID)
├── user_id (FK → users)
├── problem_id (FK → problems)
├── session_id (UUID)
├── image_s3_key
├── stroke_metadata (JSONB)
├── device_info (JSONB)
├── status (enum: received|processing|completed|failed)
├── submitted_at
├── processed_at

recognition_results
├── result_id (PK, UUID)
├── submission_id (FK → submissions, UNIQUE)
├── htr_raw_latex
├── htr_steps (JSONB)
├── htr_confidence (float)
├── is_correct (bool)
├── error_steps (JSONB)
├── analysis_summary
├── feedback_message
├── concept_tags_inferred (text[])
├── llm_model_version
├── prompt_template_id
├── created_at

user_problem_history
├── id (PK)
├── user_id (FK → users)
├── problem_id (FK → problems)
├── submission_id (FK → submissions)
├── is_correct
├── error_type (enum)
├── solved_at
```

### 9.2 인덱스 전략

| 테이블 | 인덱스 컬럼 | 이유 |
|--------|------------|------|
| `problems` | `(grade, subject, difficulty, status)` | 추천 필터 쿼리 |
| `problems` | `concept_tags` GIN 인덱스 | 태그 기반 검색 |
| `submissions` | `(user_id, submitted_at)` | 사용자별 이력 조회 |
| `user_problem_history` | `(user_id, problem_id)` | 중복 출제 방지 조회 |
| `user_problem_history` | `(user_id, error_type, solved_at)` | 오답 유형 통계 |

---

## 10. 비기능 요구사항

### 10.1 성능

| 요구사항 | 기준 |
|----------|------|
| 문제 추천 API p99 응답 시간 | ≤ 1,000ms |
| 풀이 제출 접수 (202) 응답 시간 | ≤ 500ms |
| HTR 처리 시간 (서버 기준) | ≤ 4,000ms |
| 전체 파이프라인 p95 완료 시간 | ≤ 10,000ms |
| 동시 처리 제출 수 | 500건/분 이상 |
| 캔버스 렌더링 프레임 속도 | ≥ 60 FPS |

### 10.2 확장성

- API 서버: 수평 확장 가능한 스테이트리스 설계 (Docker + ECS/K8s)
- Celery Worker: 부하에 따라 자동 스케일링 (AWS ECS Auto Scaling)
- 문제은행 DB: 읽기 복제본(Read Replica) 지원

### 10.3 가용성

- API 서버: 월간 가용성 99.5% 이상
- 다중 AZ 배포 (AWS Multi-AZ RDS, Redis Cluster)
- Celery Worker 장애 시 작업 재시도: 최대 3회 (exponential backoff)

### 10.4 보안

- 모든 API 엔드포인트: JWT 인증 필수 (`Authorization: Bearer`)
- S3 이미지: Pre-signed URL (유효기간 1시간) 또는 서버 프록시 전달
- SQL Injection 방지: ORM(SQLAlchemy) 파라미터 바인딩 사용
- Rate Limiting: 사용자당 제출 60건/시간, IP당 추천 API 100건/분

### 10.5 모니터링 및 관측성

- 각 파이프라인 단계별 처리 시간 메트릭 수집 (Prometheus)
- HTR 신뢰도 분포 대시보드 (Grafana)
- 오류율 알림: 에러율 > 1% 시 Slack/PagerDuty 알림
- 분산 트레이싱: `submission_id`를 Correlation ID로 모든 로그에 포함

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

### 12.2 통합 테스트

- 문제 추천 → 클라이언트 수신 → 캔버스 렌더링 → 제출 → HTR → 결과 반환 전체 흐름
- 다양한 필기체 스타일 샘플 (표준/비표준/어린 학생/성인) 각 50개 이상

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

### 13.3 비용 모니터링

- HTR API (MathPix 등) 호출 건수 및 비용 일별 대시보드
- LLM API 토큰 사용량 및 비용 추적
- 비용 이상 감지: 전일 대비 200% 초과 시 알림

---

## 14. 변경 이력

| 버전 | 날짜 | 변경 내용 |
|------|------|-----------|
| v1.0 | 2026-05-21 | 최초 작성 |

---

*© 2026 MathLens AI Project. All rights reserved.*
