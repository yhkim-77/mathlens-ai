# MathLens AI — 소프트웨어 요구사항 명세서 (SRS)

**Software Requirements Specification**

**문서 버전:** v1.0
**작성일:** 2026년 5월 22일
**문서 유형:** Software Requirements Specification (SRS)
**작성자:** MathLens AI 개발팀
**상태:** 초안 (Draft)

---

## 문서 개요

본 문서는 MathLens AI 프로젝트의 소프트웨어 요구사항 명세서(SRS)로서, RFP(제안요청서) 및 PRD(제품 요구사항 문서)를 기반으로 시스템의 기능적·비기능적 요구사항, 인터페이스 명세, 데이터 모델, 품질 속성을 상세히 기술합니다.

### 참조 문서

- RFP_통합본.md (v4.0, 2026-05-21)
- PRD_통합본.md (v3.0, 2026-05-21)

---

## 목차

1. [서론](#1-서론)
2. [전체 시스템 개요](#2-전체-시스템-개요)
3. [기능 요구사항](#3-기능-요구사항)
4. [외부 인터페이스 요구사항](#4-외부-인터페이스-요구사항)
5. [성능 요구사항](#5-성능-요구사항)
6. [데이터베이스 및 데이터 모델](#6-데이터베이스-및-데이터-모델)
7. [품질 속성](#7-품질-속성)
8. [보안 요구사항](#8-보안-요구사항)
9. [시스템 제약사항](#9-시스템-제약사항)
10. [검증 및 검증 기준](#10-검증-및-검증-기준)
11. [부록](#11-부록)

---

## 1. 서론

### 1.1 목적

본 SRS는 MathLens AI 시스템 개발에 필요한 모든 소프트웨어 요구사항을 명확히 정의하여 다음을 달성합니다:
- 개발팀의 구현 기준 제공
- QA 팀의 테스트 계획 수립 기반 제공
- 이해관계자 간 요구사항에 대한 공통 이해 확립
- 변경 관리 및 추적성 확보

### 1.2 범위

**제품명:** MathLens AI
**제품 유형:** 모바일 애플리케이션 (iOS/Android) + 백엔드 서비스

**주요 기능:**
- 펜 기반 손글씨 수학 풀이 입력
- AI 기반 실시간 수식 인식 (HTR)
- 풀이 과정 단계별 분석 및 오답 원인 진단
- 개인 맞춤형 개념 설명 및 피드백 제공
- 유사 문제 자동 생성 및 반복 학습 시스템
- 학습 진도 추적 및 리포트

**제외 범위:**
- 교사용 문제 출제 도구 (Phase 3)
- 학부모 대시보드 (Phase 2)
- 오프라인 AI 추론 (Phase 3)
- 실시간 협업 기능 (Phase 3)

### 1.3 정의, 약어, 축약어

| 용어 | 정의 |
|------|------|
| HTR | Handwriting Text Recognition — 손글씨 텍스트 인식 |
| iink | MyScript Interactive Ink SDK — 실시간 수식 인식 엔진 |
| LaTeX | 수학 수식 조판 언어 |
| MathML | Mathematical Markup Language — 수식 마크업 언어 |
| LLM | Large Language Model — 대규모 언어 모델 |
| CER | Character Error Rate — 문자 오류율 |
| ExpRate | Expression Rate — 수식 단위 정답률 |
| WebSocket | 양방향 실시간 통신 프로토콜 |
| JWT | JSON Web Token — 인증 토큰 |
| TTS | Text-to-Speech — 텍스트 음성 변환 |
| PKCanvasView | iOS PencilKit의 캔버스 뷰 컴포넌트 |
| Celery | Python 비동기 작업 큐 프레임워크 |

### 1.4 참조 문서

- IEEE Std 830-1998: IEEE Recommended Practice for Software Requirements Specifications
- 2022 개정 교육과정 (대한민국 교육부)
- OWASP Mobile Top 10 (2024)
- MyScript iink SDK Documentation
- MathPix API Documentation
- OpenAI GPT-4o API Documentation

---

## 2. 전체 시스템 개요

### 2.1 시스템 컨텍스트

```
┌─────────────┐
│   학습자    │ ◄──── 펜 입력, 피드백 수신
└──────┬──────┘
       │
       ▼
┌──────────────────────────────────────────────┐
│         MathLens AI 모바일 앱                 │
│  ┌─────────────┐        ┌──────────────┐    │
│  │ 펜 캔버스   │◄──────►│ iink SDK     │    │
│  │ (PencilKit) │        │ (온디바이스) │    │
│  └─────────────┘        └──────────────┘    │
└────────────────┬─────────────────────────────┘
                 │ HTTPS/WebSocket
                 ▼
┌──────────────────────────────────────────────┐
│         MathLens AI 백엔드 서비스             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │  API     │  │  AI 분석 │  │  문제    │  │
│  │  Gateway │  │  엔진    │  │  추천    │  │
│  └──────────┘  └──────────┘  └──────────┘  │
└────────┬────────────┬────────────┬──────────┘
         │            │            │
         ▼            ▼            ▼
┌────────────┐ ┌──────────┐ ┌──────────────┐
│ PostgreSQL │ │  Redis   │ │     S3       │
│    (DB)    │ │ (캐시/큐)│ │  (이미지)    │
└────────────┘ └──────────┘ └──────────────┘
                 │
                 ▼
┌────────────────────────────────────────────────┐
│         외부 서비스                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │ MathPix  │  │  GPT-4o  │  │  OAuth   │    │
│  │   API    │  │   API    │  │ Providers│    │
│  └──────────┘  └──────────┘  └──────────┘    │
└────────────────────────────────────────────────┘
```

### 2.2 주요 서브시스템

| 서브시스템 | 설명 | 플랫폼 |
|-----------|------|--------|
| 모바일 클라이언트 | 펜 입력, 수식 인식, UI/UX | iOS (Swift/SwiftUI), Android (Kotlin/Compose) |
| API Gateway | REST/WebSocket 엔드포인트 | Python FastAPI |
| HTR 서비스 | 손글씨 수식 인식 | iink SDK, MathPix API, Pix2tex |
| AI 분석 엔진 | 풀이 분석, 오답 진단 | GPT-4o / Claude 3.5 / DeepSeek-Math |
| 문제 추천 엔진 | 개인화 문제 출제 | Python (FastAPI) |
| 인증 서비스 | 사용자 인증/인가 | JWT, OAuth 2.0 |
| 데이터 레이어 | 영속성 저장 | PostgreSQL, Redis, S3 |

### 2.3 사용자 클래스 및 특성

#### 주 사용자: 학습자 (학생)

| 항목 | 내용 |
|------|------|
| 연령대 | 13~19세 (중1~고3) |
| 기술 숙련도 | 스마트폰/태블릿 사용에 익숙 |
| 주요 목표 | 수학 문제 풀이 과정에서 오류 파악 및 개념 재학습 |
| 접근 빈도 | 일 1~2회 (학습 세션당 20~40분) |
| 주요 기기 | iPad + Apple Pencil, Galaxy Tab + S-Pen |

#### 보조 사용자: 학부모 (Phase 2)

| 항목 | 내용 |
|------|------|
| 연령대 | 35~55세 |
| 기술 숙련도 | 모바일 앱 사용 가능 |
| 주요 목표 | 자녀 학습 진도 모니터링 |
| 접근 빈도 | 주 1~2회 |
| 주요 기기 | 스마트폰 (iOS/Android) |

### 2.4 운영 환경

#### 클라이언트 환경
- **iOS:** iPhone/iPad, iOS 16.0 이상
- **Android:** 스마트폰/태블릿, Android 10 (API 29) 이상
- **네트워크:** Wi-Fi 또는 LTE/5G (최소 3 Mbps)

#### 서버 환경
- **클라우드:** AWS 또는 호환 클라우드 (Multi-AZ 구성)
- **컨테이너:** Docker + ECS / Kubernetes
- **데이터베이스:** PostgreSQL 14+ (RDS Multi-AZ)
- **캐시:** Redis Cluster
- **스토리지:** S3 (AES-256 암호화)

### 2.5 설계 및 구현 제약사항

| 제약사항 | 상세 |
|---------|------|
| 프로그래밍 언어 | 백엔드: Python 3.11+, iOS: Swift 5.9+, Android: Kotlin 1.9+ |
| 프레임워크 | 백엔드: FastAPI, iOS: SwiftUI, Android: Jetpack Compose |
| 데이터베이스 | PostgreSQL (변경 불가) |
| 수식 인식 엔진 | iink SDK + MathPix Fallback (Phase 1) |
| LLM | GPT-4o / Claude 3.5 (Phase 1), 오픈소스 전환 가능 (Phase 2+) |
| 인증 방식 | JWT + OAuth 2.0 (Apple, Google, Kakao) |
| 이미지 스토리지 | S3 호환 스토리지 |

---

## 3. 기능 요구사항

### 3.1 펜 입력 및 캔버스 (FR-CANVAS)

#### FR-CANVAS-001: 펜 입력 지원

**우선순위:** P0 (필수)
**설명:** 사용자가 스타일러스 펜 또는 손가락으로 수학 풀이를 작성할 수 있는 캔버스를 제공한다.

**입력:**
- 터치 이벤트 (좌표, 필압, 타임스탬프)
- 디바이스 타입 (stylus / touch)

**처리:**
1. iOS: PKCanvasView를 사용하여 스트로크 수집
2. Android: MotionEvent를 사용하여 스트로크 수집
3. 필압 정보를 활용한 선 굵기 변화 렌더링
4. 팜 리젝션 활성화 (스타일러스 입력 시 손바닥 터치 무시)

**출력:**
- 실시간 캔버스 렌더링 (60 FPS 이상)
- 스트로크 데이터 컬렉션

**비기능 요구사항:**
- 렌더링 지연: 16ms 이하 (60 FPS)
- 입력 지연: 터치부터 화면 표시까지 10ms 이하

**수락 기준:**
- [ ] Apple Pencil/S-Pen으로 작성 시 필압에 따른 선 굵기 변화 확인
- [ ] 60 FPS 이상 렌더링 유지 (Xcode Instruments / Android Profiler 측정)
- [ ] 팜 리젝션 동작 확인 (스타일러스 입력 중 손바닥 터치 무시)

---

#### FR-CANVAS-002: 도구 모음

**우선순위:** P0 (필수)
**설명:** 펜, 지우개, 색상 선택 등의 도구를 제공한다.

**기능 요구사항:**

| 도구 | 옵션 | 기능 |
|------|------|------|
| 펜 | 굵기 3단계 (얇음/보통/굵음), 색상 5가지 (검정/파랑/빨강/초록/주황) | 기본 필기 도구 |
| 형광펜 | 굵기 1단계, 반투명 | 강조 표시 |
| 지우개 | 획 단위 지우기, 점 단위 지우기 | 오류 수정 |
| 올가미 | 영역 선택 | 선택 영역 이동/삭제 |
| 실행 취소/재실행 | 최대 50단계 | 작업 되돌리기 |
| 전체 지우기 | 확인 팝업 | 캔버스 초기화 |

**수락 기준:**
- [ ] 모든 도구가 정상 동작
- [ ] 실행 취소/재실행이 50단계까지 동작
- [ ] 전체 지우기 시 확인 팝업 표시

---

#### FR-CANVAS-003: 캔버스 조작

**우선순위:** P1 (높음)
**설명:** 사용자가 캔버스를 확대/축소하고 이동할 수 있다.

**기능:**
- 두 손가락 핀치: 확대/축소 (50% ~ 300%)
- 두 손가락 스크롤: 캔버스 이동
- Apple Pencil 더블 탭: 이전 도구 전환 (iOS)
- 줌 초기화 버튼

**수락 기준:**
- [ ] 핀치 제스처로 50%~300% 줌 동작
- [ ] 캔버스 이동이 부드럽게 동작

---

#### FR-CANVAS-004: 자동 저장

**우선순위:** P1 (높음)
**설명:** 작업 중인 풀이를 자동으로 로컬에 임시 저장한다.

**처리:**
1. 스트로크 입력 중 30초마다 로컬 저장 (UserDefaults / Room DB)
2. 앱 재시작 시 미제출 풀이 복원 여부 사용자 안내

**수락 기준:**
- [ ] 앱 종료 후 재시작 시 작업 중이던 캔버스 복원 가능

---

#### FR-CANVAS-005: 이미지 캡처 및 전처리

**우선순위:** P0 (필수)
**설명:** 캔버스를 이미지로 변환하여 서버에 전송한다.

**처리 단계:**
1. 스트로크 바운딩 박스 계산
2. 여백 추가 크롭 (±20px 패딩)
3. 해상도 표준화 (장변 1024px 기준)
4. JPEG 압축 (품질 85%, 2MB 초과 시 하향)
5. Base64 인코딩

**출력:**
- Base64 인코딩된 이미지 문자열
- 이미지 MIME 타입 (image/png 또는 image/jpeg)

**수락 기준:**
- [ ] 생성된 이미지 크기가 2MB 이하
- [ ] 이미지에 잉크 영역만 포함되고 불필요한 여백 제거됨

---

### 3.2 수식 인식 (FR-HTR)

#### FR-HTR-001: 실시간 수식 인식 (iink SDK)

**우선순위:** P0 (필수)
**설명:** 학생이 획을 그을 때마다 실시간으로 수식을 인식하여 LaTeX로 변환한다.

**입력:**
- 스트로크 데이터 (좌표, 필압, 타임스탬프)

**처리:**
1. iink SDK Math 모드로 스트로크 전달
2. 실시간 수식 인식 (< 200ms)
3. LaTeX 또는 MathML 출력

**출력:**
- 인식된 LaTeX 문자열
- 인식 신뢰도 (0.0~1.0)
- 바운딩 박스 정보

**비기능 요구사항:**
- 인식 지연: 획 입력 후 200ms 이내
- 정확도: 중·고등 수준 수식 95% 이상 (표준 필기 기준)

**수락 기준:**
- [ ] 표준 필기체로 작성한 수식 100개 중 95개 이상 정확 인식
- [ ] 인식 결과 미리보기가 200ms 이내 표시

---

#### FR-HTR-002: MathPix API Fallback

**우선순위:** P0 (필수)
**설명:** iink SDK 인식 실패 시 MathPix API로 재시도한다.

**발동 조건:**
- iink SDK 오류 코드 반환
- 인식 신뢰도 < 0.8
- 복잡한 수식으로 분류

**처리:**
1. 캔버스 이미지 PNG 변환
2. MathPix `/v3/text` API 호출
3. LaTeX 결과 반환

**비기능 요구사항:**
- 응답 시간: 3초 이내

**수락 기준:**
- [ ] iink 실패 시 자동으로 MathPix 호출
- [ ] MathPix 결과가 3초 이내 반환

---

#### FR-HTR-003: 인식 결과 수동 수정

**우선순위:** P1 (높음)
**설명:** 사용자가 인식된 LaTeX를 직접 수정할 수 있다.

**기능:**
- 인식된 LaTeX 텍스트 편집 UI
- KaTeX 실시간 미리보기
- 수정 이력 수집 (사용자 동의 시)

**수락 기준:**
- [ ] 사용자가 LaTeX 수정 후 미리보기 즉시 업데이트

---

#### FR-HTR-004: 한글/영문 주석 인식

**우선순위:** P2 (보통)
**설명:** 풀이 과정에 포함된 한글/영문 설명 텍스트를 인식한다.

**구현:**
- iOS: VNRecognizeTextRequest (Vision Framework)
- Android: Google ML Kit Text Recognition v2

**출력:**
- 인식된 텍스트를 LaTeX `\text{}` 블록으로 삽입

**수락 기준:**
- [ ] 한글 주석이 90% 이상 정확도로 인식

---

### 3.3 AI 풀이 분석 (FR-AI)

#### FR-AI-001: 비동기 처리 구조

**우선순위:** P0 (필수)
**설명:** 풀이 제출 시 즉시 응답하고 백그라운드에서 분석을 처리한다.

**처리 흐름:**
```
[POST /submissions] → 즉시 202 응답 (submission_id 반환)
        ↓
[Celery Task 생성] → Redis 큐
        ↓
[Worker 실행]
  ├── Step 1: 이미지 전처리
  ├── Step 2: HTR 실행
  ├── Step 3: LaTeX 후처리
  ├── Step 4: LLM 분석
  └── Step 5: 결과 저장 + WebSocket 푸시
```

**수락 기준:**
- [ ] 제출 후 500ms 이내 202 응답
- [ ] WebSocket으로 각 단계 상태 전달

---

#### FR-AI-002: 타임아웃 처리

**우선순위:** P0 (필수)
**설명:** 각 처리 단계에 타임아웃을 설정하고 초과 시 재시도 또는 실패 처리한다.

| 단계 | 타임아웃 | 타임아웃 시 처리 |
|------|----------|-----------------|
| 이미지 전처리 | 5초 | 원본 이미지로 HTR 진행 |
| HTR API 호출 | 10초 | 재시도 1회 후 실패 처리 |
| LLM 분석 | 30초 | 재시도 1회 후 실패 처리 |

**수락 기준:**
- [ ] 각 단계에서 타임아웃 발생 시 재시도 또는 실패 로그 기록

---

#### FR-AI-003: 풀이 단계 분해

**우선순위:** P0 (필수)
**설명:** 인식된 LaTeX 풀이를 논리적 단계로 분리한다.

**처리:**
- 등호/부등호 기준 단계 분리
- LLM 보완 (문맥 기반 단계 판별)

**출력 형식:**
```json
[
  {"step": 1, "latex": "2x + 3 = 7", "type": "equation"},
  {"step": 2, "latex": "2x = 4", "type": "equation"},
  {"step": 3, "latex": "x = 2", "type": "solution"}
]
```

**수락 기준:**
- [ ] 샘플 풀이 50개에서 평균 90% 이상 정확하게 단계 분리

---

#### FR-AI-004: 오답 유형 분류

**우선순위:** P0 (필수)
**설명:** GPT-4o에게 문제 + 풀이 + 이미지를 전달하여 오답 원인을 분류한다.

**분류 체계:**
- 개념 오류 (Conceptual Error)
  - 공식 혼동
  - 개념 미형성
  - 유사 개념 혼동
- 절차 오류 (Procedural Error)
  - 풀이 순서 오류
  - 이항 부호 실수
  - 단계 누락
- 계산 실수 (Computational Error)
  - 산술 계산 오류
  - 분수/소수 처리 실수
- 문제 이해 오류 (Comprehension Error)
  - 조건 미반영
  - 구하는 것 오해

**출력 형식:**
```json
{
  "error_type": "procedural",
  "error_subtype": "sign_error",
  "error_step": 2,
  "confidence": 0.92
}
```

**비기능 요구사항:**
- 정확도: 전문 교사 레이블 대비 90% 일치

**수락 기준:**
- [ ] 테스트셋 100문항에서 90% 이상 정확도 달성

---

#### FR-AI-005: 피드백 문장 생성

**우선순위:** P0 (필수)
**설명:** 오류 유형 및 학년 수준에 맞는 한국어 피드백을 생성한다.

**입력:**
- 오류 유형
- 관련 개념 ID
- 학습자 학년
- 이전 오답 이력

**출력:**
- 설명 텍스트 (500자 이내)
- 관련 공식 LaTeX
- 예제 풀이 LaTeX

**수락 기준:**
- [ ] 생성된 피드백이 학년 수준에 맞는 어휘로 작성됨
- [ ] 관련 공식 및 예제가 포함됨

---

#### FR-AI-006: LLM 입력 구성

**우선순위:** P0 (필수)
**설명:** LLM API 호출 시 필요한 프롬프트를 구성한다.

**프롬프트 구조:**
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

**수락 기준:**
- [ ] 프롬프트에 문제, 풀이, 이미지가 모두 포함됨

---

#### FR-AI-007: LaTeX 후처리 및 정답 판별

**우선순위:** P0 (필수)
**설명:** SymPy를 사용하여 학생 답안과 정답의 수학적 동치 여부를 판별한다.

**구현:**
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

**수락 기준:**
- [ ] 동치 판별 정확도 99% 이상 (샘플 100쌍 기준)

---

#### FR-AI-008: 유사 문제 생성

**우선순위:** P0 (필수)
**설명:** 오답 문제와 동일 개념이지만 숫자/조건이 다른 문제를 생성한다.

**구현:**
- GPT-4o + 수학 문제 템플릿 엔진
- 2022 개정 교육과정 범위 내로 제한
- 생성 문제 유효성 검사 (SymPy 파싱)

**수락 기준:**
- [ ] 생성된 문제가 원본과 동일 개념 태그를 갖는다
- [ ] 생성된 문제의 LaTeX가 유효하다 (SymPy 파싱 성공)

---

#### FR-AI-009: 오개념 추론

**우선순위:** P1 (높음)
**설명:** 학생이 무엇을 이해하지 못했는지 근본 원인을 추론한다.

**구성 요소:**
- 오개념 패턴 DB (분수 연산, 지수 법칙, 인수분해 등)
- 패턴 매칭 엔진 (코사인 유사도 또는 임베딩 거리)
- LLM 보완 추론 (패턴 DB에 없는 경우)
- 신뢰도 점수 (0.0~1.0)

**수락 기준:**
- [ ] 오개념 패턴 DB에 최소 50개 패턴 등록
- [ ] 신뢰도 점수가 포함된 추론 결과 반환

---

### 3.4 맞춤형 피드백 화면 (FR-FEEDBACK)

#### FR-FEEDBACK-001: 오류 위치 하이라이팅

**우선순위:** P0 (필수)
**설명:** 틀린 단계를 원본 캔버스 이미지 위에 오버레이로 표시한다.

**구현:**
- AI가 반환한 `error_step` 기반 빨간 테두리 표시
- 바운딩 박스 좌표 활용 (iink / MathPix 반환값)

**수락 기준:**
- [ ] 오류 단계가 시각적으로 명확히 표시됨

---

#### FR-FEEDBACK-002: 개념 설명 카드

**우선순위:** P0 (필수)
**설명:** 오류 유형, AI 설명, 관련 공식, 예제를 카드 형태로 제공한다.

**구성:**
- 오류 유형 배지 (색상 코딩)
- AI 생성 설명 텍스트
- 관련 공식 (KaTeX 렌더링)
- 핵심 예제 2개 (접이식 펼침)
- TTS 버튼

**수락 기준:**
- [ ] 모든 구성 요소가 카드에 표시됨
- [ ] TTS 버튼 클릭 시 음성 재생

---

#### FR-FEEDBACK-003: 정석 풀이 제시

**우선순위:** P1 (높음)
**설명:** 올바른 풀이 단계를 순차적으로 표시한다.

**구현:**
- 단계별 페이드인 애니메이션
- 각 단계에 설명 툴팁 옵션

**수락 기준:**
- [ ] 정석 풀이가 단계별로 표시됨

---

#### FR-FEEDBACK-004: 다음 행동 버튼

**우선순위:** P0 (필수)
**설명:** 사용자의 다음 행동을 유도하는 버튼을 제공한다.

| 버튼 | 동작 |
|------|------|
| 다시 풀기 | 동일 문제 캔버스 초기화 |
| 유사 문제 | AI 생성 유사 문제로 이동 |
| 개념 더 보기 | 개념 상세 화면으로 이동 |
| 넘어가기 | 다음 문제로 이동 |

**수락 기준:**
- [ ] 모든 버튼이 정상 동작

---

#### FR-FEEDBACK-005: TTS (음성 설명)

**우선순위:** P2 (보통)
**설명:** AI 생성 설명을 한국어 음성으로 읽어준다.

**구현:**
- iOS: AVSpeechSynthesizer
- Android: Android TextToSpeech
- 재생/일시정지, 속도 조절 (0.8x, 1.0x, 1.2x, 1.5x)
- 텍스트 하이라이팅 (재생 중인 문장 표시)

**수락 기준:**
- [ ] TTS 재생이 정상 동작
- [ ] 속도 조절이 가능

---

### 3.5 반복 학습 시스템 (FR-REPEAT)

#### FR-REPEAT-001: 완전 학습 판별

**우선순위:** P0 (필수)
**설명:** 동일 개념 유형 연속 3회 정답 시 습득 완료 처리한다.

**처리:**
- 습득 완료 시 배지 애니메이션 표시
- `concept_mastery` 테이블에 상태 업데이트

**수락 기준:**
- [ ] 연속 3회 정답 시 습득 완료 배지 표시

---

#### FR-REPEAT-002: 간격 반복 복습 스케줄

**우선순위:** P1 (높음)
**설명:** 에빙하우스 망각 곡선 기반 복습 일정을 생성한다.

| 복습 간격 | 기준 |
|-----------|------|
| 1일 후 | 첫 번째 습득 후 |
| 3일 후 | 두 번째 복습 성공 후 |
| 7일 후 | 세 번째 복습 성공 후 |
| 14일, 30일... | 지수적 간격 증가 |

**수락 기준:**
- [ ] 복습 일정이 `concept_mastery` 테이블에 기록됨

---

#### FR-REPEAT-003: 오답 노트 자동 생성

**우선순위:** P1 (높음)
**설명:** 틀린 문제를 자동으로 저장하고 관리한다.

**기능:**
- 문제 이미지 + 오류 유형 + AI 설명 저장
- 오답 노트 필터 (날짜별, 오류 유형별, 개념별)
- PDF/이미지 내보내기

**수락 기준:**
- [ ] 오답 문제가 자동으로 오답 노트에 저장됨
- [ ] 필터링 기능 동작

---

### 3.6 문제 입력 및 문제은행 (FR-PROBLEM)

#### FR-PROBLEM-001: 카메라 촬영 입력

**우선순위:** P0 (필수)
**설명:** 교재/시험지를 카메라로 촬영하여 문제를 인식한다.

**구현:**
- 촬영 이미지 → MathPix API `/v3/text` 호출
- 문제 LaTeX 추출
- 자르기 가이드 제공

**비기능 요구사항:**
- 인식 정확도: 표준 교재 인쇄체 90% 이상

**수락 기준:**
- [ ] 교과서 문제 20개 촬영 시 18개 이상 정확 인식

---

#### FR-PROBLEM-002: 앱 내 문제은행

**우선순위:** P0 (필수)
**설명:** 과목/단원/난이도별 문제를 제공한다.

**기능:**
- 과목 필터 (대수, 기하, 미적분, 확률통계)
- 단원 필터 (2022 개정 교육과정 기준)
- 난이도 필터 (1~5)
- 즐겨찾기, 최근 푼 문제

**초기 문제 수:**
- 중학교: 3,000문항 이상
- 고등학교: 8,000문항 이상
- **합계: 11,000문항 이상**

**수락 기준:**
- [ ] 문제은행에 11,000문항 이상 등록
- [ ] 필터링 기능 동작

---

#### FR-PROBLEM-003: 직접 입력

**우선순위:** P2 (보통)
**설명:** 수식 에디터로 문제를 직접 작성한다.

**구현:**
- 가상 수학 키보드 (분수, 루트, 적분 기호 버튼)
- LaTeX 직접 입력 모드

**수락 기준:**
- [ ] 수식 에디터로 문제 작성 가능

---

#### FR-PROBLEM-004: 개인화 문제 추천

**우선순위:** P0 (필수)
**설명:** 학습자의 이력을 분석하여 맞춤형 문제를 추천한다.

**입력 데이터:**
- 사용자 학년
- 최근 오답 개념 태그 (최근 30일)
- 개념별 정답률
- 직전 연속 정답 횟수
- 당일 이미 출제된 문제 ID 목록
- 취약/강점 개념 비율

**처리:**
- 오답 개념 우선 출제 (가중치 70%)
- 난이도 자동 상향 (연속 3회 정답 시 +1)
- 당일 중복 제외
- 취약:강점 = 7:3 비율 유지

**수락 기준:**
- [ ] 오답 개념이 우선 출제됨
- [ ] 연속 3회 정답 시 난이도 상승 확인

---

#### FR-PROBLEM-005: 문제은행 관리

**우선순위:** P1 (높음)
**설명:** 문제 상태를 관리한다.

**상태:**
- `draft` → `review` → `active` → `archived`

**규칙:**
- `active` 상태 문제만 학습자에게 출제
- 문제 수정 시 이전 버전 보존
- 각 문제에 `concept_tags` 및 `error_type_tags` 필수

**수락 기준:**
- [ ] 문제 상태 전환 동작 확인

---

### 3.7 학습 리포트 및 대시보드 (FR-REPORT)

#### FR-REPORT-001: 학생 대시보드 (홈 화면)

**우선순위:** P0 (필수)
**설명:** 학습 현황을 한눈에 보여주는 홈 화면을 제공한다.

**구성:**
- 오늘의 학습 목표 (문제 수) 및 달성 현황
- 최근 7일 연속 학습일 (스트릭)
- 취약 개념 TOP 3
- 추천 복습 문제 카드

**수락 기준:**
- [ ] 모든 구성 요소가 홈 화면에 표시됨

---

#### FR-REPORT-002: 주간/월간 리포트

**우선순위:** P1 (높음)
**설명:** 학습 통계를 시각화하여 제공한다.

**구성:**
- 풀이 문제 수, 정답률, 학습 시간 추이 그래프
- 오답 유형 분포 파이 차트
- 개념별 습득 현황 히트맵

**수락 기준:**
- [ ] 그래프 및 차트가 정확하게 표시됨

---

#### FR-REPORT-003: 개념 맵 (Phase 2)

**우선순위:** P3 (낮음)
**설명:** 교육과정 개념 간 선후관계를 시각화한다.

**구현:**
- 습득/미습득/취약 개념 색상 구분

**수락 기준:**
- [ ] 개념 맵이 그래프 형태로 표시됨

---

### 3.8 계정 및 인증 (FR-AUTH)

#### FR-AUTH-001: 소셜 로그인

**우선순위:** P0 (필수)
**설명:** Apple, Google, Kakao 소셜 로그인을 제공한다.

| 제공자 | 플랫폼 |
|--------|--------|
| Apple Login | iOS 필수 |
| Google Login | iOS + Android |
| Kakao Login | iOS + Android |

**수락 기준:**
- [ ] 3종 소셜 로그인 모두 정상 동작

---

#### FR-AUTH-002: 프로필 설정

**우선순위:** P0 (필수)
**설명:** 사용자 정보를 설정한다.

**설정 항목:**
- 학년 (중1 ~ 고3 / 재수생 / 기타)
- 일일 학습 목표 (문제 수)
- 알림 설정

**수락 기준:**
- [ ] 프로필 설정 저장 및 조회 가능

---

#### FR-AUTH-003: 학부모 연동 (Phase 2)

**우선순위:** P3 (낮음)
**설명:** QR 코드 또는 초대 코드로 자녀 계정을 연동한다.

**권한:**
- 학부모 계정: 조회 전용

**수락 기준:**
- [ ] QR 코드로 계정 연동 가능

---

## 4. 외부 인터페이스 요구사항

### 4.1 사용자 인터페이스

#### UI-001: 모바일 앱 화면 구성

**주요 화면:**

1. **홈 대시보드**
   - 학습 현황 요약
   - 추천 문제 카드
   - 스트릭 표시

2. **문제 선택 화면**
   - 문제은행 브라우징
   - 과목/단원/난이도 필터

3. **풀이 화면 (핵심)**
   - 상단: 문제 표시 영역
   - 하단: 펜 캔버스
   - 우측: 실시간 수식 미리보기
   - 하단: 도구 모음 및 제출 버튼

4. **분석 중 로딩 화면**
   - 처리 단계별 프로그레스 표시
   - WebSocket 상태 메시지 표시

5. **인식 결과 확인 화면**
   - iink 인식 LaTeX 표시
   - 수정 UI

6. **AI 피드백 화면**
   - 오류 하이라이팅
   - 개념 설명 카드
   - TTS 재생 버튼
   - 다음 행동 버튼

7. **학습 리포트 화면**
   - 주간/월간 그래프
   - 오답 분포
   - 개념 맵

**접근성 요구사항:**
- 다크모드 지원
- 글자 크기 조절 (시스템 Dynamic Type 연동)
- 고대비 모드 지원
- VoiceOver / TalkBack 핵심 UI 지원

---

### 4.2 하드웨어 인터페이스

#### HW-001: 터치 입력 장치

**지원 장치:**
- Apple Pencil 1세대, 2세대
- Samsung S-Pen
- USI 펜
- 일반 스타일러스
- 손가락 터치

**요구사항:**
- 필압 감지 (스타일러스 펜)
- 팜 리젝션
- 더블 탭 제스처 (Apple Pencil 2세대)

---

#### HW-002: 카메라

**용도:** 문제 촬영 입력

**요구사항:**
- 최소 800만 화소
- 자동 초점
- 플래시 지원 (옵션)

---

### 4.3 소프트웨어 인터페이스

#### SW-001: MyScript iink SDK

**버전:** 최신 안정 버전
**플랫폼:** iOS, Android
**인터페이스:**
- 입력: 스트로크 데이터 (좌표, 필압, 타임스탬프)
- 출력: LaTeX, MathML, 신뢰도

---

#### SW-002: MathPix OCR API

**엔드포인트:** `https://api.mathpix.com/v3/text`
**인증:** API Key (헤더 `app_id`, `app_key`)
**인터페이스:**
- 입력: Base64 이미지
- 출력: LaTeX, 신뢰도

---

#### SW-003: OpenAI GPT-4o API

**엔드포인트:** `https://api.openai.com/v1/chat/completions`
**인증:** Bearer Token
**인터페이스:**
- 입력: 멀티모달 (텍스트 + 이미지)
- 출력: JSON 응답 (오류 분류, 피드백 텍스트)

---

#### SW-004: OAuth 제공자

**제공자:**
- Apple Sign In
- Google Sign In
- Kakao Login

**인터페이스:**
- 입력: Authorization Code
- 출력: ID Token, Access Token

---

### 4.4 통신 인터페이스

#### COM-001: HTTPS API

**프로토콜:** HTTPS (TLS 1.3)
**포맷:** JSON
**인증:** JWT (Bearer Token)

**주요 엔드포인트:**
```
GET  /api/v1/problems/recommend
POST /api/v1/problems/generate
POST /api/v1/submissions
GET  /api/v1/submissions/{id}/status
GET  /api/v1/results/{id}
GET  /api/v1/users/{id}/report
```

---

#### COM-002: WebSocket

**프로토콜:** WSS (WebSocket Secure)
**용도:** 실시간 처리 상태 전달
**엔드포인트:** `wss://api.mathlens.ai/ws/v1/submissions/{submission_id}`

**메시지 형식:**
```json
{
  "stage": "htr_done",
  "latex_preview": "2x + 3 = 7",
  "confidence": 0.96,
  "ts": "2026-05-22T10:00:00Z"
}
```

---

## 5. 성능 요구사항

### 5.1 응답 시간

| 지표 | 요구 수준 | 측정 기준 |
|------|-----------|-----------|
| 캔버스 렌더링 프레임 속도 | ≥ 60 FPS | 16ms 이하/프레임 |
| 스트로크 입력 지연 | ≤ 10ms | 터치부터 화면 표시까지 |
| 수식 인식 미리보기 지연 | ≤ 200ms | 획 입력 후 (iink SDK) |
| 풀이 제출 접수 응답 | ≤ 500ms | P99 기준 |
| HTR 처리 시간 | ≤ 4,000ms | P95 기준 (서버) |
| 전체 파이프라인 완료 | ≤ 10,000ms | P95 기준 |
| 문제 추천 API 응답 | ≤ 1,000ms | P99 기준 |
| 앱 콜드 스타트 | ≤ 3초 | iOS/Android |

### 5.2 처리량

| 지표 | 요구 수준 |
|------|-----------|
| 동시 접속자 (CCU) | 1,000 이상 |
| 동시 처리 제출 수 | 500건/분 이상 |
| API 서버 처리량 | 10,000 req/min |

### 5.3 용량

| 항목 | 요구 수준 |
|------|-----------|
| 사용자 수 | 100,000 명 (Phase 1) |
| 문제은행 크기 | 11,000 문항 초기, 50,000 문항 확장 |
| 제출 이미지 저장 | 무제한 (S3) |
| 데이터베이스 크기 | 500 GB (초기) |

### 5.4 앱 크기

| 플랫폼 | 최대 크기 |
|--------|----------|
| iOS | 200 MB 이하 |
| Android | 150 MB 이하 |

---

## 6. 데이터베이스 및 데이터 모델

### 6.1 논리적 데이터 모델

#### 6.1.1 사용자 (users)

| 컬럼명 | 타입 | 제약조건 | 설명 |
|--------|------|----------|------|
| id | UUID | PK | 사용자 고유 ID |
| email | VARCHAR(255) | UNIQUE | 이메일 (소셜 로그인) |
| grade | VARCHAR(20) | NOT NULL | 학년 (middle_1 ~ high_3, reexaminee) |
| created_at | TIMESTAMP | NOT NULL | 가입일 |
| last_active_at | TIMESTAMP | NULL | 마지막 활동 일시 |

**인덱스:**
- PRIMARY KEY (id)
- UNIQUE INDEX (email)

---

#### 6.1.2 문제 (problems)

| 컬럼명 | 타입 | 제약조건 | 설명 |
|--------|------|----------|------|
| id | UUID | PK | 문제 고유 ID |
| title | VARCHAR(255) | NULL | 문제 제목 |
| content_text | TEXT | NOT NULL | 문제 본문 (LaTeX 포함) |
| content_image_key | TEXT | NULL | S3 이미지 키 |
| answer_latex | TEXT | NULL | 정답 (LaTeX) |
| solution_steps | JSONB | NULL | 모범 풀이 단계 |
| subject | VARCHAR(50) | NOT NULL | 과목 (algebra, geometry, calculus, statistics) |
| grade | VARCHAR(20) | NOT NULL | 학년 |
| difficulty | SMALLINT | NOT NULL | 난이도 (1~5) |
| concept_tags | TEXT[] | NULL | 개념 태그 배열 |
| error_type_tags | TEXT[] | NULL | 오류 유형 태그 배열 |
| curriculum_code | VARCHAR(50) | NULL | 교육과정 코드 |
| source | VARCHAR(50) | NOT NULL | 출처 (bank, llm_generated, textbook) |
| status | VARCHAR(20) | NOT NULL | 상태 (draft, review, active, archived) |
| created_at | TIMESTAMP | NOT NULL | 생성일 |
| updated_at | TIMESTAMP | NOT NULL | 수정일 |

**인덱스:**
- PRIMARY KEY (id)
- INDEX (grade, subject, difficulty, status)
- GIN INDEX (concept_tags)

---

#### 6.1.3 제출 (submissions)

| 컬럼명 | 타입 | 제약조건 | 설명 |
|--------|------|----------|------|
| id | UUID | PK | 제출 고유 ID |
| user_id | UUID | FK → users(id) | 사용자 ID |
| problem_id | UUID | FK → problems(id) | 문제 ID |
| session_id | UUID | NULL | 세션 ID |
| image_s3_key | TEXT | NULL | S3 이미지 키 |
| stroke_metadata | JSONB | NULL | 스트로크 메타데이터 |
| device_info | JSONB | NULL | 디바이스 정보 |
| status | VARCHAR(20) | NOT NULL | 상태 (received, processing, completed, failed) |
| submitted_at | TIMESTAMP | NOT NULL | 제출일시 |
| processed_at | TIMESTAMP | NULL | 처리완료일시 |

**인덱스:**
- PRIMARY KEY (id)
- INDEX (user_id, submitted_at)
- FOREIGN KEY (user_id) REFERENCES users(id)
- FOREIGN KEY (problem_id) REFERENCES problems(id)

---

#### 6.1.4 인식 결과 (recognition_results)

| 컬럼명 | 타입 | 제약조건 | 설명 |
|--------|------|----------|------|
| id | UUID | PK | 결과 고유 ID |
| submission_id | UUID | FK → submissions(id) UNIQUE | 제출 ID |
| htr_raw_latex | TEXT | NULL | HTR 원본 LaTeX |
| htr_steps | JSONB | NULL | HTR 단계별 결과 |
| htr_confidence | FLOAT | NULL | HTR 신뢰도 (0.0~1.0) |
| is_correct | BOOLEAN | NULL | 정답 여부 |
| error_type | VARCHAR(50) | NULL | 오류 유형 |
| error_subtype | VARCHAR(50) | NULL | 오류 세부 유형 |
| error_step | SMALLINT | NULL | 오류 발생 단계 |
| error_steps | JSONB | NULL | 오류 단계 상세 |
| feedback_text | TEXT | NULL | 피드백 텍스트 |
| correct_solution_latex | TEXT | NULL | 정석 풀이 LaTeX |
| concept_tags_inferred | TEXT[] | NULL | 추론된 개념 태그 |
| llm_model_version | VARCHAR(50) | NULL | LLM 모델 버전 |
| prompt_template_id | UUID | NULL | 프롬프트 템플릿 ID |
| confidence | FLOAT | NULL | 분석 신뢰도 |
| created_at | TIMESTAMP | NOT NULL | 생성일 |

**인덱스:**
- PRIMARY KEY (id)
- UNIQUE INDEX (submission_id)
- FOREIGN KEY (submission_id) REFERENCES submissions(id)

---

#### 6.1.5 개념 습득 현황 (concept_mastery)

| 컬럼명 | 타입 | 제약조건 | 설명 |
|--------|------|----------|------|
| id | UUID | PK | 습득 현황 고유 ID |
| user_id | UUID | FK → users(id) | 사용자 ID |
| concept_id | UUID | NOT NULL | 개념 ID |
| status | VARCHAR(20) | NOT NULL | 상태 (learning, mastered, review_due) |
| consecutive_correct | SMALLINT | NOT NULL | 연속 정답 횟수 |
| next_review_at | TIMESTAMP | NULL | 다음 복습 일시 |
| updated_at | TIMESTAMP | NOT NULL | 수정일 |

**인덱스:**
- PRIMARY KEY (id)
- INDEX (user_id, status, next_review_at)
- FOREIGN KEY (user_id) REFERENCES users(id)

---

#### 6.1.6 사용자 문제 이력 (user_problem_history)

| 컬럼명 | 타입 | 제약조건 | 설명 |
|--------|------|----------|------|
| id | UUID | PK | 이력 고유 ID |
| user_id | UUID | FK → users(id) | 사용자 ID |
| problem_id | UUID | FK → problems(id) | 문제 ID |
| submission_id | UUID | FK → submissions(id) | 제출 ID |
| is_correct | BOOLEAN | NOT NULL | 정답 여부 |
| error_type | VARCHAR(50) | NULL | 오류 유형 |
| solved_at | TIMESTAMP | NOT NULL | 풀이일시 |

**인덱스:**
- PRIMARY KEY (id)
- INDEX (user_id, problem_id)
- INDEX (user_id, error_type, solved_at)
- FOREIGN KEY (user_id) REFERENCES users(id)
- FOREIGN KEY (problem_id) REFERENCES problems(id)
- FOREIGN KEY (submission_id) REFERENCES submissions(id)

---

### 6.2 물리적 데이터베이스 설계

**DBMS:** PostgreSQL 14+
**인스턴스:** RDS Multi-AZ (Primary + Standby)
**스토리지:** 500 GB SSD (초기), Auto Scaling 활성화
**백업:** 자동 백업 (일 1회, 7일 보관)

---

## 7. 품질 속성

### 7.1 신뢰성 (Reliability)

| 지표 | 요구 수준 |
|------|-----------|
| 서비스 가용성 | 99.5% 이상 (월 기준) |
| 크래시율 | 0.1% 이하 |
| API 에러율 | 1% 이하 |

**Fallback 전략:**
- MathPix API 다운 시 → Pix2tex 자체 서버
- GPT-4o API 다운 시 → Claude API → DeepSeek-Math
- WebSocket 연결 실패 시 → HTTP 폴링

**재시도 정책:**
- Celery Worker 장애 시 최대 3회 재시도 (exponential backoff)

---

### 7.2 확장성 (Scalability)

**수평 확장:**
- API 서버: ECS Auto Scaling (CPU > 70% 시 스케일 아웃)
- Celery Worker: 큐 길이 기반 Auto Scaling

**데이터 확장:**
- PostgreSQL: Read Replica 추가 (읽기 부하 분산)
- S3: 무제한 확장 (자동)

---

### 7.3 유지보수성 (Maintainability)

**코드 품질:**
- 백엔드: Python 타입 힌트 100% 적용
- 유닛 테스트 커버리지: 80% 이상
- API 문서: OpenAPI 3.0 자동 생성 (FastAPI)

**모니터링:**
- 로그: 구조화된 JSON 로그 (ELK Stack)
- 메트릭: Prometheus + Grafana
- 에러 트래킹: Sentry

---

### 7.4 사용성 (Usability)

**학습 곡선:**
- 신규 사용자가 5분 이내에 첫 문제 풀이 완료 가능

**도움말:**
- 인앱 온보딩 튜토리얼 (첫 실행 시)
- 컨텍스트 기반 툴팁

---

### 7.5 이식성 (Portability)

**지원 플랫폼:**
- iOS 16.0 ~ 최신
- Android 10 (API 29) ~ 최신

**백엔드 이식성:**
- Docker 컨테이너 기반 (클라우드 독립적)

---

## 8. 보안 요구사항

### 8.1 인증 및 인가

**인증 방식:**
- JWT (Access Token 1시간, Refresh Token 30일)
- OAuth 2.0 (Apple, Google, Kakao)

**권한 관리:**
- 학습자: 자신의 데이터만 접근
- 학부모: 연동된 자녀 데이터 읽기 전용 (Phase 2)

---

### 8.2 데이터 보호

**전송 암호화:**
- TLS 1.3 (HTTPS, WSS)

**저장 암호화:**
- S3: AES-256 서버 측 암호화
- PostgreSQL: 데이터베이스 암호화 (RDS)

**개인정보 보호:**
- 미성년자 개인정보 수집 최소화
- 법정대리인 동의 프로세스 (만 14세 미만)
- 풀이 이미지: 분석 후 30일 경과 시 자동 삭제 (설정 가능)

---

### 8.3 입력 검증

**SQL Injection 방지:**
- ORM 파라미터 바인딩 (SQLAlchemy)

**XSS 방지:**
- 사용자 입력 이스케이프 처리
- Content Security Policy 설정

---

### 8.4 Rate Limiting

| 대상 | 제한 |
|------|------|
| 사용자당 제출 | 60건/시간 |
| IP당 추천 API | 100건/분 |

---

### 8.5 보안 감사

**기준:**
- OWASP Mobile Top 10 (2024)
- OWASP API Security Top 10

**검증:**
- Phase 1 출시 전 보안 취약점 스캔 (High/Critical 0건)

---

## 9. 시스템 제약사항

### 9.1 기술 제약사항

| 항목 | 제약 |
|------|------|
| 프로그래밍 언어 | 백엔드: Python 3.11+, iOS: Swift 5.9+, Android: Kotlin 1.9+ |
| 프레임워크 | 백엔드: FastAPI, iOS: SwiftUI, Android: Jetpack Compose |
| 데이터베이스 | PostgreSQL (변경 불가) |
| 캐시/큐 | Redis (변경 불가) |
| 이미지 스토리지 | S3 호환 (변경 불가) |

---

### 9.2 외부 의존성

| 서비스 | 용도 | 대체 방안 |
|--------|------|-----------|
| MyScript iink SDK | 실시간 수식 인식 | WebView 기반 iink JS |
| MathPix API | Fallback 수식 인식 | Pix2tex 자체 호스팅 |
| OpenAI GPT-4o | AI 분석 | Claude 3.5 / DeepSeek-Math |

---

### 9.3 규정 준수

**교육과정:**
- 2022 개정 교육과정 (대한민국 교육부) 준수

**법규:**
- 개인정보보호법 (대한민국)
- 정보통신망법 (대한민국)
- 아동·청소년의 성보호에 관한 법률

**앱스토어 정책:**
- Apple App Store Review Guidelines
- Google Play Developer Policy

---

## 10. 검증 및 검증 기준

### 10.1 단위 테스트

**대상 모듈:**
- 문제 추천 엔진
- LaTeX 파서
- 이미지 전처리
- 정답 동치 판별 (SymPy)
- 오류 분류기

**커버리지:**
- 80% 이상

---

### 10.2 통합 테스트

**시나리오:**
- 문제 추천 → 풀이 제출 → HTR → AI 분석 → 결과 반환 전체 흐름
- Fallback 시나리오 (iink → MathPix → GPT-4o Vision)

---

### 10.3 성능 테스트

**도구:**
- k6 또는 Locust

**시나리오:**
- 동시 500건 제출 처리
- HTR API 응답 시간 p50/p95/p99 측정
- 24시간 연속 부하 (메모리 누수 검증)

---

### 10.4 HTR 정확도 테스트

**데이터셋:**

| 유형 | 샘플 수 | 기준 |
|------|---------|------|
| 중학 수준 수식 (표준 필기) | 200 | CER ≤ 5% |
| 고등 수준 수식 (표준 필기) | 200 | CER ≤ 5% |
| 비표준 필기 (성인) | 100 | CER ≤ 15% |
| 혼합 (수식 + 한글) | 100 | 단어 정확도 ≥ 90% |

---

### 10.5 사용자 수용 테스트

**알파 테스트:**
- 내부 테스터 20명 이상
- 크리티컬/블로킹 버그 0건
- 크래시율 < 0.1%

**베타 테스트:**
- 실사용자 100명 이상
- D7 Retention ≥ 40%
- NPS ≥ 30

---

## 11. 부록

### 11.1 용어집

| 용어 | 정의 |
|------|------|
| HTR | Handwriting Text Recognition — 손글씨 텍스트 인식 |
| LaTeX | 수학 수식 조판 언어 |
| iink | MyScript Interactive Ink SDK |
| CER | Character Error Rate — 문자 오류율 |
| ExpRate | Expression Rate — 수식 단위 정답률 |
| LLM | Large Language Model — 대규모 언어 모델 |

---

### 11.2 약어 목록

| 약어 | 전체 명칭 |
|------|-----------|
| API | Application Programming Interface |
| AWS | Amazon Web Services |
| CCU | Concurrent Users |
| CI/CD | Continuous Integration / Continuous Deployment |
| ECS | Elastic Container Service |
| JWT | JSON Web Token |
| KPI | Key Performance Indicator |
| NPS | Net Promoter Score |
| OAuth | Open Authorization |
| ORM | Object-Relational Mapping |
| P95 | 95th Percentile |
| RDS | Relational Database Service |
| REST | Representational State Transfer |
| S3 | Simple Storage Service |
| SDK | Software Development Kit |
| SQL | Structured Query Language |
| TLS | Transport Layer Security |
| TTS | Text-to-Speech |
| UI | User Interface |
| UX | User Experience |
| WS | WebSocket |

---

### 11.3 참조 표준

- IEEE Std 830-1998: IEEE Recommended Practice for Software Requirements Specifications
- ISO/IEC 25010:2011: Systems and software Quality Requirements and Evaluation (SQuaRE)
- OWASP Mobile Top 10 (2024)
- OWASP API Security Top 10
- 2022 개정 교육과정 (대한민국 교육부)

---

### 11.4 문서 개정 이력

| 버전 | 날짜 | 변경 내용 | 작성자 |
|------|------|-----------|--------|
| v1.0 | 2026-05-22 | 최초 작성 — RFP v4.0, PRD v3.0 기반 SRS 전면 작성 | MathLens AI 개발팀 |

---

*본 문서는 내부 참고용입니다.*

*© 2026 MathLens AI Project. All rights reserved.*
