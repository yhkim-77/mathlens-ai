# MathLens AI — QA 검증 계획서

**문서 버전:** v1.0
**작성일:** 2026년 5월 22일
**문서 유형:** QA Validation Plan
**작성자:** MathLens AI QA팀
**상태:** 초안 (Draft)

---

## 목차

1. [문서 개요](#1-문서-개요)
2. [검증 전략](#2-검증-전략)
3. [테스트 범위](#3-테스트-범위)
4. [테스트 환경](#4-테스트-환경)
5. [테스트 단계별 계획](#5-테스트-단계별-계획)
6. [품질 기준 및 완료 조건](#6-품질-기준-및-완료-조건)
7. [위험 관리](#7-위험-관리)
8. [일정 및 리소스](#8-일정-및-리소스)
9. [부록](#9-부록)

---

## 1. 문서 개요

### 1.1 목적

본 문서는 MathLens AI 시스템의 품질 보증을 위한 검증 계획을 정의합니다. 테스트 전략, 범위, 환경, 일정, 리소스 및 품질 기준을 명시하여 체계적인 품질 검증을 수행합니다.

### 1.2 범위

**검증 대상:**
- Backend API (FastAPI + SQLAlchemy)
- Mobile Application (Android React Native)
- CI/CD Pipeline (GitHub Actions)
- Integration Points (AI APIs, Database)

**제외 범위:**
- iOS 애플리케이션 (Phase 2)
- 학부모 대시보드 (Phase 2)
- 오프라인 AI 기능 (Phase 3)

### 1.3 참조 문서

- [SRS.md](./SRS.md) — 소프트웨어 요구사항 명세서
- [Functional_Design_Document.md](./Functional_Design_Document.md) — 기능 설계서
- [Test_Cases.md](./Test_Cases.md) — 테스트 케이스 문서
- [CI_CD_Documentation.md](./CI_CD_Documentation.md) — CI/CD 문서

---

## 2. 검증 전략

### 2.1 테스트 피라미드

```
         /\
        /  \  E2E Tests (5%)
       /----\
      / Inte \  Integration Tests (25%)
     /  gration\
    /----------\
   /   Unit     \ Unit Tests (70%)
  /--------------\
```

**테스트 비율:**
- Unit Tests: 70% — 개별 함수, 메서드 검증
- Integration Tests: 25% — 컴포넌트 간 통합 검증
- E2E Tests: 5% — 사용자 시나리오 검증

### 2.2 테스트 유형

| 테스트 유형 | 설명 | 도구 | 책임자 |
|------------|------|------|--------|
| **Unit Test** | 개별 함수/메서드 단위 테스트 | pytest, Jest | 개발자 |
| **Integration Test** | API 엔드포인트, DB 연동 테스트 | pytest, Supertest | 개발자/QA |
| **E2E Test** | 사용자 시나리오 기반 전체 플로우 | Detox, Playwright | QA |
| **Performance Test** | 응답 시간, 처리량, 부하 테스트 | Locust, k6 | QA |
| **Security Test** | 인증, 권한, SQL Injection, XSS | OWASP ZAP, Bandit | 보안팀/QA |
| **Usability Test** | 사용자 경험, UI/UX 검증 | Manual Testing | QA/UX팀 |
| **Regression Test** | 기존 기능 영향도 검증 | 자동화 테스트 스위트 | QA |

### 2.3 자동화 전략

**자동화 우선순위:**
1. **High Priority**: Unit tests, API integration tests, 핵심 비즈니스 로직
2. **Medium Priority**: E2E 주요 사용자 플로우, 성능 테스트
3. **Low Priority**: UI 세부 검증, 에러 메시지 문구

**자동화 비율 목표:**
- Backend: 80% 자동화
- Mobile: 60% 자동화
- E2E: 40% 자동화

---

## 3. 테스트 범위

### 3.1 기능별 테스트 범위

#### 3.1.1 Backend API

| 기능 모듈 | 테스트 범위 | 우선순위 |
|----------|------------|---------|
| **인증 (Auth)** | 회원가입, 로그인, JWT 발급/갱신, 권한 검증 | Critical |
| **풀이 분석 (Analyze)** | 동기/비동기 분석, GPT-4o 통합, 오류 분류 | Critical |
| **제출 관리 (Submissions)** | 비동기 처리, 상태 조회, WebSocket 통신 | Critical |
| **문제 관리 (Problems)** | CRUD, 추천 알고리즘, AI 생성 | High |
| **사용자 리포트 (Users)** | 학습 리포트, 개념 습득, 오답 노트 | High |
| **개념 관리 (Concepts)** | CRUD, AI 개념 설명 | Medium |

#### 3.1.2 Mobile Application

| 기능 모듈 | 테스트 범위 | 우선순위 |
|----------|------------|---------|
| **로그인/회원가입** | 소셜 로그인 (Kakao, Google, Apple), 세션 유지 | Critical |
| **펜 입력 캔버스** | 스타일러스 입력, 도구 선택, 실시간 렌더링 | Critical |
| **손글씨 인식** | iink SDK 통합, LaTeX 변환, MathPix 폴백 | Critical |
| **풀이 제출 및 결과** | 비동기 제출, 실시간 상태 업데이트, 피드백 표시 | Critical |
| **문제 풀이** | 문제 목록, 추천, 카메라 입력 | High |
| **학습 대시보드** | 리포트 조회, 오답 노트, 진도 추적 | High |
| **오프라인 모드** | 로컬 캐싱, 동기화 | Medium |

### 3.2 비기능 요구사항 테스트

| 비기능 요구사항 | 검증 기준 | 테스트 방법 |
|---------------|----------|------------|
| **성능** | 동기 분석 ≤ 5초, 비동기 제출 ≤ 1초 응답 | Locust 부하 테스트 |
| **확장성** | 동시 사용자 1,000명 처리 | k6 스트레스 테스트 |
| **보안** | JWT 검증, SQL Injection 방어, HTTPS 통신 | OWASP ZAP 스캔 |
| **가용성** | 99.5% uptime | 모니터링 + 헬스체크 |
| **호환성** | Android API 24+, Python 3.11+, PostgreSQL 14+ | 다중 환경 테스트 |

---

## 4. 테스트 환경

### 4.1 환경 구성

| 환경 | 용도 | 인프라 | 데이터 |
|------|------|--------|--------|
| **Development** | 개발자 로컬 테스트 | Docker Compose | Mock/Seed 데이터 |
| **CI** | 자동화 테스트 (PR/Push) | GitHub Actions | In-memory SQLite |
| **Staging** | QA 검증 환경 | AWS/GCP | 익명화된 프로덕션 데이터 |
| **Production** | 실제 서비스 환경 | AWS/GCP | 실제 사용자 데이터 |

### 4.2 Backend 테스트 환경

**소프트웨어 요구사항:**
- Python 3.11
- PostgreSQL 14+ (staging/prod), SQLite (dev/CI)
- Redis (비동기 큐)
- Docker 24+

**환경 변수:**
```bash
DATABASE_URL=sqlite+aiosqlite:///./test.db
SECRET_KEY=test-secret-key
OPENAI_API_KEY=sk-test-mock-key
ENVIRONMENT=test
```

### 4.3 Mobile 테스트 환경

**Android:**
- Android API 24 (Android 7.0) ~ API 34 (Android 14)
- 에뮬레이터: Pixel 5, Pixel 6, Galaxy S21
- 실기기: Samsung Galaxy A52, Pixel 7

**iOS (Phase 2):**
- iOS 14.0+
- 시뮬레이터: iPhone 12, iPhone 14, iPad Air

### 4.4 테스트 데이터

**데이터 준비 전략:**
1. **Seed Data**: 초기 개념, 문제 샘플 (backend/tests/fixtures/)
2. **Mock Data**: AI API 응답 모킹 (pytest-mock)
3. **Synthetic Data**: 익명화된 학습 데이터 (Faker)
4. **Production Subset**: Staging 환경용 익명화 데이터

---

## 5. 테스트 단계별 계획

### 5.1 Phase 1: Unit Testing (Week 1-2)

**목표:** 개별 컴포넌트 단위 테스트 커버리지 70% 이상

**Backend Unit Tests:**
- [ ] 인증 서비스 (JWT 생성/검증, bcrypt)
- [ ] 분석 서비스 (GPT-4o 모킹, 오류 분류 로직)
- [ ] 추천 서비스 (간격 반복 알고리즘, 개념 습득 계산)
- [ ] 데이터베이스 모델 (CRUD, 관계, 제약조건)
- [ ] 유틸리티 함수 (날짜 계산, 데이터 검증)

**도구:** pytest, pytest-asyncio, pytest-mock

**완료 조건:**
- 커버리지 ≥ 70%
- 모든 테스트 PASS
- CI 파이프라인 통합

### 5.2 Phase 2: Integration Testing (Week 3-4)

**목표:** API 엔드포인트, DB 연동, 외부 서비스 통합 검증

**API Integration Tests:**
- [ ] 인증 플로우 (회원가입 → 로그인 → 토큰 갱신)
- [ ] 풀이 제출 플로우 (제출 → 상태 조회 → 결과 조회)
- [ ] 문제 추천 플로우 (사용자 히스토리 → 추천 → AI 생성)
- [ ] WebSocket 통신 (연결 → 메시지 전송 → 연결 해제)

**Database Integration:**
- [ ] 트랜잭션 롤백/커밋
- [ ] Foreign key 제약조건
- [ ] 동시성 제어 (Optimistic/Pessimistic locking)

**도구:** pytest, httpx, TestClient, asyncio

**완료 조건:**
- 주요 API 플로우 테스트 완료
- DB 마이그레이션 검증
- 외부 API 모킹 완료

### 5.3 Phase 3: E2E Testing (Week 5-6)

**목표:** 사용자 시나리오 기반 전체 플로우 검증

**Critical User Journeys:**
1. 신규 사용자 온보딩 (회원가입 → 프로필 설정 → 첫 문제 풀이)
2. 문제 풀이 및 피드백 (문제 선택 → 펜 입력 → 제출 → 결과 확인)
3. 학습 리포트 조회 (대시보드 → 오답 노트 → 개념 복습)
4. AI 유사 문제 생성 (틀린 문제 → 유사 문제 생성 → 재도전)

**도구:** Detox (React Native), Playwright (웹 관리자)

**완료 조건:**
- 4개 핵심 시나리오 자동화
- Staging 환경 검증 완료

### 5.4 Phase 4: Performance & Security Testing (Week 7)

**Performance Testing:**
- [ ] 부하 테스트: 동시 사용자 500명, 평균 응답 시간 ≤ 2초
- [ ] 스트레스 테스트: 1,000명 부하, 에러율 ≤ 1%
- [ ] Spike 테스트: 갑작스러운 트래픽 증가 대응

**도구:** Locust, k6

**Security Testing:**
- [ ] OWASP Top 10 취약점 스캔
- [ ] SQL Injection, XSS, CSRF 방어 검증
- [ ] JWT 토큰 만료, 권한 검증
- [ ] 민감 정보 암호화 (비밀번호, API 키)

**도구:** OWASP ZAP, Bandit, Safety

**완료 조건:**
- 성능 기준 충족
- Critical/High 보안 이슈 0건

### 5.5 Phase 5: Regression & UAT (Week 8)

**Regression Testing:**
- [ ] 전체 자동화 테스트 스위트 재실행
- [ ] 주요 기능 수동 회귀 테스트
- [ ] 버그 픽스 재검증

**User Acceptance Testing (UAT):**
- [ ] 베타 사용자 10명 초청
- [ ] 실제 문제 풀이 시나리오 테스트
- [ ] 피드백 수집 및 개선사항 반영

**완료 조건:**
- 자동화 테스트 PASS 100%
- UAT 만족도 ≥ 8/10
- Critical/High 버그 0건

---

## 6. 품질 기준 및 완료 조건

### 6.1 테스트 커버리지 목표

| 컴포넌트 | 목표 커버리지 | 측정 도구 |
|---------|-------------|----------|
| Backend Unit Tests | ≥ 70% | pytest-cov |
| Backend Integration Tests | ≥ 60% | pytest-cov |
| Mobile Unit Tests | ≥ 50% | Jest |
| E2E Tests | ≥ 40% (주요 플로우) | Detox |

### 6.2 버그 우선순위 및 해결 기준

| 우선순위 | 정의 | 해결 기한 |
|---------|------|----------|
| **Critical** | 시스템 크래시, 데이터 손실, 보안 취약점 | 즉시 (24시간) |
| **High** | 핵심 기능 동작 불가, 심각한 UX 문제 | 3일 이내 |
| **Medium** | 비핵심 기능 오류, 경미한 UX 문제 | 1주일 이내 |
| **Low** | UI 오타, 개선 제안 | 2주일 이내 또는 다음 릴리즈 |

### 6.3 릴리즈 품질 게이트

**릴리즈 가능 조건:**
- [ ] 모든 자동화 테스트 PASS
- [ ] Critical/High 버그 0건
- [ ] 테스트 커버리지 목표 달성
- [ ] 성능 기준 충족
- [ ] 보안 스캔 통과
- [ ] UAT 승인

---

## 7. 위험 관리

### 7.1 주요 위험 요소

| 위험 | 영향도 | 발생 가능성 | 완화 전략 |
|------|--------|-----------|----------|
| **AI API 응답 불안정** | High | Medium | Mock 데이터 준비, 재시도 로직, 폴백 모델 |
| **손글씨 인식 정확도 낮음** | High | Medium | MathPix 폴백, 수동 수정 UI, 정확도 임계값 |
| **동시 접속 부하** | Medium | High | 캐싱, 큐 시스템, 수평 확장 |
| **외부 의존성 장애** | Medium | Low | Health check, Circuit breaker, 알림 시스템 |
| **테스트 환경 불안정** | Low | Medium | Docker 일관성, CI 캐싱, 환경 격리 |

### 7.2 버그 트래킹

**도구:** GitHub Issues

**워크플로우:**
1. QA가 버그 발견 → Issue 생성 (우선순위, 라벨 태그)
2. 개발자 할당 → 수정 → PR 생성
3. QA 재검증 → Issue 닫기

**라벨:**
- `bug`, `critical`, `high`, `medium`, `low`
- `backend`, `mobile`, `ci-cd`
- `needs-verification`, `in-progress`, `verified`

---

## 8. 일정 및 리소스

### 8.1 테스트 일정 (8주)

| 주차 | 단계 | 활동 | 담당 |
|------|------|------|------|
| **Week 1-2** | Unit Testing | Backend/Mobile 단위 테스트 작성 | 개발자 |
| **Week 3-4** | Integration Testing | API, DB 통합 테스트 | 개발자/QA |
| **Week 5-6** | E2E Testing | 사용자 시나리오 테스트 자동화 | QA |
| **Week 7** | Performance & Security | 부하/보안 테스트 | QA/보안팀 |
| **Week 8** | Regression & UAT | 회귀 테스트, 베타 테스트 | QA/베타 사용자 |

### 8.2 리소스 계획

**인력:**
- Backend 개발자 2명
- Mobile 개발자 2명
- QA 엔지니어 2명
- 보안 엔지니어 1명 (파트타임)

**인프라:**
- GitHub Actions (CI/CD)
- Staging 서버 (AWS/GCP)
- 테스트 기기 (Android 에뮬레이터/실기기)

---

## 9. 부록

### 9.1 테스트 체크리스트

**Backend API:**
- [ ] 모든 엔드포인트 2xx/4xx/5xx 응답 테스트
- [ ] JWT 인증/권한 검증
- [ ] 입력 데이터 검증 (스키마, 타입, 범위)
- [ ] DB 트랜잭션 롤백/커밋
- [ ] 비동기 작업 큐 처리
- [ ] WebSocket 연결 및 메시지 전송
- [ ] 에러 핸들링 및 로깅

**Mobile Application:**
- [ ] 로그인/회원가입 플로우
- [ ] 펜 입력 캔버스 (터치, 스타일러스)
- [ ] 손글씨 인식 및 LaTeX 변환
- [ ] 비동기 제출 및 실시간 상태 업데이트
- [ ] 오프라인 모드 및 동기화
- [ ] 푸시 알림
- [ ] 다양한 화면 크기 (폰, 태블릿)

### 9.2 참고 자료

- [Test_Cases.md](./Test_Cases.md) — 상세 테스트 케이스 문서
- [CI_CD_Documentation.md](./CI_CD_Documentation.md) — CI/CD 파이프라인 문서
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [pytest Documentation](https://docs.pytest.org/)
- [Detox Documentation](https://wix.github.io/Detox/)

---

**문서 이력:**

| 버전 | 날짜 | 작성자 | 변경 내용 |
|------|------|--------|----------|
| v1.0 | 2026-05-22 | QA팀 | 초안 작성 |
