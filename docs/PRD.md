# MathLens AI — 제품 요구사항 문서 (PRD)

**문서 버전:** v1.0  
**작성일:** 2026년 5월 21일  
**문서 유형:** Product Requirements Document (PRD)  
**작성자:** MathLens AI 제품팀  
**상태:** 초안 (Draft)

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
7. [화면 흐름 (User Flow)](#7-화면-흐름-user-flow)
8. [API 명세 (핵심)](#8-api-명세-핵심)
9. [데이터 모델](#9-데이터-모델)
10. [출시 기준 (Definition of Done)](#10-출시-기준-definition-of-done)
11. [리스크 및 완화 방안](#11-리스크-및-완화-방안)
12. [성공 지표 (KPI)](#12-성공-지표-kpi)
13. [변경 이력](#13-변경-이력)

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

### 1.3 제품 범위 (In Scope / Out of Scope)

| 항목 | Phase 1 | Phase 2 | Phase 3 |
|------|---------|---------|---------|
| 펜 수식 인식 (iink SDK) | ✅ | ✅ | ✅ |
| AI 오답 분석 (GPT-4o) | ✅ | ✅ | ✅ |
| 유사 문제 자동 생성 | ✅ | ✅ | ✅ |
| 카메라 문제 인식 | ✅ | ✅ | ✅ |
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
4. 서버에 LaTeX + 원본 이미지 전송
5. GPT-4o가 오답 유형 분류 + 피드백 문장 생성 (3~5초)
6. 피드백 화면에서 틀린 단계 하이라이팅 + 개념 설명 카드 표시
7. "다시 풀기" 탭 → 같은 유형 다른 숫자의 문제 자동 생성
8. 연속 3회 정답 시 "해당 개념 습득 완료" 배지 표시
```

### 3.2 사용자 스토리 목록

| ID | As a... | I want to... | So that... | 우선순위 |
|----|---------|-------------|------------|---------|
| US-01 | 학생 | 펜으로 수학 풀이를 쓰면 실시간으로 수식이 인식되는 것을 보고 싶다 | 인식 오류를 즉시 확인하고 수정할 수 있다 | Must Have |
| US-02 | 학생 | 풀이를 제출하면 어느 단계에서 틀렸는지 정확히 알고 싶다 | 단순 정오가 아닌 원인을 파악할 수 있다 | Must Have |
| US-03 | 학생 | 내 수준에 맞는 설명으로 틀린 개념을 다시 배우고 싶다 | 개념 오류를 스스로 교정할 수 있다 | Must Have |
| US-04 | 학생 | 틀린 문제와 비슷한 유형의 문제를 바로 다시 풀고 싶다 | 같은 실수를 반복하지 않는지 확인할 수 있다 | Must Have |
| US-05 | 학생 | 교재 문제를 카메라로 찍어 앱에 입력하고 싶다 | 별도로 문제를 입력하는 번거로움이 없다 | Must Have |
| US-06 | 학생 | 내가 자주 틀리는 개념이 어떤 것인지 한눈에 보고 싶다 | 취약점을 집중 보완할 수 있다 | Should Have |
| US-07 | 학부모 | 자녀의 주간 학습 현황과 취약 개념을 요약해서 보고 싶다 | 학습 관리를 적극적으로 할 수 있다 | Should Have (Phase 2) |
| US-08 | 학생 | 인터넷이 없어도 수식 인식과 기본 학습을 하고 싶다 | 장소에 구애받지 않고 공부할 수 있다 | Nice to Have (Phase 3) |

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

#### FR-CANVAS-03: 캔버스 제스처

- 두 손가락 핀치: 확대/축소 (50% ~ 300%)
- 두 손가락 스크롤: 캔버스 이동
- Apple Pencil 더블 탭: 이전 도구 전환 (iOS)

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

#### FR-AI-01: 풀이 단계 분해

| 항목 | 내용 |
|------|------|
| 설명 | 인식된 LaTeX 풀이를 논리적 단계로 자동 분리 |
| 구현 | 백엔드 파서 (정규식 + LLM 보완): 등호/부등호 기준 단계 분리 |
| 출력 형식 | `[{"step": 1, "latex": "2x + 3 = 7", "type": "equation"}, ...]` |

#### FR-AI-02: 오답 유형 분류

| 항목 | 내용 |
|------|------|
| 설명 | GPT-4o에게 문제 + 풀이 단계 + 원본 이미지를 전달하여 오답 원인 분류 |
| 분류 체계 | 개념 오류 / 절차 오류 / 계산 실수 / 문제 이해 오류 (4대 유형, 12 세부 항목) |
| 출력 형식 | `{"error_type": "conceptual", "error_subtype": "formula_confusion", "error_step": 2, "confidence": 0.92}` |
| 정확도 목표 | 전문 교사 레이블 대비 90% 일치 |

#### FR-AI-03: 피드백 문장 생성

| 항목 | 내용 |
|------|------|
| 설명 | 오류 유형 및 학년 수준에 맞는 한국어 개념 설명 생성 |
| 입력 | 오류 유형, 관련 개념 ID, 학습자 학년, 이전 오답 이력 |
| 출력 | 설명 텍스트 (500자 이내) + 관련 공식 LaTeX + 예제 풀이 LaTeX |
| 말투 | 학생이 이해하기 쉬운 구어체 (반말 설정 가능) |

#### FR-AI-04: 유사 문제 생성

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
| 입력 | 바운딩 박스 좌표 (iink SDK 또는 Mathpix API 반환값 활용) |

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
| 풀이 제출 후 AI 분석 완료 | P95 기준 5초 이내 |
| 앱 콜드 스타트 | 3초 이내 (iOS/Android) |
| API 서버 응답 시간 | P99 기준 2초 이내 (AI 분석 제외) |
| 동시 접속자 | 1,000 CCU 이상 처리 (AWS ECS Auto Scaling) |

### 5.2 신뢰성

- 서비스 가용성: 99.5% 이상 (월 기준)
- AI API 다운 시: MathPix Fallback → GPT-4o Fallback → 수동 확인 모드 순서로 대체
- 로컬 캐시: 마지막 10개 문제 및 피드백 결과 로컬 저장 (오프라인 열람)

### 5.3 보안

- 전송 암호화: TLS 1.3
- 인증: JWT (Access Token 1시간, Refresh Token 30일)
- 미성년자 개인정보: 수집 최소화, 법정대리인 동의 프로세스
- 풀이 이미지: 분석 후 30일 경과 시 자동 삭제 (설정 가능)
- MathPix API 호출 시 사용자 식별 정보 포함 금지
- OWASP Mobile Top 10 기준 보안 설계

### 5.4 접근성

- 다크모드 지원
- 글자 크기: 시스템 Dynamic Type (iOS) / 텍스트 크기 조절 (Android) 연동
- 고대비 모드 지원
- VoiceOver / TalkBack 핵심 UI 지원

### 5.5 현지화

- 1차 출시: 한국어 전용
- 2차 확장 고려: 영어, 일본어 (데이터 구조 i18n 설계)

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
| 주의 | 두 API 모두 인터넷 필수, 비용 모니터링 필수 |

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
    │     · 실시간 수식 미리보기
    │     · 도구 모음
    │       ↓ (제출)
    │   [분석 중 로딩] (1~5초)
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

### POST `/api/v1/solutions/analyze`
풀이 이미지와 LaTeX를 분석하여 오답 유형 및 피드백을 반환합니다.

**Request**
```json
{
  "problem_id": "prob_12345",
  "canvas_image_base64": "<Base64 PNG>",
  "recognized_latex": "2x + 3 = 7 \\\\ 2x = 4 \\\\ x = 3",
  "student_grade": "middle_2"
}
```

**Response**
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

### POST `/api/v1/problems/generate`
오답 유형 기반으로 유사 문제를 생성합니다.

**Request**
```json
{
  "source_problem_id": "prob_12345",
  "error_type": "procedural",
  "concept_id": "concept_linear_equation",
  "difficulty": "medium",
  "student_grade": "middle_2"
}
```

**Response**
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

### GET `/api/v1/users/{user_id}/report`
학습자 리포트를 조회합니다.

**Response (요약)**
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

### 주요 테이블 (PostgreSQL)

```sql
-- 사용자
users (
  id UUID PRIMARY KEY,
  email VARCHAR UNIQUE,
  grade VARCHAR,         -- middle_1 ~ high_3, reexaminee
  created_at TIMESTAMP,
  last_active_at TIMESTAMP
)

-- 문제
problems (
  id UUID PRIMARY KEY,
  latex TEXT NOT NULL,
  answer_latex TEXT,
  concept_ids UUID[],
  difficulty SMALLINT,   -- 1(하) ~ 5(상)
  grade VARCHAR,
  source VARCHAR,        -- bank | generated | user_camera
  curriculum_year INT    -- 2022
)

-- 풀이 세션
solution_sessions (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users,
  problem_id UUID REFERENCES problems,
  canvas_image_s3_key TEXT,
  recognized_latex TEXT,
  submitted_at TIMESTAMP
)

-- AI 분석 결과
analysis_results (
  id UUID PRIMARY KEY,
  session_id UUID REFERENCES solution_sessions,
  is_correct BOOLEAN,
  error_type VARCHAR,    -- conceptual|procedural|computational|comprehension
  error_subtype VARCHAR,
  error_step SMALLINT,
  feedback_text TEXT,
  correct_solution_latex TEXT,
  confidence NUMERIC,
  llm_model VARCHAR,     -- gpt-4o | claude-3.5-sonnet
  created_at TIMESTAMP
)

-- 개념 습득 현황
concept_mastery (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users,
  concept_id UUID,
  status VARCHAR,        -- learning | mastered | review_due
  consecutive_correct SMALLINT,
  next_review_at TIMESTAMP,
  updated_at TIMESTAMP
)
```

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
- [ ] 학습 리포트 기본 화면 구현 완료
- [ ] 소셜 로그인 3종 (Apple, Google, Kakao) 정상 동작

#### 품질 기준
- [ ] 크래시율: < 0.1% (Firebase Crashlytics 기준)
- [ ] 앱 스토어 심사 가이드라인 준수 (특히 아동 개인정보 처리)
- [ ] 성능: 풀이 제출 → AI 분석 P95 < 5초
- [ ] 보안: OWASP Mobile Top 10 취약점 점검 완료

#### 콘텐츠 기준
- [ ] 문제은행: 중학교 1~3학년 각 단원별 최소 50문제 이상
- [ ] 개념 설명 DB: 중학교 수학 전 단원 커버

---

## 11. 리스크 및 완화 방안

| 리스크 | 가능성 | 영향도 | 완화 방안 |
|--------|--------|--------|-----------|
| MyScript iink SDK 라이선스 비용 초과 | 중 | 중 | Phase 1은 개발자 라이선스 활용, 출시 전 기업 라이선스 협상 |
| GPT-4o API 비용 급증 | 중 | 높음 | 응답 캐싱 (Redis), 짧은 풀이는 GPT-4o mini 사용, 예산 알림 설정 |
| 수식 인식 정확도 미달 (95% 미만) | 중 | 높음 | 인식 결과 수동 수정 UI 필수 제공, 사용자 교정 데이터 누적 |
| 미성년자 개인정보 규제 이슈 | 낮음 | 매우 높음 | 법무팀 사전 검토, 개인정보 수집 최소화 설계 |
| OpenAI API 다운타임 | 낮음 | 높음 | Claude API Fallback 구성, 서킷 브레이커 패턴 적용 |
| 앱스토어 심사 거절 | 낮음 | 중 | Apple/Google 가이드라인 사전 검토, 심사 2주 여유 |

---

## 12. 성공 지표 (KPI)

### 12.1 제품 성능 지표

| KPI | 목표 (Phase 1 출시 3개월 후) |
|-----|------|
| 수식 인식 정확도 | ≥ 95% |
| AI 오답 분류 정확도 | ≥ 90% |
| 풀이 분석 P95 응답 시간 | ≤ 5초 |
| 앱 크래시율 | ≤ 0.1% |

### 12.2 비즈니스 지표

| KPI | 목표 (출시 3개월 후) |
|-----|------|
| MAU | 10,000 이상 |
| D7 Retention | ≥ 50% |
| D30 Retention | ≥ 30% |
| 일 평균 풀이 제출 수 | MAU × 2 이상 |
| 유료 전환율 (프리미엄) | ≥ 5% |

### 12.3 학습 효과 지표

| KPI | 목표 |
|-----|------|
| 동일 유형 3회 이내 정답률 | ≥ 70% |
| 개념 습득 완료 후 2주 복습 정답률 | ≥ 80% |
| 사용자 만족도 (NPS) | ≥ 40 |

---

## 13. 변경 이력

| 버전 | 날짜 | 변경 내용 | 작성자 |
|------|------|-----------|--------|
| v1.0 | 2026-05-21 | 최초 작성 — RFP v2.0 기반 PRD 전면 작성 | MathLens AI 제품팀 |

---

*본 문서는 내부 참고용이며, 외부 공개 시 기술 결정사항 및 비용 관련 항목은 편집이 필요합니다.*

*© 2026 MathLens AI Project. All rights reserved.*
