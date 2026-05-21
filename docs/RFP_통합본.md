# MathLens AI — 통합 제안요청서 (RFP)

**문서 버전:** v3.0 (통합본)  
**작성일:** 2026년 5월 21일  
**문서 유형:** 제안요청서 (Request for Proposal)  
**변경 이력:**
- v1.0 (2026-05-20) — 최초 작성
- v1.1 (2026-05-21) — 손글씨 인식 기술 상세 챕터 추가
- v2.0 (2026-05-21) — 펜 기반 수식 인식 기술 구현 방안 전면 재정비
- v3.0 (2026-05-21) — **통합본**: 백엔드 문제 출제, 펜 입력 AI 인식, 시스템 인터페이스 요구사항 통합. 모든 이전 RFP 문서를 하나로 통합.

---

## 목차

1. [프로젝트 개요](#1-프로젝트-개요)
2. [배경 및 목적](#2-배경-및-목적)
3. [핵심 기능 요구사항](#3-핵심-기능-요구사항)
4. [펜 수식 인식 기술 — 현실 구현 방안](#4-펜-수식-인식-기술--현실-구현-방안)
5. [손글씨 인식 기술 상세 요구사항](#5-손글씨-인식-기술-상세-요구사항)
6. [백엔드 문제 출제 시스템 요구사항](#6-백엔드-문제-출제-시스템-요구사항)
7. [펜 입력 캡처 및 전송 요구사항](#7-펜-입력-캡처-및-전송-요구사항)
8. [AI 인식 엔진 연동 요구사항](#8-ai-인식-엔진-연동-요구사항)
9. [전체 데이터 흐름 및 시스템 인터페이스](#9-전체-데이터-흐름-및-시스템-인터페이스)
10. [시스템 아키텍처](#10-시스템-아키텍처)
11. [기술 스택 요구사항](#11-기술-스택-요구사항)
12. [UX/UI 설계 방향](#12-uxui-설계-방향)
13. [개발 범위 및 단계](#13-개발-범위-및-단계)
14. [성능 및 품질 요구사항](#14-성능-및-품질-요구사항)
15. [보안 및 개인정보 보호 요구사항](#15-보안-및-개인정보-보호-요구사항)
16. [일정 계획](#16-일정-계획)
17. [예산 및 산출 기준](#17-예산-및-산출-기준)
18. [제안사 자격 요건](#18-제안사-자격-요건)
19. [제안서 제출 요건](#19-제안서-제출-요건)
20. [평가 기준](#20-평가-기준)
21. [부록](#21-부록)

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
- MyScript iink SDK, MathPix API 등 상용 수식 인식 엔진의 성숙과 GPT-4o·Claude의 멀티모달 능력 확보로 현실적 구현 가능성이 충분히 검증됨

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
- 문제 생성 시 교육과정(국내 2022 개정 교육과정) 범위 준수

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

## 4. 펜 수식 인식 기술 — 현실 구현 방안

> **이 챕터는 수식 인식의 현실적 구현 방안을 명확히 제시합니다.** 수식 인식은 본 프로젝트의 가장 중요한 기술적 도전 과제이므로, 현실적으로 검증된 기술 선택지를 명확히 제시합니다.

### 4.1 기술 선택 원칙

| 원칙 | 설명 |
|------|------|
| 상용화된 SDK/API 우선 | 자체 ML 모델 훈련은 데이터·비용·시간 요구가 과대하므로, 검증된 상용 엔진을 우선 채택 |
| 플랫폼 네이티브 최대 활용 | iOS PencilKit, Android Ink API는 무료·저지연·필압 지원으로 렌더링 레이어 최적 |
| 멀티모달 LLM 보완 | 인식 엔진이 처리하지 못하는 복잡 구조는 GPT-4o Vision 등 멀티모달 LLM이 보완 |
| 단계적 도입 | Phase 1: 상용 API → Phase 3: 온디바이스 경량 모델 전환 가능성 열어둠 |

---

### 4.2 추천 기술 스택 (우선순위 순)

#### 4.2.1 [1순위] MyScript iink SDK — 실시간 인터랙티브 수식 인식

| 항목 | 내용 |
|------|------|
| 공급사 | MyScript (프랑스, 1998년 설립, 손글씨 인식 전문) |
| 제품명 | Interactive Ink (iink) SDK |
| 라이선스 | 상용 SDK, 사용량 기반 과금 또는 기업 라이선스 |
| 지원 플랫폼 | iOS, Android, Web (JS) |
| 핵심 강점 | • 쓰는 도중 실시간으로 스트로크를 수식으로 변환 (배치 아님) <br>• 수학 전용 모드(Math) 탑재: 분수·제곱근·행렬·적분 기호 완벽 지원 <br>• 출력 포맷: LaTeX, MathML, 이미지 <br>• GoodNotes·Nebo·Samsung Notes에서 실사용 검증 <br>• 오프라인 동작 가능 (온디바이스 모델 포함) |
| 수식 인식 정확도 | 업계 최고 수준, 95% 이상 (표준 필기 기준) |
| 응답 지연 | 스트로크 입력 즉시 인식 (< 200ms) |
| 단점 | SDK 라이선스 비용 발생, 고급 커스터마이징 제한 |
| 참고 링크 | https://developer.myscript.com |

**구현 흐름 (iOS 예시):**
```
PencilKit (터치/필압 캔버스) → PKDrawing 스트로크 데이터
        ↓
iink SDK (Math 모드) 실시간 수식 인식
        ↓
LaTeX / MathML 출력
        ↓
백엔드 AI 분석 엔진 전달
```

**구현 흐름 (Android 예시):**
```
Android Ink API (MotionEvent) → Stroke 좌표 수집
        ↓
iink SDK (Android, Math 모드) 실시간 수식 인식
        ↓
LaTeX / MathML 출력
        ↓
백엔드 AI 분석 엔진 전달
```

---

#### 4.2.2 [2순위] MathPix API — 고정밀 손글씨 수식 이미지 인식

| 항목 | 내용 |
|------|------|
| 공급사 | Snap Inc. 산하 Mathpix (미국) |
| 제품 | Mathpix OCR API (`/v3/text`, `/v3/latex`) |
| 라이선스 | SaaS API, 요청 건수 기반 과금 (월 1,000건 무료 티어 제공) |
| 입력 | 손글씨 수식 이미지 (PNG/JPEG) 또는 PDF |
| 출력 | LaTeX, MathML, 구조화된 JSON |
| 핵심 강점 | • 인쇄체/손글씨 혼용 인식 탁월 <br>• 분수, 첨자, 행렬, 적분, 시그마 등 고급 수식 완벽 지원 <br>• 대학원 수준 수식까지 처리 <br>• REST API이므로 플랫폼 독립적 통합 용이 |
| 수식 인식 정확도 | ~97% (단독 수식 기준), 복잡 수식 ~90% |
| 응답 지연 | 1~3초 (네트워크 의존) |
| 단점 | 인터넷 연결 필수, 비용 발생, 이미지 배치 처리 (실시간 스트로크 인식 불가) |
| 적합한 시나리오 | 제출(Submit) 후 일괄 분석, 카메라 촬영 문제 인식 |

**구현 흐름:**
```
PencilKit / Android Ink → 캔버스 스냅샷 이미지 생성 (PNG)
        ↓
Mathpix API POST /v3/text (이미지 + 파라미터)
        ↓
LaTeX 응답 수신
        ↓
백엔드 AI 분석 파이프라인으로 전달
```

---

#### 4.2.3 [3순위] GPT-4o / Claude Vision — 멀티모달 LLM 직접 이미지 분석

| 항목 | 내용 |
|------|------|
| 공급사 | OpenAI (GPT-4o), Anthropic (Claude 3.5 Sonnet) |
| 활용 방식 | 손글씨 풀이 이미지를 Base64로 인코딩하여 API 전달, 프롬프트로 수식 인식 + 오류 분석 동시 요청 |
| 핵심 강점 | • 수식 인식 + AI 분석을 단일 API 호출로 처리 가능 <br>• 추가 HTR 엔진 없이도 중간 복잡도 수식 처리 가능 <br>• 한국어 수학 설명 생성 품질 매우 높음 |
| 수식 인식 정확도 | 단순~중간 수식: ~85~90% / 복잡 수식(미적분, 행렬): ~75~80% |
| 응답 지연 | 3~8초 |
| 단점 | 복잡 수식 정확도가 전문 HTR 엔진 대비 낮음, API 비용 높음, 인터넷 필수 |
| 권장 역할 | HTR 엔진 실패 시 fallback, 풀이 오류 분석 주 엔진 |

---

#### 4.2.4 [보완] 플랫폼 네이티브 API — 입력 캔버스 및 일반 텍스트 인식

| 플랫폼 | API | 역할 |
|--------|-----|------|
| iOS | PencilKit | Apple Pencil 필압·속도 반응 렌더링, 스트로크 데이터 수집 |
| iOS | VNRecognizeTextRequest (Vision) | 한글/영문 주석 텍스트 인식 (수식 아닌 설명 부분) |
| Android | MotionEvent + CustomView 또는 Jetpack Compose Canvas | 스트로크 좌표 및 필압 수집 |
| Android | Google ML Kit Ink Recognition | 기본 알파벳/숫자 인식 (수식 기호 제한적) |

> **참고**: 플랫폼 네이티브 API는 수식 인식에 직접 사용하기 어렵습니다. PencilKit/Android Ink는 렌더링 및 스트로크 수집에 집중하고, 수식 인식은 반드시 iink SDK 또는 Mathpix API를 사용해야 95% 이상 정확도를 달성할 수 있습니다.

---

### 4.3 기술 조합 권장안 (Phase별)

#### Phase 1 (MVP) — 권장 조합

```
[펜 입력 레이어]
iOS: PencilKit  |  Android: Custom Canvas (MotionEvent)
        ↓
[실시간 수식 인식]
MyScript iink SDK (Math 모드) — 온디바이스, 실시간, LaTeX 출력
        ↓ (iink 실패 또는 복잡 수식)
[Fallback: 이미지 기반 인식]
MathPix API — 캔버스 이미지 → LaTeX
        ↓
[AI 분석 엔진]
GPT-4o / Claude API — LaTeX + 원본 이미지 동시 전달, 오답 분석 + 피드백 생성
        ↓
[결과 출력]
LaTeX 렌더링 (KaTeX / MathJax) + 오류 하이라이팅 UI
```

#### Phase 3 (고도화) — 온디바이스 전환 검토

```
[온디바이스 수식 인식]
iink SDK 오프라인 모드 또는 자체 경량 모델 (CRNN + CTC 기반, CoreML/TFLite)
        ↓
[온디바이스 AI 분석]
소형 파인튜닝 모델 (Phi-3 Mini, Gemma 2B 등)
```

---

### 4.4 기술 선택 근거 요약

| 기술 | 선택/제외 이유 |
|------|--------------|
| MyScript iink SDK | ✅ **선택** — 실시간 스트로크 인식, 오프라인 지원, 업계 최고 정확도, 상용 검증 완료 |
| MathPix API | ✅ **선택 (보완)** — 이미지 기반 고정밀 인식, REST API로 백엔드 통합 용이, iink 보완 역할 |
| GPT-4o Vision | ✅ **선택 (AI 분석 주엔진)** — 수식 인식보다 오답 분석·피드백 생성에 최적, fallback 인식 역할 |
| Google ML Kit Ink | ⚠️ **제한적 사용** — 수식 기호 지원 미흡, 한글 설명 텍스트 인식에만 활용 |
| 자체 ML 모델 (처음부터 훈련) | ❌ **제외** — 수만 건 이상 레이블링 데이터 필요, 훈련 비용 수억 원, Phase 1에 비현실적 |
| Tesseract OCR | ❌ **제외** — 인쇄체 전용, 손글씨 수식 인식 정확도 30~50% 수준 |

---

### 4.5 비용 구조 (수식 인식 엔진)

| 엔진 | 과금 방식 | 예상 월 비용 (MAU 1만 기준) |
|------|-----------|--------------------------|
| MyScript iink SDK | 기업 라이선스 협상 또는 App SDK 구독 | ~$500 ~ $2,000/월 (계약 조건에 따라 상이) |
| MathPix API | 건당 $0.004 ~ $0.01 (볼륨 할인 있음) | ~$400 ~ $1,000/월 (풀이당 1회 호출 기준) |
| GPT-4o API | 입력 $2.5/1M 토큰, 출력 $10/1M 토큰 | ~$1,000 ~ $3,000/월 (분석 복잡도에 따라 상이) |
| **합계 (추정)** | | **~$2,000 ~ $6,000/월** |

> MAU 10만 이상 확장 시 MathPix 볼륨 계약 및 iink 엔터프라이즈 라이선스 별도 협상 필요

---

## 5. 손글씨 인식 기술 상세 요구사항

본 챕터는 MathLens AI의 핵심 기술인 손글씨 수식 인식(HTR) 구현에 필요한 기술적 방법론, 도구, 구현 전략을 상세히 기술한다. 제안사는 아래 내용을 기반으로 자사의 구체적인 구현 방안을 제안서에 포함해야 한다.

---

### 5.1 손글씨 인식 기술 개요 및 접근 방법

수학 손글씨 인식은 일반 텍스트 인식보다 훨씬 복잡하다. 수식은 2차원 구조(분수, 지수, 첨자 등)를 가지며, 기호의 종류가 방대하고, 필기자마다 편차가 크다.

| 접근 방법 | 설명 | 장점 | 단점 |
|-----------|------|------|------|
| 온라인 인식 (Online HTR) | 펜의 이동 경로(스트로크) 데이터를 실시간으로 분석 | 빠른 응답, 필순 정보 활용 가능 | 스타일러스 펜 필수, 스트로크 수집 인프라 필요 |
| 오프라인 인식 (Offline HTR) | 완성된 이미지(사진/스캔)를 분석 | 카메라 촬영 지원, 범용성 높음 | 이미지 품질에 민감, 처리 시간 다소 소요 |
| 하이브리드 | 온라인 + 오프라인 병행 | 두 방식의 장점 결합 | 구현 복잡도 증가 |

**본 프로젝트의 기본 방향은 하이브리드 방식**으로, 스타일러스 펜 입력 시 온라인 인식, 카메라 촬영 시 오프라인 인식을 적용한다.

---

### 5.2 입력 데이터 수집 및 전처리

#### 5.2.1 온라인 입력 (스트로크 기반)

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

#### 5.2.2 이미지 전처리 파이프라인 (오프라인)

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

#### 5.2.3 전처리 라이브러리 권장

| 라이브러리 | 용도 | 플랫폼 |
|-----------|------|--------|
| OpenCV | 이미지 전처리 전반 | Python/Android/iOS |
| Pillow | 경량 이미지 처리 | Python 백엔드 |
| Core Image | iOS 네이티브 필터 | iOS |
| Android Bitmap | Android 네이티브 처리 | Android |

---

### 5.3 수식 인식 엔진 옵션 비교

#### 5.3.1 상용 API/SDK

| 솔루션 | 제공사 | 방식 | 수식 지원 수준 | 비용 |
|--------|--------|------|--------------|------|
| **MathPix API** | MathPix | 오프라인(이미지) | LaTeX 직접 변환, 최고 수준 | 유료 API (건당 과금) |
| **MyScript Math SDK** | MyScript | 온라인(스트로크) | 실시간 수식 인식, LaTeX/MathML 출력 | SDK 라이선스 |
| **Google ML Kit** | Google | 오프라인(이미지) | 텍스트 인식 강점, 수식 제한적 | 무료 (온디바이스) |
| **Apple Vision** | Apple | 오프라인(이미지) | 텍스트 인식 우수, 수식 제한적 | 무료 (iOS 전용) |
| **Pix2tex (LaTeX-OCR)** | 오픈소스 | 오프라인(이미지) | 수식 특화, 자체 호스팅 | 무료 (서버 비용만) |

#### 5.3.2 권장 조합 전략

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

#### 5.3.3 자체 모델 개발 옵션 (선택 사항)

- **베이스 모델**: TrOCR (Microsoft), Pix2tex, CRNN+CTC
- **파인튜닝 데이터셋**: CROHME(국제 손글씨 수식 인식 대회 데이터), IM2LATEX-100K
- **한국 수학 교과서 특화**: 국내 교과서 수식 스타일에 맞춘 추가 학습 데이터 구축 필요
- **온디바이스 추론**: TensorFlow Lite / Core ML 변환으로 오프라인 동작 가능

> 자체 모델 개발 시 초기 정확도가 상용 API 대비 낮을 수 있으므로, Phase 1에서는 상용 API 사용 후 Phase 3에서 자체 모델로 전환하는 단계적 접근을 권장한다.

---

### 5.4 수식 구조 파싱 및 LaTeX 변환

#### 5.4.1 2차원 수식 구조 인식

수학 수식은 선형(1D)이 아닌 2차원 구조를 가지므로, 단순 좌→우 순서 인식이 아닌 구조적 파싱이 필요하다.

**구조 파싱 알고리즘:**
1. **기준선(Baseline) 검출**: 수식의 기준 수평선 파악
2. **영역 분류**: 기준선 위(지수/분자), 기준선(본문), 기준선 아래(첨자/분모)로 구분
3. **재귀적 파싱**: 분수 내부, 근호 내부 등을 재귀적으로 하위 수식으로 처리
4. **LaTeX 트리 생성**: 파싱 결과를 LaTeX AST(Abstract Syntax Tree)로 변환

#### 5.4.2 LaTeX 출력 및 검증

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

#### 5.4.3 지원 수식 기호 범위

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

### 5.5 플랫폼별 네이티브 구현

#### 5.5.1 iOS — PencilKit + Vision Framework

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

        toolPicker.setVisible(true, forFirstResponder: canvasView)
        toolPicker.addObserver(canvasView)
        canvasView.becomeFirstResponder()
    }

    func extractDrawingImage() -> UIImage {
        let drawing = canvasView.drawing
        return drawing.image(from: drawing.bounds, scale: UIScreen.main.scale)
    }

    func canvasViewDrawingDidChange(_ canvasView: PKCanvasView) {
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

#### 5.5.2 Android — Ink API + ML Kit

```kotlin
import androidx.ink.authoring.InProgressStrokesView
import androidx.ink.strokes.Stroke

class MathCanvasFragment : Fragment() {

    private lateinit var inProgressStrokesView: InProgressStrokesView
    private val completedStrokes = mutableListOf<Stroke>()

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        setupInkCanvas()
    }

    private fun setupInkCanvas() {
        inProgressStrokesView = view.findViewById(R.id.ink_canvas)
        inProgressStrokesView.addFinishedStrokesListener { strokes ->
            completedStrokes.addAll(strokes)
            scheduleRecognition()
        }
    }

    private val recognitionHandler = Handler(Looper.getMainLooper())
    private fun scheduleRecognition() {
        recognitionHandler.removeCallbacksAndMessages(null)
        recognitionHandler.postDelayed({ triggerRecognition() }, 1500)
    }

    private fun triggerRecognition() {
        val bitmap = captureCanvasBitmap()
        sendToMathRecognitionApi(bitmap)
    }

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
}
```

---

### 5.6 수식 인식 API 연동 명세

#### 5.6.1 MathPix API 연동

```python
import httpx
import base64

async def recognize_math_image(image_base64: str) -> dict:
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
        "include_line_data": True
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

#### 5.6.2 MyScript Math SDK 연동 (iOS)

```swift
import MyScriptInteractiveInk

class MyScriptRecognizer: NSObject {

    private var engine: IINKEngine!
    private var editor: IINKEditor!

    func initialize() {
        engine = IINKEngine(certificate: myCertificate)
        let contentPackage = try! engine.createPackage(withName: "MathSession")
        let contentPart = try! contentPackage.createPart(with: "Math")
        let renderer = try! engine.createRenderer(dpiX: 96, dpiY: 96, target: self)
        editor = try! engine.createEditor(renderer: renderer)
        try! editor.setPart(contentPart)
    }

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

    func exportToLatex() -> String {
        return (try? editor.export_(selection: nil, mimeType: .LATEX)) ?? ""
    }
}
```

---

### 5.7 인식 후처리 및 품질 향상

#### 5.7.1 신뢰도 기반 재처리

```python
async def process_recognition_result(result: dict) -> dict:
    confidence = result.get("confidence", 0)

    if confidence >= 0.95:
        return result

    elif confidence >= 0.7:
        corrected = await llm_correct_latex(result["latex"])
        return {**result, "latex": corrected, "corrected": True}

    else:
        return {**result, "needs_retry": True,
                "message": "손글씨를 더 또렷하게 작성해 주세요."}
```

#### 5.7.2 LLM 기반 LaTeX 보정

인식된 LaTeX가 불완전하거나 문맥상 오류가 있을 경우 LLM으로 보정:

```python
async def llm_correct_latex(raw_latex: str, problem_context: str = "") -> str:
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
    # LLM API 호출
    ...
```

#### 5.7.3 사용자 수정 피드백 루프

```
[인식 결과 표시]
      ↓
[사용자 확인/수정]
      ↓
  수정 없음 → 학습 데이터로 저장 (정답 레이블)
  수정 있음 → (원본, 수정본) 쌍으로 저장 → 모델 파인튜닝 데이터
```

---

### 5.8 성능 요구사항 및 측정 기준

| 지표 | 요구 수준 | 측정 방법 |
|------|-----------|-----------|
| 수식 인식 정확도 (CER) | 문자 오류율 5% 이하 | 표준 테스트셋 (CROHME 2023) |
| 수식 인식 정확도 (ExpRate) | 수식 단위 정답률 90% 이상 | 수식 전체 일치 여부 |
| 인식 응답 시간 | 3초 이내 (LTE 환경) | 95 percentile 기준 |
| 온디바이스 인식 (Phase 3) | 1초 이내 | 오프라인 환경 기준 |
| 지원 기호 종류 | 300종 이상 | 수학 기호 커버리지 |
| 필기 스타일 범용성 | 다양한 필기체 지원 | 10명 이상 사용자 테스트 |

---

### 5.9 오프라인(온디바이스) 인식 전략 (Phase 3)

| 항목 | 내용 |
|------|------|
| 모델 크기 목표 | 50MB 이하 (모바일 최적화) |
| 변환 포맷 | TensorFlow Lite (.tflite) / Core ML (.mlmodel) |
| 양자화 | INT8 양자화로 모델 크기 및 추론 속도 최적화 |
| 베이스 모델 | MobileViT, EfficientNet 기반 경량 인코더 |
| 학습 방법 | Knowledge Distillation (대형 모델 → 경량 모델) |
| 폴백 전략 | 온디바이스 인식 실패 시 → 클라우드 API 자동 전환 |

---

### 5.10 제안사 손글씨 인식 관련 제출 필수 항목

제안사는 제안서에 다음을 반드시 포함해야 한다:

1. **채택 기술 명시**: 상용 API(MathPix, MyScript 등) 또는 자체 모델 중 선택 및 사유
2. **정확도 달성 계획**: CER 5% 이하, ExpRate 90% 이상 달성을 위한 구체적 방안
3. **플랫폼별 구현 방안**: iOS(PencilKit 기반), Android(Ink API 기반) 각각의 구현 전략
4. **전처리 파이프라인**: 이미지 전처리 단계 및 적용 기술 명시
5. **라이선스 비용**: 상용 SDK/API 사용 시 라이선스 및 API 비용 산출
6. **성능 측정 계획**: 테스트 데이터셋 구성 및 정확도 측정 방법론
7. **오류 처리 전략**: 인식 실패 또는 저신뢰도 결과 처리 방안
8. **단계별 전환 계획**: Phase 1(상용 API) → Phase 3(온디바이스) 전환 로드맵

---

## 6. 백엔드 문제 출제 시스템 요구사항

### 6.1 문제은행 데이터베이스

#### 6.1.1 문제 메타데이터 스키마

| 필드 | 타입 | 설명 |
|------|------|------|
| `problem_id` | UUID | 고유 식별자 |
| `title` | string | 문제 제목 (선택) |
| `content_text` | string | 문제 본문 (LaTeX 포함 텍스트) |
| `content_image_url` | string | 문제 이미지 URL (선택) |
| `answer` | string | 정답 (LaTeX 또는 텍스트) |
| `solution_steps` | JSON array | 모범 풀이 단계 |
| `subject` | enum | 과목 (대수, 기하, 미적분, 확률통계, 기타) |
| `grade` | enum | 학년 (중1~고3, 수능) |
| `difficulty` | int (1~5) | 난이도 |
| `concept_tags` | string array | 관련 개념 태그 |
| `error_type_tags` | string array | 연관 오류 유형 태그 |
| `curriculum_code` | string | 2022 개정 교육과정 코드 |
| `source` | enum | 문제 출처 (문제은행/LLM생성/교과서) |
| `status` | enum | 상태 (draft/review/active/archived) |
| `created_at` | datetime | 생성 일시 |

#### 6.1.2 문제은행 규모

| 학교급 | 최소 문제 수 (초기 구축) |
|--------|------------------------|
| 중학교 (1~3학년) | 3,000문항 이상 |
| 고등학교 공통·수학I·II | 5,000문항 이상 |
| 미적분·확률통계·기하 | 3,000문항 이상 |
| **합계** | **11,000문항 이상** |

### 6.2 문제 출제 API

#### 6.2.1 개인화 문제 출제

```
GET /api/v1/problems/recommend
```

| 파라미터 | 필수 | 설명 |
|----------|------|------|
| `user_id` | ✅ | 학습자 식별자 |
| `grade` | ✅ | 학년 |
| `subject` | ❌ | 과목 필터 |
| `difficulty_range` | ❌ | 난이도 범위 (예: `2-4`) |
| `concept_tags` | ❌ | 특정 개념 태그 필터 |
| `limit` | ❌ | 반환 문제 수 (기본 1, 최대 10) |

개인화 추천 로직 요구사항:
- 사용자의 최근 오답 개념 태그 우선 출제 (가중치 70%)
- 난이도 스캐폴딩: 직전 정답 연속 횟수에 따라 난이도 자동 상향 (연속 3회 정답 시 +1 난이도)
- 동일 문제 24시간 내 재출제 금지
- 취약 개념 대비 강점 개념 출제 비율 = 7:3

#### 6.2.2 LLM 기반 유사 문제 동적 생성

```
POST /api/v1/problems/generate
```

요청 바디:

```json
{
  "reference_problem_id": "uuid",
  "concept_tags": ["이차방정식", "인수분해"],
  "difficulty": 3,
  "error_type": "conceptual_error",
  "grade": "고1",
  "variation_type": "number_change"
}
```

생성 요구사항:
- LLM(GPT-4o 또는 Claude)을 활용하여 원본 문제와 동일 개념, 다른 숫자·조건의 문제 생성
- 생성된 문제는 수식 파서로 정답 검증 후 문제은행에 저장
- LaTeX 수식 문법 파싱 성공 여부 확인 (SymPy)
- 생성 요청 후 응답 시간 **5초 이내**

---

## 7. 펜 입력 캡처 및 전송 요구사항

### 7.1 클라이언트 캔버스 구현

#### 7.1.1 iOS (PencilKit 기반)

| 요구사항 | 상세 |
|----------|------|
| SDK | PencilKit (iOS 13+) |
| 지원 입력 | Apple Pencil 1·2세대, 손가락 터치 |
| 필압 반응 | PKStrokePoint의 `force` 값을 활용한 가변 선 굵기 |
| 팜 리젝션 | PencilKit 기본 팜 리젝션 활성화 |
| 캔버스 크기 | 문제 표시 영역 하단 전체 (최소 500pt 높이) |

#### 7.1.2 Android (Ink API 기반)

| 요구사항 | 상세 |
|----------|------|
| SDK | `androidx.ink` (Jetpack Ink) 또는 Android Ink API |
| 지원 입력 | S-Pen, USI 펜, 손가락 터치 |
| 필압 반응 | `MotionEvent.AXIS_PRESSURE` 기반 가변 굵기 |
| 팜 리젝션 | `PointerType.STYLUS` 우선 처리 로직 |
| 저지연 렌더링 | `SurfaceView` 또는 `GLSurfaceView` 활용 |

#### 7.1.3 공통 캔버스 UX 요구사항

- 펜 도구: 굵기 3단계, 색상 5가지 (검정·파랑·빨강·초록·주황)
- 형광펜: 굵기 1단계, 반투명
- 지우개 도구: 스트로크 단위 지우개, 픽셀 지우개
- 올가미: 선택 영역 이동/삭제
- 실행취소(Undo) / 재실행(Redo): 최대 50단계
- 캔버스 확대/축소: 핀치 줌 50% ~ 300%
- 풀이 제출 버튼: 명확한 CTA 위치에 배치

### 7.2 이미지 캡처 및 전처리

#### 7.2.1 캡처 규격

| 항목 | 요구사항 |
|------|----------|
| 출력 포맷 | PNG (투명도 지원) 또는 JPEG (배경 흰색) |
| 해상도 | 최소 1080×1440 px (A4 세로 비율 기준) |
| 색상 공간 | sRGB |
| DPI | 150 DPI 이상 |
| 최대 파일 크기 | 원본 5 MB 이내, 전송 전 압축 후 2 MB 이내 |

#### 7.2.2 클라이언트 사이드 전처리

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

#### 7.2.3 스트로크 메타데이터 수집

제출 데이터에 다음 메타데이터를 선택적으로 포함:

```json
{
  "stroke_count": 42,
  "total_duration_ms": 35000,
  "canvas_size": { "width": 1080, "height": 1440 },
  "input_type": "stylus"
}
```

### 7.3 서버 전송 인터페이스

#### 7.3.1 풀이 제출 API

```
POST /api/v1/submissions
Content-Type: application/json
Authorization: Bearer {JWT}
```

요청 바디:

```json
{
  "user_id": "string (UUID)",
  "problem_id": "string (UUID)",
  "session_id": "string (UUID)",
  "image_base64": "string",
  "image_mime_type": "image/png | image/jpeg",
  "stroke_metadata": {
    "stroke_count": 42,
    "total_duration_ms": 35000,
    "canvas_size": { "width": 1080, "height": 1440 },
    "input_type": "stylus"
  },
  "client_timestamp": "ISO8601",
  "device_info": {
    "platform": "ios | android",
    "os_version": "string",
    "app_version": "string"
  }
}
```

응답 (202 Accepted):

```json
{
  "submission_id": "uuid",
  "status": "received",
  "websocket_url": "wss://api.mathlens.ai/ws/v1/submissions/{submission_id}",
  "estimated_processing_time_ms": 5000
}
```

#### 7.3.2 처리 결과 조회 (폴링)

```
GET /api/v1/submissions/{submission_id}/status
```

#### 7.3.3 실시간 상태 수신 (WebSocket)

```
WS /ws/v1/submissions/{submission_id}
```

| 단계 | 메시지 |
|------|--------|
| 이미지 수신 | `{"stage": "received", "ts": "..."}` |
| 전처리 완료 | `{"stage": "preprocessed", "ts": "..."}` |
| HTR 완료 | `{"stage": "htr_done", "latex_preview": "...", "confidence": 0.96, "ts": "..."}` |
| 분석 완료 | `{"stage": "analysis_done", "result_id": "uuid", "is_correct": true, "ts": "..."}` |
| 오류 발생 | `{"stage": "error", "error_code": "HTR_TIMEOUT", "message": "...", "ts": "..."}` |

---

## 8. AI 인식 엔진 연동 요구사항

### 8.1 서버 사이드 이미지 전처리

| 단계 | 처리 내용 | 기술 옵션 |
|------|-----------|-----------|
| 1. 이진화 | 배경/잉크 분리, Otsu's Threshold | OpenCV |
| 2. 노이즈 제거 | 가우시안 블러, 모폴로지 연산 | OpenCV |
| 3. 기울기 보정 | 필기 라인 기울기 검출 후 회전 | OpenCV |
| 4. 행 분리 | 풀이 행 단위 분리 (Horizontal Projection Profile) | 커스텀 구현 |
| 5. 수식/텍스트 영역 분류 | 수식 영역과 자연어 설명 영역 분리 | YOLO 또는 규칙 기반 |

### 8.2 HTR 엔진 요구사항

| 요구사항 | 상세 |
|----------|------|
| 출력 포맷 | LaTeX (예: `\frac{x^2 + 1}{2x - 3}`) |
| 지원 기호 범위 | 사칙연산, 분수, 루트, 거듭제곱, 극한, 미적분, 행렬, 집합, 확률 기호 |
| 인식 정확도 | 95% 이상 (Character Error Rate 기준, 표준 필기) |
| 응답 시간 | 단일 이미지 기준 **2초 이내** |
| 한글/영문 텍스트 인식 | 90% 이상 (한국어 손글씨 기준) |

### 8.3 LaTeX 후처리 및 구조화

1. **LaTeX 파싱**: 수식 구조를 Abstract Syntax Tree(AST)로 변환
2. **단계 분리**: 등호(`=`), 줄바꿈 패턴 기반 풀이 단계 분리
3. **수식 검증**: SymPy를 통해 수식 문법 유효성 확인
4. **정답 비교**: 제출 답안 LaTeX와 문제 정답 LaTeX의 수학적 동치 여부 판별

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

### 8.4 멀티모달 LLM 연동

HTR 결과(LaTeX 텍스트) 및 원본 이미지를 함께 LLM에 전달:

```
POST /api/v1/analyze
{
  "submission_id": "uuid",
  "problem_id": "uuid",
  "htr_result": {
    "latex": "...",
    "steps": ["step1_latex", ...],
    "confidence": 0.97
  },
  "image_base64": "...",
  "user_id": "uuid"
}
```

LLM 프롬프트 구성 요구사항:
- 문제 원문 포함
- 학습자 학년 및 이전 오류 유형 히스토리 포함 (시스템 프롬프트)
- 인식된 LaTeX 풀이 단계 포함
- 원본 손글씨 이미지 동시 제공 (이미지 인식 불확실 구간 보완)

---

## 9. 전체 데이터 흐름 및 시스템 인터페이스

### 9.1 문제 출제 → 펜 입력 → AI 인식 전체 흐름

```
┌─────────────────────────────────────────────────────────────────┐
│  [1] 문제 출제                                                    │
│                                                                  │
│  앱 시작/다음 문제 요청                                            │
│        │                                                         │
│        ▼                                                         │
│  GET /api/v1/problems/recommend?user_id=...                      │
│        │                                                         │
│        ▼                                                         │
│  문제 추천 서비스                                                  │
│  ├── 학습 이력 조회 (Redis 캐시 또는 PostgreSQL)                   │
│  ├── 취약 개념 기반 문제 선정                                      │
│  └── 난이도 조절 후 문제 반환                                      │
│        │                                                         │
│        ▼                                                         │
│  클라이언트 문제 표시 (상단 영역)                                   │
└─────────────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│  [2] 펜 입력                                                      │
│                                                                  │
│  사용자 펜 입력 (PencilKit / Android Ink API)                      │
│        │                                                         │
│  [제출 버튼 탭]                                                    │
│        │                                                         │
│        ▼                                                         │
│  클라이언트 사이드 전처리                                          │
│  ├── 캔버스 → PNG 캡처                                            │
│  ├── 잉크 영역 크롭                                               │
│  └── Base64 인코딩                                               │
└─────────────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│  [3] 서버 수신 및 저장                                             │
│                                                                  │
│  POST /api/v1/submissions                                        │
│  ├── submission_id 발급 및 즉시 응답 (202 Accepted)               │
│  ├── 이미지 S3 저장 (원본 보존)                                    │
│  └── 처리 큐 (Redis Queue / Celery) 등록                          │
└─────────────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│  [4] AI 인식 파이프라인 (비동기 처리)                               │
│                                                                  │
│  [4-1] 이미지 전처리 (OpenCV)                                     │
│        ├── 이진화 / 노이즈 제거 / 기울기 보정                       │
│        └── 수식 영역 분리                                         │
│        │                                                         │
│  [4-2] HTR 엔진                                                  │
│        ├── Math HTR → LaTeX 변환 (iink SDK / MathPix 등)         │
│        └── Text HTR → 한글·영문 텍스트 변환                        │
│        │                                                         │
│  [4-3] LaTeX 후처리                                              │
│        ├── AST 파싱 및 단계 분리                                   │
│        └── SymPy 정답 동치 비교                                   │
│        │                                                         │
│  [4-4] LLM 풀이 분석                                              │
│        ├── 문제 + 풀이(LaTeX) + 이미지 → LLM 전달                  │
│        └── 오류 분류 및 피드백 생성                                 │
│        │                                                         │
│  [4-5] 결과 저장 및 클라이언트 푸시                                 │
│        └── WebSocket / APNs·FCM 푸시                             │
└─────────────────────────────────────────────────────────────────┘
```

### 9.2 API 인터페이스 요약

| Method | Endpoint | 설명 | 인증 |
|--------|----------|------|------|
| GET | `/api/v1/problems/recommend` | 개인화 문제 추천 | JWT |
| GET | `/api/v1/problems/{id}` | 문제 단건 조회 | JWT |
| POST | `/api/v1/problems/generate` | 유사 문제 LLM 생성 | JWT |
| POST | `/api/v1/submissions` | 펜 입력 풀이 제출 | JWT |
| GET | `/api/v1/submissions/{id}/status` | 처리 상태 폴링 | JWT |
| WS | `/ws/v1/submissions/{id}` | 처리 단계 실시간 수신 | JWT (쿼리 파라미터) |
| GET | `/api/v1/results/{submission_id}` | 최종 분석 결과 조회 | JWT |
| GET | `/api/v1/users/{id}/report` | 학습 리포트 조회 | JWT |

---

## 10. 시스템 아키텍처

### 10.1 전체 구조

```
┌────────────────────────────────────────────────────────┐
│                  모바일 클라이언트                        │
│         (iOS Swift/SwiftUI  |  Android Kotlin/Compose) │
│                                                        │
│  ┌──────────────────────────────────────────────────┐  │
│  │           펜 입력 캔버스 레이어                    │  │
│  │  iOS: PencilKit  |  Android: Custom Ink Canvas   │  │
│  └───────────────────────┬──────────────────────────┘  │
│                          │ Stroke Data / Canvas Image  │
│  ┌──────────────────────────────────────────────────┐  │
│  │      수식 인식 레이어 (MyScript iink SDK)          │  │
│  │  실시간 스트로크 → LaTeX/MathML 변환 (온디바이스)  │  │
│  └───────────────────────┬──────────────────────────┘  │
└──────────────────────────┼─────────────────────────────┘
                           │ LaTeX + 원본 이미지 (HTTPS)
                           ▼
┌────────────────────────────────────────────────────────┐
│                    API Gateway                          │
│              (FastAPI, REST / WebSocket)                │
└───────────────────┬────────────────────────────────────┘
                    │
       ┌────────────┼────────────┬──────────────┐
       ▼            ▼            ▼              ▼
┌───────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐
│ MathPix   │ │ AI 분석  │ │ 문제 생성 │ │ 개념 지식    │
│ Fallback  │ │ 서비스   │ │ 서비스   │ │ 그래프       │
│ 서비스    │ │(GPT-4o / │ │(LLM +    │ │ 서비스       │
│           │ │ Claude)  │ │ 템플릿)  │ │              │
└─────┬─────┘ └─────┬────┘ └─────┬────┘ └──────┬───────┘
      └─────────────┼────────────┘             │
                    ▼                           │
          ┌──────────────────┐                 │
          │   데이터베이스    │◄────────────────┘
          │  PostgreSQL      │
          │  Redis (캐시)    │
          │  S3 (이미지)     │
          └──────────────────┘
```

### 10.2 AI 분석 파이프라인

```
[사용자 펜 입력]
       ↓
[iink SDK 실시간 인식] ──(실패/복잡)──► [MathPix API Fallback]
       ↓
[LaTeX 구조화 데이터]
       ↓
[풀이 단계 파서] → 논리 단계 분리, 수식 단위 파싱
       ↓
[GPT-4o / Claude API]
  - 입력: LaTeX 텍스트 + 원본 캔버스 이미지 (멀티모달)
  - 역할: 개념 이해도 추론 + 오류 분류 + 피드백 문장 생성
       ↓
[피드백 생성기] → 맞춤형 설명 + 유사 문제 생성 요청
       ↓
[LaTeX 렌더링 (KaTeX)] + 오류 하이라이팅 오버레이
       ↓
[사용자 화면 출력]
```

---

## 11. 기술 스택 요구사항

### 11.1 확정 기술 스택 (변경 불가)

| 영역 | 기술 | 비고 |
|------|------|------|
| 백엔드 API 서버 | Python FastAPI | 비동기 처리, WebSocket 지원 |
| 주 데이터베이스 | PostgreSQL | 사용자/학습 데이터 |
| 캐시/큐 | Redis | 세션·캐싱·비동기 큐 브로커 |
| 비동기 작업 큐 | Celery (Redis 브로커) | AI 파이프라인 처리 |
| 이미지 스토리지 | AWS S3 호환 | 풀이 이미지 저장 |
| iOS 클라이언트 | Swift 5.9+ + SwiftUI + PencilKit | iOS 16+ |
| Android 클라이언트 | Kotlin + Jetpack Compose + Ink API | Android 10+ |

### 11.2 협의 가능 기술 스택

| 영역 | 기술 옵션 |
|------|-----------|
| HTR 엔진 | MathPix API, MyScript Math SDK, Pix2Tex, 자체 모델 |
| LLM | OpenAI GPT-4o, Anthropic Claude 3.5+, 자체 파인튜닝 |
| 이미지 전처리 | OpenCV, Pillow, scikit-image |
| LaTeX 파싱 | SymPy, LaTeXML |
| 수식 렌더링 | KaTeX (WebView), iosMath (iOS 네이티브) |
| 개념 지식 그래프 | PostgreSQL 또는 Neo4j |
| 벡터 검색 | pgvector (PostgreSQL 확장) 또는 Pinecone |
| 컨테이너 오케스트레이션 | Docker + ECS / Kubernetes |
| 인증 | OAuth 2.0, JWT, 소셜 로그인 (Google, Apple, Kakao) |
| 모니터링 | Grafana + Prometheus, Sentry |
| CI/CD | GitHub Actions |

---

## 12. UX/UI 설계 방향

### 12.1 핵심 화면 구성

#### 화면 1: 홈 대시보드
- 오늘의 학습 현황 (목표 문제 수, 달성률)
- 최근 오답 유형 요약
- 추천 복습 문제 카드

#### 화면 2: 문제 풀이 화면 (핵심)
- 상단: 문제 표시 영역 (KaTeX 렌더링)
- 중단: iink SDK 수식 입력 캔버스 (전체 화면 확장 가능)
  - 실시간 인식 결과 미리보기 (LaTeX → 수식 렌더링)
  - 인식 오류 수동 수정 버튼
- 하단: 도구 모음 (펜 굵기/색상, 지우개, 실행취소, 제출)

#### 화면 3: AI 피드백 화면
- 풀이 오류 위치 하이라이팅 오버레이
- 오류 유형 배지 (개념 오류 / 계산 실수 등)
- 개념 설명 카드 (스크롤)
- 정석 풀이 애니메이션 재생
- "다시 풀기" / "다음 유사 문제" 버튼

#### 화면 4: 인식 결과 확인·수정
- iink SDK 인식 결과 LaTeX 표시
- 사용자가 잘못 인식된 기호 직접 수정 가능 (인식 정확도 피드백 수집 겸용)

#### 화면 5: 개념 설명 상세
- 개념 정의 및 공식
- 핵심 예제 2~3개
- 관련 개념 링크 (개념 맵)

#### 화면 6: 학습 리포트
- 주간 학습 그래프
- 오답 유형 분포 차트
- 취약 개념 목록

### 12.2 UX 원칙

- **마찰 최소화**: 문제 촬영부터 피드백까지 탭 3회 이내
- **즉각적 피드백**: 분석 중 로딩 화면에서도 진행 상태 시각화
- **인식 결과 투명성**: 사용자가 인식된 수식을 확인하고 수정할 수 있는 인터페이스 제공
- **학습 동기 유지**: 연속 학습일, 개념 습득 배지 등 게임화 요소
- **접근성**: 다크모드, 글자 크기 조절, 고대비 모드 지원

---

## 13. 개발 범위 및 단계

### Phase 1 — MVP (최소 기능 제품)

**목표**: 핵심 학습 루프 검증

| 기능 | 포함 여부 |
|------|-----------|
| 펜 입력 캔버스 (PencilKit / Android Canvas) | ✅ |
| MyScript iink SDK 수식 인식 (중등 수준) | ✅ |
| MathPix API Fallback 인식 | ✅ |
| AI 오답 분석 (GPT-4o, 상위 5개 오류 유형) | ✅ |
| 맞춤형 개념 설명 | ✅ |
| 유사 문제 재출제 (자동 생성) | ✅ |
| 인식 결과 확인·수정 UI | ✅ |
| 기본 학습 이력 저장 | ✅ |
| 소셜 로그인 | ✅ |
| 학부모 대시보드 | ❌ Phase 2 |
| 오프라인 모드 | ❌ Phase 3 |

### Phase 2 — 기능 확장

- 학부모/교사 대시보드
- 고등 수학 전체 범위 확장
- 문제은행 확충 (교과서 연계)
- 개념 맵 시각화
- 푸시 알림 및 학습 리마인더

### Phase 3 — 고도화

- iink SDK 오프라인 모드 최적화 또는 자체 경량 모델 전환
- 온디바이스 AI 추론 (CoreML / TFLite 소형 모델)
- 실시간 협업 풀이 (그룹 스터디)
- 교사 맞춤 문제 출제 도구
- 수능/모의고사 연계 콘텐츠

---

## 14. 성능 및 품질 요구사항

### 14.1 응답 시간 SLA

| 항목 | 목표값 | 최대 허용값 |
|------|--------|------------|
| 문제 추천 API 응답 시간 | 300ms | 1,000ms |
| 문제 생성 (LLM) 응답 시간 | 3초 | 5초 |
| 풀이 제출 접수 응답 (202) | 500ms | 1,000ms |
| HTR 인식 완료 (서버 기준) | 2초 | 4초 |
| 전체 파이프라인 (접수~분석 완료) | 5초 | 10초 |
| 캔버스 렌더링 프레임 속도 | — | ≤ 16ms/frame (60 FPS 이상) |

### 14.2 인식 정확도 KPI

| 지표 | 목표 |
|------|------|
| 수식 HTR 정확도 (표준 필기) | ≥ 95% |
| 수식 HTR 정확도 (비표준 필기) | ≥ 85% |
| 한글 텍스트 HTR 정확도 | ≥ 90% |
| AI 오답 분류 정확도 | ≥ 90% (전문 교사 레이블 기준) |
| 정답 동치 판별 정확도 (SymPy) | ≥ 99% |
| LaTeX → AST 파싱 성공률 | ≥ 98% |

### 14.3 시스템 가용성

| 항목 | 목표 |
|------|------|
| API 서버 가용성 | 99.5% (월간 기준) |
| AI 파이프라인 가용성 | 99.0% |
| 최대 동시 처리 제출 수 | 500건/분 이상 |

### 14.4 확장성

- API 서버: 수평 확장 가능한 스테이트리스 설계 (Docker + ECS/K8s)
- Celery Worker: 부하에 따라 자동 스케일링 (AWS ECS Auto Scaling)
- 문제은행 DB: 읽기 복제본(Read Replica) 지원

---

## 15. 보안 및 개인정보 보호 요구사항

### 15.1 데이터 보안

| 요구사항 | 상세 |
|----------|------|
| 전송 암호화 | TLS 1.3 (HTTPS, WSS) |
| 이미지 저장 | S3 서버 사이드 암호화(AES-256), 사용자 ID와 분리 저장 |
| 인증 | OAuth 2.0 + JWT (Access Token 만료: 1시간, Refresh Token: 30일) |
| API Rate Limiting | 사용자당 제출 60건/시간, IP당 추천 API 100건/분 |
| SQL Injection 방지 | ORM(SQLAlchemy) 파라미터 바인딩 사용 |

### 15.2 개인정보 보호

- 미성년자(만 14세 미만) 데이터 처리 시 법정대리인 동의 프로세스 필수
- 개인정보보호법 및 아동·청소년 관련 법령 준수
- 손글씨 이미지에 포함된 개인 정보(이름 등) 자동 마스킹 (OCR 후 처리)
- 이미지 보존 기간: 계정 활성 기간 + 1년 (이후 자동 삭제)
- MathPix API 호출 시 사용자 식별 정보 포함 금지
- OWASP Mobile Top 10 기준 보안 설계

---

## 16. 일정 계획

### 16.1 전체 개발 일정

| 단계 | 기간 | 주요 산출물 |
|------|------|------------|
| 요구사항 분석 및 설계 | 1~2개월 | 기능 명세서, 시스템 설계서, iink/MathPix PoC |
| Phase 1 개발 | 3~6개월 | MVP 앱 (iOS + Android) |
| 내부 테스트 (알파) | 7개월 | 버그 리포트, 수식 인식 정확도 측정 결과 |
| 베타 테스트 | 8~9개월 | 실사용자 피드백, 인식 오류 패턴 분석 |
| Phase 1 출시 | 10개월 | 앱스토어/플레이스토어 출시 |
| Phase 2 개발 | 11~15개월 | 확장 기능 업데이트 |
| Phase 3 개발 | 16~21개월 | 고도화 기능 업데이트 |

### 16.2 마일스톤

| 마일스톤 | 기준 |
|----------|------|
| M1 — 문제 출제 API 완료 | 문제 추천 및 LLM 생성 API 정상 응답 |
| M2 — 캔버스 + 전송 완료 | iOS/Android에서 펜 입력 후 서버 수신 확인 |
| M3 — HTR 파이프라인 완료 | 샘플 100문항 기준 인식 정확도 95% 달성 |
| M4 — 통합 테스트 완료 | 전체 파이프라인 SLA 충족 |
| M5 — Phase 1 출시 | 앱스토어/플레이스토어 심사 통과 |

### 16.3 제안서 제출 일정

| 항목 | 일정 |
|------|------|
| RFP 공고 | 2026년 5월 21일 |
| 질의응답 마감 | 2026년 6월 4일 |
| 제안서 제출 마감 | 2026년 6월 18일 |
| 제안 발표 (PT) | 2026년 6월 25~26일 |
| 우선협상 대상자 선정 | 2026년 7월 2일 |
| 계약 체결 | 2026년 7월 중 |

> **참고**: 일정은 제안사 규모 및 팀 구성에 따라 조정 협의 가능

---

## 17. 예산 및 산출 기준

### 17.1 예산 범위

| 항목 | 예상 비용 (참고) |
|------|----------------|
| Phase 1 개발 전체 | 2억 ~ 4억 원 |
| MyScript iink SDK 라이선스 (연) | 약 500만 ~ 2,000만 원 (계약 규모에 따라 상이) |
| MathPix API 운영비 (월, MAU 1만) | 약 50만 ~ 130만 원 |
| AI/LLM API 운영비 (월, MAU 1만) | 약 120만 ~ 350만 원 |
| 클라우드 인프라 (월) | 약 100만 ~ 300만 원 |
| 유지보수 (연) | 개발비의 15~20% |

> 위 금액은 참고 범위이며, 제안사는 상세 내역을 별도 제출

### 17.2 제안서 포함 필수 비용 항목

- 인력 투입 계획 (역할별 MM 및 단가)
- MyScript iink SDK 라이선스 방식 및 비용 명시
- MathPix API 예상 호출량 및 비용 산출 근거
- LLM API (GPT-4o 또는 Claude) 예상 토큰 소비 및 비용
- HTR API 단가 포함 상세 비용
- 인프라 구축 및 운영 비용
- QA 및 보안 감사 비용
- 앱스토어 등록 및 유지 비용
- 유지보수 및 기술 지원 조건

---

## 18. 제안사 자격 요건

### 18.1 필수 요건

- 모바일 앱 (iOS + Android) 개발 경험 **3년 이상**
- AI/ML 백엔드 구축 경험 보유
- 교육 관련 앱 개발 실적 **1건 이상**
- 손글씨 인식 또는 이미지 처리 기술 구현 경험
- FastAPI 또는 동급 Python 백엔드 개발 경험 2년 이상
- LLM API 연동 및 프롬프트 엔지니어링 경험

### 18.2 우대 요건

- **MyScript iink SDK 또는 MathPix API 실 적용 경험**
- 수학 수식 인식(Math OCR) 모델 개발·운영 경험
- LLM 기반 서비스 개발 및 운영 경험
- 수학 교육 콘텐츠 또는 에듀테크 도메인 경험
- 개인정보보호 인증 (ISMS, PIMS 등) 보유
- 실시간 WebSocket 기반 서비스 운영 경험
- 에듀테크 서비스 개발 경험

---

## 19. 제안서 제출 요건

### 19.1 필수 제출 항목

1. 회사 소개서 (사업자등록증 사본 포함)
2. 기술 제안서
   - iink SDK 및 MathPix API 통합 방안 상세 기술
   - HTR 엔진 선정 이유 및 정확도 근거 (벤치마크 데이터 포함)
   - AI 분석 파이프라인 설계 (프롬프트 엔지니어링 전략 포함)
   - 수식 인식 정확도 달성 전략 (iink + MathPix + fallback 구성)
   - 전체 데이터 흐름도 (Sequence Diagram)
   - API 명세서 초안
   - 비동기 파이프라인 설계 (Celery Worker 구성 등)
3. 수행 계획서
   - 단계별 일정 (간트 차트)
   - 팀 구성 및 역할
4. 비용 제안서 (세부 항목 명시)
5. 유사 프로젝트 포트폴리오 (최소 2건)

### 19.2 우대 제출 항목

- **수식 인식 PoC 데모** (iink 또는 MathPix 활용 시 가산점)
- HTR 인식 데모 (샘플 이미지 5장 이상 LaTeX 변환 결과 포함)
- 펜 입력 캔버스 프로토타입 (영상 또는 TestFlight/APK)

### 19.3 제출 형식

- 파일 형식: PDF (또는 PPT + PDF 병행)
- 분량: 기술 제안서 30페이지 이내, 비용 제안서 별도
- 제출 방법: 이메일 또는 지정 제출 시스템

---

## 20. 평가 기준

### 20.1 전체 평가 배점

| 평가 항목 | 배점 |
|-----------|------|
| 기술력 (iink SDK + MathPix + LLM 통합 방안의 타당성) | 25점 |
| HTR 파이프라인 설계의 기술적 타당성 | 20점 |
| 개발 경험 및 포트폴리오 | 15점 |
| 문제 출제 시스템 설계 완성도 | 10점 |
| 수행 계획의 현실성 | 10점 |
| 비용 적정성 | 10점 |
| 팀 구성 및 전문성 | 5점 |
| 수식 인식 PoC 데모 완성도 | 5점 |
| **합계** | **100점** |

> 70점 미만 제안사는 협상 대상에서 제외

---

## 21. 부록

### 부록 A. 주요 용어 정의

| 용어 | 정의 |
|------|------|
| HTR | Handwritten Text Recognition. 손글씨를 디지털 텍스트로 변환하는 기술 |
| Math HTR | 수학 기호·수식에 특화된 손글씨 인식 기술 |
| iink SDK | MyScript Interactive Ink SDK. 실시간 스트로크 기반 손글씨 인식 SDK |
| LaTeX | 수학 수식을 표현하는 문서 조판 언어 |
| MathML | 수학 수식을 XML 형태로 표현하는 W3C 표준 마크업 언어 |
| AST | Abstract Syntax Tree. 수식을 트리 구조로 파싱한 결과 |
| LLM | Large Language Model. 대규모 언어 모델 |
| 멀티모달 | 텍스트·이미지 등 여러 형태의 입력을 동시에 처리하는 AI 방식 |
| KaTeX | 웹/앱에서 수식을 빠르게 렌더링하는 JavaScript 라이브러리 |
| SymPy | Python 기반 수식 연산 라이브러리 |
| 완전 학습 | 학습 목표를 완전히 달성할 때까지 반복 학습하는 교육 방법론 |
| 간격 반복 | 망각 곡선에 기반하여 최적 시점에 복습을 유도하는 학습 방법 |
| 스캐폴딩 | 학습자 수준에 맞춰 점진적으로 난이도를 높여 지원하는 교육 방법 |
| Celery | Python 분산 비동기 작업 큐 라이브러리 |
| SLA | Service Level Agreement. 서비스 수준 합의 (응답 시간, 가용성 등) |
| CER | Character Error Rate. 문자 단위 오류율 |
| ExpRate | Expression Recognition Rate. 수식 단위 정답률 |

### 부록 B. 참고 교육과정 범위

- 국내 2022 개정 교육과정 수학 (중학교 1~3학년, 고등학교 공통수학 1·2, 수학 I·II, 미적분, 확률과 통계, 기하)
- 수능 수학 영역 전 범위

### 부록 C. 참고 경쟁 서비스

| 서비스 | 특징 | 차별화 포인트 |
|--------|------|--------------|
| Photomath | 카메라로 문제 인식 후 풀이 제공 | 풀이 과정 분석 없음 |
| Mathway | 수식 입력 후 답 제공 | 오답 원인 분석 없음 |
| 콴다 | 문제 촬영 후 유사 문제 검색 | AI 개념 설명 피드백 부재 |
| GoodNotes | iink SDK 기반 필기 앱 | 수학 학습 피드백 없음 |
| **MathLens AI** | **손글씨 풀이 인식(iink) + 오답 원인 추론(GPT-4o) + 맞춤 반복 학습** | **완전한 학습 루프 제공** |

### 부록 D. MyScript iink SDK 수학 지원 기호 범위

| 카테고리 | 지원 기호 예시 |
|----------|--------------|
| 기본 연산 | +, −, ×, ÷, =, ≠, <, >, ≤, ≥ |
| 분수 | 가로 분수선 (a/b 구조) |
| 지수·첨자 | 위 첨자(xⁿ), 아래 첨자(xₙ) |
| 근호 | √, ∛, ⁿ√ |
| 삼각함수 | sin, cos, tan, csc, sec, cot |
| 로그 | log, ln, logₐ |
| 미적분 | d/dx, ∂, ∫, ∬, lim, Σ, Π |
| 행렬·벡터 | 대괄호 행렬, 화살표 벡터 |
| 집합 | ∈, ∉, ⊂, ⊃, ∪, ∩, ∅ |
| 기타 | ∞, ±, ∓, ∝, ∴, ∵ |

### 부록 E. 수식 인식 샘플 기대 출력

| 입력 손글씨 | 기대 LaTeX 출력 |
|-------------|----------------|
| `2x² + 3x - 5 = 0` | `2x^{2} + 3x - 5 = 0` |
| `∫₀¹ x² dx` | `\int_{0}^{1} x^{2} \, dx` |
| `lim(x→∞) 1/x` | `\lim_{x \to \infty} \frac{1}{x}` |
| `√(a² + b²)` | `\sqrt{a^{2} + b^{2}}` |
| `Σᵢ₌₁ⁿ i` | `\sum_{i=1}^{n} i` |

### 부록 F. 문의처

- 담당 부서: [발주처 부서명]
- 담당자: [담당자명]
- 이메일: [이메일 주소]
- 전화: [전화번호]
- 질의응답: 이메일로만 접수 (답변 공개 게시)

---

*본 문서의 내용은 발주처의 판단에 따라 변경될 수 있으며, 최종 계약서가 우선합니다.*

*© 2026 MathLens AI Project. All rights reserved.*
