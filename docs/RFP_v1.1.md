# 수학 풀이 인식 기반 AI 튜터 앱 — 프로젝트 개요 및 RFP

**문서 버전:** v1.1  
**작성일:** 2026년 5월 21일  
**문서 유형:** 제안요청서 (Request for Proposal)  
**변경 이력:** v1.1 — 손글씨 인식 기술 상세 챕터 추가 (섹션 6)

---

## 목차

1. [프로젝트 개요](#1-프로젝트-개요)
2. [배경 및 목적](#2-배경-및-목적)
3. [핵심 기능 요구사항](#3-핵심-기능-요구사항)
4. [시스템 아키텍처](#4-시스템-아키텍처)
5. [기술 스택 요구사항](#5-기술-스택-요구사항)
6. [손글씨 인식 기술 상세 요구사항](#6-손글씨-인식-기술-상세-요구사항) ← NEW
7. [UX/UI 설계 방향](#7-uxui-설계-방향)
8. [개발 범위 및 단계](#8-개발-범위-및-단계)
9. [일정 계획](#9-일정-계획)
10. [예산 및 산출 기준](#10-예산-및-산출-기준)
11. [제안사 자격 요건](#11-제안사-자격-요건)
12. [제안서 제출 요건](#12-제안서-제출-요건)
13. [평가 기준](#13-평가-기준)
14. [부록](#14-부록)

---

## 1. 프로젝트 개요

### 1.1 프로젝트명

**MathLens AI** — 손글씨 수학 풀이 인식 기반 개인 맞춤형 AI 수학 튜터 모바일 애플리케이션

### 1.2 플랫폼

- iOS (iPhone, iPad) — iOS 16.0 이상
- Android — Android 10 (API Level 29) 이상

### 1.3 핵심 가치 제안

| 구분 | 설명 |
|------|------|
| 풀이 인식 | 사용자가 펜 또는 손가락으로 입력한 수학 풀이 과정을 실시간 인식 |
| 개념 이해도 추론 | 인식된 풀이에서 학습자가 올바른 개념을 이해하고 있는지 AI가 판단 |
| 오답 원인 분석 | 단순 정오 여부가 아닌 오답의 근본 원인(개념 오류, 계산 실수 등)을 추론 |
| 맞춤 설명 | 오답 유형에 따른 개인화된 개념 재설명 제공 |
| 반복 학습 | 동일 유형의 문제를 재출제하여 완전 학습(Mastery Learning) 유도 |

---

## 2. 배경 및 목적

### 2.1 시장 배경

- 국내 에듀테크 시장은 2024년 약 7조 원 규모로 매년 15% 이상 성장 중
- 수학은 학습 격차가 가장 크게 발생하는 과목으로, AI 기반 개인 맞춤 학습 수요 급증
- 기존 수학 앱은 정답 여부만 판별하며, **풀이 과정 분석 기반 피드백**은 시장 내 미충족 영역
- 손글씨 인식 기술(HTR, Handwritten Text Recognition)과 멀티모달 LLM의 발전으로 구현 가능성 확보

### 2.2 프로젝트 목적

1. 학습자가 종이에 쓰듯 자연스럽게 스마트 기기 위에서 수학 풀이를 작성
2. AI가 풀이 과정을 단계별로 분석하여 **어느 단계에서 어떤 개념이 틀렸는지** 진단
3. 학습자의 오개념을 정확히 짚어주는 **맞춤형 개념 설명** 제공
4. 같은 유형의 문제를 반복 출제하여 **완전 학습** 달성

### 2.3 타깃 사용자

| 타깃 | 세부 내용 |
|------|-----------|
| 주요 타깃 | 중학교 1학년 ~ 고등학교 3학년 (13~19세) |
| 보조 타깃 | 수능 재수생, 대학 기초 수학 수강생 |
| 보호자 | 학습 현황 모니터링을 원하는 학부모 |

---

## 3. 핵심 기능 요구사항

### 3.1 펜 입력 및 손글씨 인식 (Handwriting Recognition)

#### 3.1.1 입력 방식
- 스타일러스 펜 (Apple Pencil, S-Pen 등) 및 손가락 터치 모두 지원
- 실시간 잉크 렌더링: 필압 및 속도에 반응하는 자연스러운 필기감
- 수식 전용 인식 엔진 연동 (수학 기호, 분수, 제곱근, 적분 기호 등 포함)

#### 3.1.2 인식 범위
- 기본 사칙연산 및 수식 표현
- 방정식, 부등식, 함수식
- 기하학적 도형 및 보조선 스케치
- 행렬, 집합, 수열, 극한, 미적분 기호
- 한글/영문 풀이 설명 텍스트 병행 인식

#### 3.1.3 인식 정확도 요구
- 수식 인식 정확도: **95% 이상** (표준 필기체 기준)
- 인식 응답 시간: 풀이 완료 후 **3초 이내** 분석 시작

---

### 3.2 AI 풀이 분석 엔진

#### 3.2.1 풀이 단계 분해
- 인식된 풀이를 논리적 단계로 자동 분리
- 각 단계의 수학적 유효성 검증
- 단계 간 논리적 연결성 분석

#### 3.2.2 개념 이해도 추론
AI는 다음 항목을 기준으로 학습자의 개념 이해 수준을 판별한다:

| 판별 항목 | 설명 |
|-----------|------|
| 공식 적용 | 해당 문제 유형에 맞는 공식을 사용했는가 |
| 풀이 방향 | 접근 전략이 수학적으로 올바른가 |
| 중간 계산 | 각 단계의 계산 과정이 정확한가 |
| 논리 흐름 | 단계 간 논리적 비약 또는 오류가 없는가 |
| 최종 검증 | 답을 검증하는 과정을 시도했는가 |

#### 3.2.3 오답 원인 분류 체계

```
오답 유형
├── 개념 오류 (Conceptual Error)
│   ├── 공식 혼동 (예: 인수분해 공식 오적용)
│   ├── 개념 미형성 (예: 함수의 정의 미이해)
│   └── 유사 개념 혼동 (예: 순열/조합 혼동)
├── 절차 오류 (Procedural Error)
│   ├── 풀이 순서 오류
│   ├── 이항 부호 실수
│   └── 단계 누락
├── 계산 실수 (Computational Error)
│   ├── 산술 계산 오류
│   └── 분수/소수 처리 실수
└── 문제 이해 오류 (Comprehension Error)
    ├── 조건 미반영
    └── 구하는 것 오해
```

---

### 3.3 맞춤형 피드백 및 개념 설명

#### 3.3.1 피드백 구조
1. **오류 위치 하이라이팅**: 틀린 단계를 시각적으로 표시
2. **오류 유형 안내**: 어떤 종류의 오류인지 친절하게 설명
3. **개념 재설명**: 관련 개념을 학년 수준에 맞춰 재설명
4. **올바른 풀이 예시**: 정석 풀이 단계별 제시 (애니메이션 옵션)
5. **핵심 공식 카드**: 관련 공식과 예제를 카드 형태로 제공

#### 3.3.2 설명 수준 조절
- 학습자의 학년, 이전 학습 이력, 오답 패턴을 반영하여 설명 깊이 자동 조절
- 쉬운 말로 설명 / 수학적 표현으로 설명 선택 옵션 제공

#### 3.3.3 멀티미디어 지원
- 개념 설명 텍스트 + 수식 + 그래프/도형 시각화
- 개념 설명 TTS(Text-to-Speech) 지원 (한국어)

---

### 3.4 반복 학습 시스템

#### 3.4.1 유사 문제 생성
- 오답 문제와 동일한 개념·유형이지만 숫자·조건이 다른 새 문제 자동 생성
- 난이도를 점진적으로 상승시키는 스캐폴딩(Scaffolding) 방식 적용
- 문제 생성 시 교육과정(국내 2015/2022 개정 교육과정) 범위 준수

#### 3.4.2 완전 학습 판별
- 동일 유형 연속 3회 정답 → 해당 개념 "습득 완료" 처리
- 습득 완료 개념은 일정 기간 후 복습 문제로 재등장 (망각 곡선 기반 간격 반복)

#### 3.4.3 학습 진행 추적
- 개념 단위 습득 현황 시각화 (개념 맵)
- 오답 노트 자동 생성 및 관리
- 주간/월간 학습 리포트

---

### 3.5 문제 입력 방식

| 입력 방식 | 설명 |
|-----------|------|
| 카메라 촬영 | 교재, 시험지 문제를 카메라로 촬영하여 업로드 |
| 갤러리 이미지 | 저장된 문제 이미지 업로드 |
| 앱 내 문제은행 | 과목/단원/난이도별 문제 선택 |
| 직접 입력 | 앱 내 수식 에디터로 문제 직접 작성 |

---

### 3.6 학부모/교사 대시보드

- 학습자 오답 유형 현황 요약
- 취약 개념 리스트
- 학습 시간 및 문제 풀이 횟수
- 알림 설정 (학습 목표 달성, 장기 미접속 등)

---

## 4. 시스템 아키텍처

### 4.1 전체 구조

```
┌─────────────────────────────────────────────────────┐
│                  모바일 클라이언트                     │
│         (iOS Swift / Android Kotlin)                │
│                                                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐  │
│  │  펜 입력  │  │ 카메라   │  │  문제은행 UI      │  │
│  │  캔버스   │  │ 스캐너   │  │  학습 대시보드    │  │
│  └────┬─────┘  └────┬─────┘  └──────────────────┘  │
└───────┼─────────────┼───────────────────────────────┘
        │             │
        ▼             ▼
┌─────────────────────────────────────────────────────┐
│                    API Gateway                       │
│              (REST / WebSocket)                      │
└──────────────────────┬──────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────────┐
│  HTR 서비스  │ │  AI 분석     │ │  문제 생성 서비스 │
│ (손글씨 인식)│ │  엔진        │ │  (문제은행 + LLM) │
│              │ │  (LLM 기반)  │ │                  │
└──────┬───────┘ └──────┬───────┘ └────────┬─────────┘
       │                │                  │
       └────────────────┼──────────────────┘
                        ▼
              ┌──────────────────┐
              │   데이터베이스    │
              │  - 사용자 정보   │
              │  - 학습 이력     │
              │  - 문제/풀이 저장│
              └──────────────────┘
```

### 4.2 AI 분석 파이프라인

```
[사용자 펜 입력]
      ↓
[이미지 전처리] → 노이즈 제거, 정렬, 이진화
      ↓
[HTR 엔진] → 수식/텍스트 LaTeX 변환
      ↓
[풀이 단계 파서] → 논리 단계 분리
      ↓
[멀티모달 LLM] → 개념 이해도 추론 + 오류 분류
      ↓
[피드백 생성기] → 맞춤형 설명 + 유사 문제 생성
      ↓
[사용자 화면 출력]
```

---

## 5. 기술 스택 요구사항

### 5.1 모바일 클라이언트

| 플랫폼 | 요구 기술 |
|--------|-----------|
| iOS | Swift 5.9+, SwiftUI, PencilKit, Vision Framework |
| Android | Kotlin, Jetpack Compose, Android Ink API, ML Kit |
| 공통 고려 | React Native 또는 Flutter 기반 크로스플랫폼 병행 검토 가능 |

### 5.2 손글씨 인식 (HTR)

- **수식 인식**: MyScript Nebo SDK, MathPix API, 또는 자체 학습 모델
- **일반 텍스트 인식**: Google ML Kit, Apple Vision Framework
- **LaTeX 변환**: 인식 결과를 구조화된 수식으로 변환

### 5.3 AI 백엔드

| 구성 요소 | 기술 옵션 |
|-----------|-----------|
| LLM 기반 분석 | OpenAI GPT-4o, Anthropic Claude, 또는 자체 파인튜닝 모델 |
| 문제 생성 | LLM + 수학 문제 템플릿 엔진 |
| 개념 지식 그래프 | Neo4j 또는 커스텀 온톨로지 |
| 벡터 검색 | Pinecone, Weaviate (유사 문제 검색) |

### 5.4 인프라

| 구성 | 기술 |
|------|------|
| 클라우드 | AWS 또는 GCP |
| API 서버 | FastAPI (Python) 또는 Node.js |
| 데이터베이스 | PostgreSQL (사용자/학습 데이터), Redis (캐싱) |
| 스토리지 | S3 호환 (풀이 이미지 저장) |
| 인증 | OAuth 2.0, JWT, 소셜 로그인 (Google, Apple, Kakao) |
| 모니터링 | Datadog 또는 Grafana + Prometheus |

### 5.5 보안 요구사항

- 미성년자 데이터 처리: 개인정보보호법 및 아동·청소년 관련 법령 준수
- 모든 데이터 전송 TLS 1.3 암호화
- 풀이 이미지 저장 시 개인 식별 정보 분리 보관
- OWASP Mobile Top 10 기준 보안 설계

---

## 6. 손글씨 인식 기술 상세 요구사항

본 챕터는 MathLens AI의 핵심 기술인 손글씨 수식 인식(HTR, Handwritten Text Recognition) 구현에 필요한 기술적 방법론, 도구, 구현 전략을 상세히 기술한다. 제안사는 아래 내용을 기반으로 자사의 구체적인 구현 방안을 제안서에 포함해야 한다.

---

### 6.1 손글씨 인식 기술 개요 및 접근 방법

수학 손글씨 인식은 일반 텍스트 인식보다 훨씬 복잡하다. 수식은 2차원 구조(분수, 지수, 첨자 등)를 가지며, 기호의 종류가 방대하고, 필기자마다 편차가 크다. 이를 해결하기 위한 기술 접근법은 크게 세 가지 방향으로 분류된다.

| 접근 방법 | 설명 | 장점 | 단점 |
|-----------|------|------|------|
| 온라인 인식 (Online HTR) | 펜의 이동 경로(스트로크) 데이터를 실시간으로 분석 | 빠른 응답, 필순 정보 활용 가능 | 스타일러스 펜 필수, 스트로크 수집 인프라 필요 |
| 오프라인 인식 (Offline HTR) | 완성된 이미지(사진/스캔)를 분석 | 카메라 촬영 지원, 범용성 높음 | 이미지 품질에 민감, 처리 시간 다소 소요 |
| 하이브리드 | 온라인 + 오프라인 병행 | 두 방식의 장점 결합 | 구현 복잡도 증가 |

**본 프로젝트의 기본 방향은 하이브리드 방식**으로, 스타일러스 펜 입력 시 온라인 인식, 카메라 촬영 시 오프라인 인식을 적용한다.

---

### 6.2 입력 데이터 수집 및 전처리

#### 6.2.1 온라인 입력 (스트로크 기반)

스타일러스 또는 터치 입력 시 수집되는 데이터:

```
스트로크 데이터 구조
{
  strokes: [
    {
      points: [ {x, y, pressure, timestamp}, ... ],
      strokeId: "s1"
    },
    ...
  ],
  canvasWidth: 1080,
  canvasHeight: 1920,
  inputDevice: "stylus" | "touch"
}
```

- **필압(Pressure)**: Apple Pencil / S-Pen의 필압 데이터를 활용하여 획의 굵기 및 의도 파악
- **속도(Velocity)**: 빠르게 그은 선과 천천히 그은 기호를 구분
- **스트로크 순서**: 필순 정보를 기반으로 기호 분류 정확도 향상

#### 6.2.2 이미지 전처리 파이프라인 (오프라인)

카메라 촬영 이미지 또는 캔버스 스냅샷에 적용하는 전처리 단계:

```
[원본 이미지 입력]
        ↓
[1단계: 기울기 보정 (Deskewing)]
   - Hough Transform으로 텍스트 라인 기울기 감지
   - 최대 ±15° 자동 보정
        ↓
[2단계: 노이즈 제거 (Denoising)]
   - Gaussian Blur → 카메라 촬영 노이즈 제거
   - Median Filter → 소금-후추 노이즈 제거
        ↓
[3단계: 이진화 (Binarization)]
   - Otsu's Thresholding (균일 조명 환경)
   - Adaptive Thresholding (불균일 조명 / 그림자)
        ↓
[4단계: 레이아웃 분석 (Layout Analysis)]
   - 풀이 줄(Line) 단위 분리
   - 수식 영역 vs 텍스트 영역 구분
        ↓
[5단계: 기호 분절 (Symbol Segmentation)]
   - Connected Component Analysis로 개별 기호 분리
   - 분수선, 근호 등 구조적 기호 우선 검출
        ↓
[전처리 완료 → HTR 엔진 입력]
```

#### 6.2.3 전처리 라이브러리 권장

| 라이브러리 | 용도 | 플랫폼 |
|-----------|------|--------|
| OpenCV | 이미지 전처리 전반 | Python/Android/iOS |
| Pillow | 경량 이미지 처리 | Python 백엔드 |
| Core Image | iOS 네이티브 필터 | iOS |
| Android Bitmap | Android 네이티브 처리 | Android |

---

### 6.3 수식 인식 엔진 옵션 비교

#### 6.3.1 상용 API/SDK

| 솔루션 | 제공사 | 방식 | 수식 지원 수준 | 비용 |
|--------|--------|------|--------------|------|
| **MathPix API** | MathPix | 오프라인(이미지) | LaTeX 직접 변환, 최고 수준 | 유료 API (건당 과금) |
| **MyScript Math SDK** | MyScript | 온라인(스트로크) | 실시간 수식 인식, LaTeX/MathML 출력 | SDK 라이선스 |
| **Google ML Kit** | Google | 오프라인(이미지) | 텍스트 인식 강점, 수식 제한적 | 무료 (온디바이스) |
| **Apple Vision** | Apple | 오프라인(이미지) | 텍스트 인식 우수, 수식 제한적 | 무료 (iOS 전용) |
| **Pix2tex (LaTeX-OCR)** | 오픈소스 | 오프라인(이미지) | 수식 특화, 자체 호스팅 | 무료 (서버 비용만) |

#### 6.3.2 권장 조합 전략

```
입력 유형별 엔진 선택 전략

[스타일러스 펜 실시간 입력]
        ↓
  MyScript Math SDK (온라인 HTR)
  → 스트로크 단위 실시간 인식
  → LaTeX / MathML 출력

[카메라 촬영 / 갤러리 이미지]
        ↓
  MathPix API (클라우드) 또는
  Pix2tex 자체 호스팅 (비용 절감)
  → 이미지 → LaTeX 변환

[텍스트 설명 (한글/영문)]
        ↓
  Google ML Kit (Android) /
  Apple Vision (iOS)
  → 일반 텍스트 인식
```

#### 6.3.3 자체 모델 개발 옵션 (선택 사항)

비용 절감 및 성능 최적화를 위해 자체 수식 인식 모델 개발을 고려할 수 있다:

- **베이스 모델**: TrOCR (Microsoft), Pix2tex, CRNN+CTC
- **파인튜닝 데이터셋**: CROHME(국제 손글씨 수식 인식 대회 데이터), IM2LATEX-100K
- **한국 수학 교과서 특화**: 국내 교과서 수식 스타일에 맞춘 추가 학습 데이터 구축 필요
- **온디바이스 추론**: TensorFlow Lite / Core ML 변환으로 오프라인 동작 가능

> 자체 모델 개발 시 초기 정확도가 상용 API 대비 낮을 수 있으므로, Phase 1에서는 상용 API 사용 후 Phase 3에서 자체 모델로 전환하는 단계적 접근을 권장한다.

---

### 6.4 수식 구조 파싱 및 LaTeX 변환

#### 6.4.1 2차원 수식 구조 인식

수학 수식은 선형(1D)이 아닌 2차원 구조를 가지므로, 단순 좌→우 순서 인식이 아닌 구조적 파싱이 필요하다:

```
인식 대상 2D 구조 예시

분수:        a           지수:  x²        근호:  √(a+b)
           ───
            b

행렬:  [1  2]            적분:  ∫f(x)dx
       [3  4]
```

**구조 파싱 알고리즘:**

1. **기준선(Baseline) 검출**: 수식의 기준 수평선 파악
2. **영역 분류**: 기준선 위(지수/분자), 기준선(본문), 기준선 아래(첨자/분모)로 구분
3. **재귀적 파싱**: 분수 내부, 근호 내부 등을 재귀적으로 하위 수식으로 처리
4. **LaTeX 트리 생성**: 파싱 결과를 LaTeX AST(Abstract Syntax Tree)로 변환

#### 6.4.2 LaTeX 출력 및 검증

인식된 수식을 LaTeX로 변환 후 수학적 유효성 검증:

```python
# LaTeX 검증 예시 (Python)
import sympy
from sympy.parsing.latex import parse_latex

def validate_latex(latex_str: str) -> dict:
    try:
        expr = parse_latex(latex_str)
        return {
            "valid": True,
            "expression": str(expr),
            "simplified": str(sympy.simplify(expr))
        }
    except Exception as e:
        return {"valid": False, "error": str(e)}
```

#### 6.4.3 지원 수식 기호 범위

| 분류 | 기호 예시 |
|------|-----------|
| 기본 연산 | +, −, ×, ÷, =, ≠, <, >, ≤, ≥ |
| 분수/지수 | a/b, xⁿ, x₁, √x, ⁿ√x |
| 함수 | sin, cos, tan, log, ln, lim, Σ, ∏ |
| 미적분 | ∫, ∂, d/dx, f'(x), f''(x) |
| 집합/논리 | ∈, ∉, ⊂, ∪, ∩, ∀, ∃ |
| 행렬/벡터 | [ ], ( ), 벡터 화살표 |
| 그리스 문자 | α, β, γ, θ, π, Σ, Δ, λ |

---

### 6.5 플랫폼별 네이티브 구현

#### 6.5.1 iOS — PencilKit + Vision Framework

```swift
import PencilKit
import Vision

class MathCanvasViewController: UIViewController, PKCanvasViewDelegate {

    private let canvasView = PKCanvasView()
    private let toolPicker = PKToolPicker()

    override func viewDidLoad() {
        super.viewDidLoad()
        setupCanvas()
    }

    private func setupCanvas() {
        canvasView.delegate = self
        canvasView.drawingPolicy = .anyInput  // 펜 + 손가락 모두 허용
        canvasView.backgroundColor = .white
        view.addSubview(canvasView)

        // Tool Picker 연결 (펜, 지우개 등)
        toolPicker.setVisible(true, forFirstResponder: canvasView)
        toolPicker.addObserver(canvasView)
        canvasView.becomeFirstResponder()
    }

    // 풀이 완료 시 이미지 추출
    func extractDrawingImage() -> UIImage {
        let drawing = canvasView.drawing
        return drawing.image(from: drawing.bounds, scale: UIScreen.main.scale)
    }

    // 스트로크 데이터 추출 (MyScript SDK 연동용)
    func extractStrokes() -> [[PKStroke]] {
        return [canvasView.drawing.strokes]
    }

    // 실시간 인식 트리거
    func canvasViewDrawingDidChange(_ canvasView: PKCanvasView) {
        // 마지막 스트로크 후 1.5초 지연 → 인식 시작 (사용자 입력 완료 감지)
        NSObject.cancelPreviousPerformRequests(withTarget: self,
            selector: #selector(triggerRecognition), object: nil)
        perform(#selector(triggerRecognition), with: nil, afterDelay: 1.5)
    }

    @objc func triggerRecognition() {
        let image = extractDrawingImage()
        // → MathPix API 또는 MyScript SDK로 전송
    }
}
```

#### 6.5.2 Android — Ink API + ML Kit

```kotlin
import androidx.ink.authoring.InProgressStrokesView
import androidx.ink.strokes.Stroke
import com.google.mlkit.vision.text.TextRecognition

class MathCanvasFragment : Fragment() {

    private lateinit var inProgressStrokesView: InProgressStrokesView
    private val completedStrokes = mutableListOf<Stroke>()

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        setupInkCanvas()
    }

    private fun setupInkCanvas() {
        inProgressStrokesView = view.findViewById(R.id.ink_canvas)

        // 스트로크 완료 콜백
        inProgressStrokesView.addFinishedStrokesListener { strokes ->
            completedStrokes.addAll(strokes)
            scheduleRecognition()
        }
    }

    // 입력 완료 감지 후 인식 트리거
    private val recognitionHandler = Handler(Looper.getMainLooper())
    private fun scheduleRecognition() {
        recognitionHandler.removeCallbacksAndMessages(null)
        recognitionHandler.postDelayed({ triggerRecognition() }, 1500)
    }

    private fun triggerRecognition() {
        val bitmap = captureCanvasBitmap()
        sendToMathRecognitionApi(bitmap)
    }

    // 비트맵 캡처
    private fun captureCanvasBitmap(): Bitmap {
        val bitmap = Bitmap.createBitmap(
            inProgressStrokesView.width,
            inProgressStrokesView.height,
            Bitmap.Config.ARGB_8888
        )
        val canvas = Canvas(bitmap)
        canvas.drawColor(Color.WHITE)
        inProgressStrokesView.draw(canvas)
        return bitmap
    }

    // MathPix API 연동
    private fun sendToMathRecognitionApi(bitmap: Bitmap) {
        val base64Image = bitmapToBase64(bitmap)
        viewModel.analyzeMathSolution(base64Image)
    }
}
```

---

### 6.6 수식 인식 API 연동 명세

#### 6.6.1 MathPix API 연동

```python
# 백엔드: MathPix API 호출 예시
import httpx
import base64

async def recognize_math_image(image_base64: str) -> dict:
    """
    MathPix API로 수식 이미지 → LaTeX 변환
    """
    headers = {
        "app_id": MATHPIX_APP_ID,
        "app_key": MATHPIX_APP_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "src": f"data:image/png;base64,{image_base64}",
        "formats": ["latex_styled", "text", "asciimath"],
        "data_options": {
            "include_latex": True,
            "include_asciimath": True
        },
        "include_line_data": True   # 줄 단위 인식 결과
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.mathpix.com/v3/text",
            headers=headers,
            json=payload,
            timeout=10.0
        )
    result = response.json()
    return {
        "latex": result.get("latex_styled", ""),
        "text": result.get("text", ""),
        "confidence": result.get("confidence", 0),
        "lines": result.get("line_data", [])
    }
```

#### 6.6.2 MyScript Math SDK 연동 (iOS)

```swift
import MyScriptInteractiveInk

class MyScriptRecognizer: NSObject {

    private var engine: IINKEngine!
    private var editor: IINKEditor!

    func initialize() {
        // MyScript 라이선스 초기화
        engine = IINKEngine(certificate: myCertificate)

        // 수식 인식 패키지 설정
        let contentPackage = try! engine.createPackage(withName: "MathSession")
        let contentPart = try! contentPackage.createPart(with: "Math")

        // 에디터 생성
        let renderer = try! engine.createRenderer(dpiX: 96, dpiY: 96, target: self)
        editor = try! engine.createEditor(renderer: renderer)
        try! editor.setPart(contentPart)
    }

    // 스트로크 추가
    func addStroke(_ stroke: PKStroke) {
        let pointerEvents = stroke.points.map { point in
            IINKPointerEvent(
                type: .move,
                x: Float(point.location.x),
                y: Float(point.location.y),
                t: point.timeOffset,
                f: Float(point.force),
                pointerId: 1
            )
        }
        try! editor.pointerEvents(pointerEvents, doProcessGestures: false)
    }

    // LaTeX 결과 추출
    func exportToLatex() -> String {
        return (try? editor.export_(selection: nil, mimeType: .LATEX)) ?? ""
    }
}
```

---

### 6.7 인식 후처리 및 품질 향상

#### 6.7.1 신뢰도 기반 재처리

```python
async def process_recognition_result(result: dict) -> dict:
    confidence = result.get("confidence", 0)

    if confidence >= 0.95:
        # 고신뢰도: 바로 사용
        return result

    elif confidence >= 0.7:
        # 중간 신뢰도: LLM으로 보정 요청
        corrected = await llm_correct_latex(result["latex"])
        return {**result, "latex": corrected, "corrected": True}

    else:
        # 저신뢰도: 사용자에게 재입력 요청
        return {**result, "needs_retry": True,
                "message": "손글씨를 더 또렷하게 작성해 주세요."}
```

#### 6.7.2 LLM 기반 LaTeX 보정

인식된 LaTeX가 불완전하거나 문맥상 오류가 있을 경우, LLM으로 보정한다:

```python
async def llm_correct_latex(raw_latex: str, problem_context: str = "") -> str:
    """
    인식된 LaTeX를 LLM으로 문맥 보정
    """
    prompt = f"""
다음은 손글씨 수식 인식 결과입니다. 수학적으로 올바른 LaTeX로 보정해주세요.

인식 결과: {raw_latex}
문제 맥락: {problem_context}

규칙:
1. 인식 오류(예: x2 → x^2, 1/2 → \\frac{{1}}{{2}})를 수정
2. 누락된 괄호, 중괄호를 보완
3. 수학적으로 의미 있는 표현으로만 수정
4. LaTeX 코드만 반환 (설명 없이)
"""
    response = await anthropic_client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text.strip()
```

#### 6.7.3 사용자 수정 피드백 루프

인식 결과를 사용자가 수정할 수 있는 UI를 제공하고, 수정 데이터를 수집하여 모델 개선에 활용:

```
[인식 결과 표시]
      ↓
[사용자 확인/수정]
      ↓
  수정 없음 → 학습 데이터로 저장 (정답 레이블)
  수정 있음 → (원본, 수정본) 쌍으로 저장 → 모델 파인튜닝 데이터
```

---

### 6.8 성능 요구사항 및 측정 기준

| 지표 | 요구 수준 | 측정 방법 |
|------|-----------|-----------|
| 수식 인식 정확도 (CER) | 문자 오류율 5% 이하 | 표준 테스트셋 (CROHME 2023) |
| 수식 인식 정확도 (ExpRate) | 수식 단위 정답률 90% 이상 | 수식 전체 일치 여부 |
| 인식 응답 시간 | 3초 이내 (LTE 환경) | 95 percentile 기준 |
| 온디바이스 인식 (Phase 3) | 1초 이내 | 오프라인 환경 기준 |
| 지원 기호 종류 | 300종 이상 | 수학 기호 커버리지 |
| 필기 스타일 범용성 | 다양한 필기체 지원 | 10명 이상 사용자 테스트 |

#### 6.8.1 인식 정확도 평가 방법

```
평가 지표

1. Character Error Rate (CER)
   CER = (삽입 + 삭제 + 대체) / 전체 문자 수

2. Expression Recognition Rate (ExpRate)
   ExpRate = 완전히 일치하는 수식 수 / 전체 수식 수

3. Structural Accuracy
   - 분수, 지수, 근호 등 구조적 요소의 정확도 별도 측정

테스트 데이터셋
- CROHME 2023 (국제 표준)
- 국내 교과서 수식 자체 구축 데이터셋 (최소 5,000건)
- 실사용자 수집 데이터 (베타 테스트)
```

---

### 6.9 오프라인(온디바이스) 인식 전략 (Phase 3)

네트워크 없이 기기 내에서 수식을 인식하기 위한 경량 모델 전략:

| 항목 | 내용 |
|------|------|
| 모델 크기 목표 | 50MB 이하 (모바일 최적화) |
| 변환 포맷 | TensorFlow Lite (.tflite) / Core ML (.mlmodel) |
| 양자화 | INT8 양자화로 모델 크기 및 추론 속도 최적화 |
| 베이스 모델 | MobileViT, EfficientNet 기반 경량 인코더 |
| 학습 방법 | Knowledge Distillation (대형 모델 → 경량 모델) |
| 폴백 전략 | 온디바이스 인식 실패 시 → 클라우드 API 자동 전환 |

---

### 6.10 제안사 요구사항

제안사는 손글씨 인식 기술과 관련하여 제안서에 다음을 반드시 포함해야 한다:

1. **채택 기술 명시**: 상용 API(MathPix, MyScript 등) 또는 자체 모델 중 선택 및 사유
2. **정확도 달성 계획**: CER 5% 이하, ExpRate 90% 이상 달성을 위한 구체적 방안
3. **플랫폼별 구현 방안**: iOS(PencilKit 기반), Android(Ink API 기반) 각각의 구현 전략
4. **전처리 파이프라인**: 이미지 전처리 단계 및 적용 기술 명시
5. **라이선스 비용**: 상용 SDK/API 사용 시 라이선스 및 API 비용 산출
6. **성능 측정 계획**: 테스트 데이터셋 구성 및 정확도 측정 방법론
7. **오류 처리 전략**: 인식 실패 또는 저신뢰도 결과 처리 방안
8. **단계별 전환 계획**: Phase 1(상용 API) → Phase 3(온디바이스) 전환 로드맵

---

## 7. UX/UI 설계 방향

### 6.1 핵심 화면 구성

#### 화면 1: 홈 대시보드
- 오늘의 학습 현황 (목표 문제 수, 달성률)
- 최근 오답 유형 요약
- 추천 복습 문제 카드

#### 화면 2: 문제 풀이 화면 (핵심)
- 상단: 문제 표시 영역
- 중단: 펜 입력 캔버스 (전체 화면 확장 가능)
- 하단: 도구 모음 (펜 굵기/색상, 지우개, 실행취소, 제출)

#### 화면 3: AI 피드백 화면
- 풀이 오류 위치 하이라이팅 오버레이
- 오류 유형 배지 (개념 오류 / 계산 실수 등)
- 개념 설명 카드 (스크롤)
- 정석 풀이 애니메이션 재생
- "다시 풀기" / "다음 유사 문제" 버튼

#### 화면 4: 개념 설명 상세
- 개념 정의 및 공식
- 핵심 예제 2~3개
- 관련 개념 링크 (개념 맵)

#### 화면 5: 학습 리포트
- 주간 학습 그래프
- 오답 유형 분포 차트
- 취약 개념 목록

### 6.2 UX 원칙

- **마찰 최소화**: 문제 촬영부터 피드백까지 탭 3회 이내
- **즉각적 피드백**: 분석 중 로딩 화면에서도 진행 상태 시각화
- **학습 동기 유지**: 연속 학습일, 개념 습득 배지 등 게임화 요소
- **접근성**: 다크모드, 글자 크기 조절, 고대비 모드 지원

---

## 8. 개발 범위 및 단계

### Phase 1 — MVP (최소 기능 제품)

**목표**: 핵심 학습 루프 검증

| 기능 | 포함 여부 |
|------|-----------|
| 펜 입력 캔버스 | ✅ |
| 수식 손글씨 인식 (중등 수준) | ✅ |
| AI 오답 분석 (상위 5개 오류 유형) | ✅ |
| 맞춤형 개념 설명 | ✅ |
| 유사 문제 재출제 (자동 생성) | ✅ |
| 기본 학습 이력 저장 | ✅ |
| 소셜 로그인 | ✅ |
| 학부모 대시보드 | ❌ (Phase 2) |
| 교사 기능 | ❌ (Phase 2) |
| 오프라인 모드 | ❌ (Phase 3) |

### Phase 2 — 기능 확장

- 학부모/교사 대시보드
- 고등 수학 전체 범위 확장
- 문제은행 확충 (교과서 연계)
- 개념 맵 시각화
- 푸시 알림 및 학습 리마인더

### Phase 3 — 고도화

- 오프라인 AI 추론 (온디바이스 모델)
- 실시간 협업 풀이 (그룹 스터디)
- 교사 맞춤 문제 출제 도구
- 수능/모의고사 연계 콘텐츠

---

## 9. 일정 계획

| 단계 | 기간 | 주요 산출물 |
|------|------|------------|
| 요구사항 분석 및 설계 | 1~2개월 | 기능 명세서, 시스템 설계서, 프로토타입 |
| Phase 1 개발 | 3~6개월 | MVP 앱 (iOS + Android) |
| 내부 테스트 (알파) | 7개월 | 버그 리포트, 성능 측정 결과 |
| 베타 테스트 | 8~9개월 | 실사용자 피드백, 개선 사항 |
| Phase 1 출시 | 10개월 | 앱스토어/플레이스토어 출시 |
| Phase 2 개발 | 11~15개월 | 확장 기능 업데이트 |
| Phase 3 개발 | 16~21개월 | 고도화 기능 업데이트 |

> **참고**: 일정은 제안사 규모 및 팀 구성에 따라 조정 협의 가능

---

## 10. 예산 및 산출 기준

### 9.1 예산 범위

| 항목 | 예상 비용 (참고) |
|------|----------------|
| Phase 1 개발 전체 | 2억 ~ 4억 원 |
| AI/LLM API 운영비 (월) | 300만 ~ 800만 원 |
| 클라우드 인프라 (월) | 100만 ~ 300만 원 |
| 유지보수 (연) | 개발비의 15~20% |

> 위 금액은 참고 범위이며, 제안사는 상세 내역을 별도 제출

### 9.2 제안서 포함 필수 비용 항목

- 인력 투입 계획 (역할별 MM 및 단가)
- 외부 API/SDK 라이선스 비용
- 인프라 구축 및 운영 비용
- QA 및 보안 감사 비용
- 앱스토어 등록 및 유지 비용
- 유지보수 및 기술 지원 조건

---

## 11. 제안사 자격 요건

### 10.1 필수 요건

- 모바일 앱 (iOS + Android) 개발 경험 **3년 이상**
- AI/ML 백엔드 구축 경험 보유
- 교육 관련 앱 개발 실적 **1건 이상**
- 손글씨 인식 또는 이미지 처리 기술 구현 경험

### 10.2 우대 요건

- LLM 기반 서비스 개발 및 운영 경험
- 수학 교육 콘텐츠 또는 에듀테크 도메인 경험
- 개인정보보호 인증 (ISMS, PIMS 등) 보유
- 스타트업 또는 인하우스 개발팀과의 협업 경험

---

## 12. 제안서 제출 요건

### 11.1 제출 서류

1. 회사 소개서 (사업자등록증 사본 포함)
2. 기술 제안서
   - 기능 구현 방안 상세 기술
   - AI 분석 파이프라인 설계
   - 손글씨 인식 기술 접근 방안
3. 수행 계획서
   - 단계별 일정 (간트 차트)
   - 팀 구성 및 역할
4. 비용 제안서 (세부 항목 명시)
5. 유사 프로젝트 포트폴리오 (최소 2건)
6. 기술 데모 또는 프로토타입 (선택, 제출 시 가산점)

### 11.2 제출 형식

- 파일 형식: PDF (또는 PPT + PDF 병행)
- 분량: 기술 제안서 30페이지 이내, 비용 제안서 별도
- 제출 방법: 이메일 또는 지정 제출 시스템

### 11.3 일정

| 항목 | 일정 |
|------|------|
| RFP 공고 | 2026년 5월 20일 |
| 질의응답 마감 | 2026년 6월 3일 |
| 제안서 제출 마감 | 2026년 6월 17일 |
| 제안 발표 (PT) | 2026년 6월 24~25일 |
| 우선협상 대상자 선정 | 2026년 7월 1일 |
| 계약 체결 | 2026년 7월 중 |

---

## 13. 평가 기준

| 평가 항목 | 배점 |
|-----------|------|
| 기술력 (AI/HTR 구현 방안의 타당성) | 35점 |
| 개발 경험 및 포트폴리오 | 20점 |
| 수행 계획의 현실성 | 15점 |
| 비용 적정성 | 15점 |
| 팀 구성 및 전문성 | 10점 |
| 기술 데모 / 프로토타입 완성도 | 5점 |
| **합계** | **100점** |

> 70점 미만 제안사는 협상 대상에서 제외

---

## 14. 부록

### 부록 A. 주요 용어 정의

| 용어 | 정의 |
|------|------|
| HTR | Handwritten Text Recognition. 손글씨를 디지털 텍스트로 변환하는 기술 |
| LaTeX | 수학 수식을 표현하는 문서 조판 언어 |
| LLM | Large Language Model. 대규모 언어 모델 |
| 완전 학습 | 학습 목표를 완전히 달성할 때까지 반복 학습하는 교육 방법론 |
| 간격 반복 | 망각 곡선에 기반하여 최적 시점에 복습을 유도하는 학습 방법 |
| 스캐폴딩 | 학습자 수준에 맞춰 점진적으로 난이도를 높여 지원하는 교육 방법 |
| 오개념 | 학습자가 잘못 형성한 개념 |

### 부록 B. 참고 교육과정 범위

- 국내 2022 개정 교육과정 수학 (중학교 1~3학년, 고등학교 공통수학 1·2, 수학 I·II, 미적분, 확률과 통계, 기하)
- 수능 수학 영역 전 범위

### 부록 C. 참고 경쟁 서비스

| 서비스 | 특징 | 차별화 포인트 |
|--------|------|--------------|
| Photomath | 카메라로 문제 인식 후 풀이 제공 | 풀이 과정 분석 없음 |
| Mathway | 수식 입력 후 답 제공 | 오답 원인 분석 없음 |
| 콴다 | 문제 촬영 후 유사 문제 검색 | AI 개념 설명 피드백 부재 |
| **MathLens AI** | **손글씨 풀이 인식 + 오답 원인 추론 + 맞춤 반복 학습** | **완전한 학습 루프 제공** |

### 부록 D. 문의처

- 담당 부서: [발주처 부서명]
- 담당자: [담당자명]
- 이메일: [이메일 주소]
- 전화: [전화번호]
- 질의응답: 이메일로만 접수 (답변 공개 게시)

---

*본 문서의 내용은 발주처의 판단에 따라 변경될 수 있으며, 최종 계약서가 우선합니다.*

*© 2026 MathLens AI Project. All rights reserved.*
