# MathLens AI — 테스트 케이스 (Test Cases)

**문서 버전:** v1.0
**작성일:** 2026년 5월 22일
**문서 유형:** Test Case Specification
**작성자:** MathLens AI QA팀
**상태:** 초안 (Draft)

---

## 목차

1. [문서 개요](#1-문서-개요)
2. [Backend API 테스트 케이스](#2-backend-api-테스트-케이스)
3. [Mobile Application 테스트 케이스](#3-mobile-application-테스트-케이스)
4. [Integration 테스트 케이스](#4-integration-테스트-케이스)
5. [Performance 테스트 케이스](#5-performance-테스트-케이스)
6. [Security 테스트 케이스](#6-security-테스트-케이스)
7. [부록](#7-부록)

---

## 1. 문서 개요

### 1.1 목적

본 문서는 MathLens AI 시스템의 상세 테스트 케이스를 정의합니다. 각 테스트 케이스는 실행 가능한 단계, 예상 결과, 우선순위를 포함합니다.

### 1.2 테스트 케이스 형식

| 필드 | 설명 |
|------|------|
| **TC ID** | 테스트 케이스 고유 식별자 |
| **제목** | 테스트 케이스 이름 |
| **우선순위** | Critical / High / Medium / Low |
| **전제조건** | 테스트 실행 전 필요한 조건 |
| **테스트 단계** | 실행할 단계들 |
| **예상 결과** | 예상되는 시스템 동작 |
| **실제 결과** | 실행 후 기록 |
| **상태** | Pass / Fail / Blocked / Not Run |

### 1.3 참조 문서

- [QA_Validation_Plan.md](./QA_Validation_Plan.md) — QA 검증 계획서
- [SRS.md](./SRS.md) — 요구사항 명세서
- [Functional_Design_Document.md](./Functional_Design_Document.md) — 기능 설계서

---

## 2. Backend API 테스트 케이스

### 2.1 인증 (Authentication)

#### TC-AUTH-001: 회원가입 성공
- **우선순위:** Critical
- **전제조건:** 데이터베이스 초기화
- **테스트 단계:**
  1. POST `/api/v1/auth/register` 요청
  2. Body: `{"username": "testuser", "email": "test@example.com", "password": "SecurePass123!", "grade_level": 8}`
- **예상 결과:**
  - HTTP 201 Created
  - 응답 Body: `{"id": 1, "username": "testuser", "email": "test@example.com", "grade_level": 8}`
  - 비밀번호는 bcrypt 해시되어 저장
- **실제 결과:**
- **상태:** Not Run

---

#### TC-AUTH-002: 중복 이메일 회원가입 실패
- **우선순위:** High
- **전제조건:** `test@example.com` 이메일로 사용자 이미 존재
- **테스트 단계:**
  1. POST `/api/v1/auth/register` 요청
  2. Body: `{"username": "newuser", "email": "test@example.com", "password": "Pass123!", "grade_level": 7}`
- **예상 결과:**
  - HTTP 400 Bad Request
  - 응답 Body: `{"detail": "Email already registered"}`
- **실제 결과:**
- **상태:** Not Run

---

#### TC-AUTH-003: 로그인 성공 및 JWT 발급
- **우선순위:** Critical
- **전제조건:** 사용자 등록 완료 (`test@example.com` / `SecurePass123!`)
- **테스트 단계:**
  1. POST `/api/v1/auth/token` 요청
  2. Form Data: `username=test@example.com&password=SecurePass123!`
- **예상 결과:**
  - HTTP 200 OK
  - 응답 Body: `{"access_token": "eyJ...", "token_type": "bearer", "expires_in": 3600}`
  - JWT 토큰 유효성 검증 (서명, 만료 시간)
- **실제 결과:**
- **상태:** Not Run

---

#### TC-AUTH-004: 잘못된 비밀번호 로그인 실패
- **우선순위:** Critical
- **전제조건:** 사용자 등록 완료
- **테스트 단계:**
  1. POST `/api/v1/auth/token` 요청
  2. Form Data: `username=test@example.com&password=WrongPassword`
- **예상 결과:**
  - HTTP 401 Unauthorized
  - 응답 Body: `{"detail": "Incorrect username or password"}`
- **실제 결과:**
- **상태:** Not Run

---

#### TC-AUTH-005: JWT 토큰 갱신
- **우선순위:** High
- **전제조건:** 유효한 JWT 토큰 보유
- **테스트 단계:**
  1. POST `/api/v1/auth/refresh` 요청
  2. Header: `Authorization: Bearer <old_token>`
- **예상 결과:**
  - HTTP 200 OK
  - 응답 Body: `{"access_token": "eyJ...", "token_type": "bearer", "expires_in": 3600}`
  - 새 토큰 발급, 기존 토큰과 다름
- **실제 결과:**
- **상태:** Not Run

---

#### TC-AUTH-006: 만료된 JWT 토큰 거부
- **우선순위:** Critical
- **전제조건:** 만료된 JWT 토큰 (만료 시간 3600초 경과)
- **테스트 단계:**
  1. GET `/api/v1/auth/me` 요청
  2. Header: `Authorization: Bearer <expired_token>`
- **예상 결과:**
  - HTTP 401 Unauthorized
  - 응답 Body: `{"detail": "Token expired"}`
- **실제 결과:**
- **상태:** Not Run

---

### 2.2 풀이 분석 (Analysis)

#### TC-ANALYZE-001: 동기 풀이 분석 성공
- **우선순위:** Critical
- **전제조건:**
  - 인증된 사용자
  - 유효한 문제 ID (`problem_id=1`)
- **테스트 단계:**
  1. POST `/api/v1/analyze` 요청
  2. Header: `Authorization: Bearer <token>`
  3. Body:
  ```json
  {
    "problem_id": 1,
    "user_solution_latex": "x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}",
    "user_solution_steps": ["1단계: 근의 공식 적용", "2단계: 계산"],
    "image_base64": null
  }
  ```
- **예상 결과:**
  - HTTP 200 OK
  - 응답 Body:
  ```json
  {
    "is_correct": true,
    "error_type": null,
    "feedback": "정답입니다! 근의 공식을 올바르게 적용했습니다.",
    "concept_id": 5
  }
  ```
- **실제 결과:**
- **상태:** Not Run

---

#### TC-ANALYZE-002: 오답 분석 및 피드백 생성
- **우선순위:** Critical
- **전제조건:**
  - 인증된 사용자
  - 문제 ID 1, 정답: `x = 2`
- **테스트 단계:**
  1. POST `/api/v1/analyze` 요청
  2. Body:
  ```json
  {
    "problem_id": 1,
    "user_solution_latex": "x = 4",
    "user_solution_steps": ["1단계: 2x = 4", "2단계: x = 4"]
  }
  ```
- **예상 결과:**
  - HTTP 200 OK
  - 응답 Body:
  ```json
  {
    "is_correct": false,
    "error_type": "calculation",
    "feedback": "계산 실수가 있습니다. 2x = 4를 풀면 x = 2입니다.",
    "concept_id": 1,
    "similar_problems": [3, 7, 12]
  }
  ```
- **실제 결과:**
- **상태:** Not Run

---

#### TC-ANALYZE-003: 이미지 업로드 분석
- **우선순위:** High
- **전제조건:**
  - 인증된 사용자
  - 손글씨 이미지 파일 (PNG, < 5MB)
- **테스트 단계:**
  1. POST `/api/v1/analyze/image` 요청
  2. Header: `Authorization: Bearer <token>`, `Content-Type: multipart/form-data`
  3. Form Data: `problem_id=1`, `image=<file>`
- **예상 결과:**
  - HTTP 200 OK
  - 응답 Body:
  ```json
  {
    "recognized_latex": "x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}",
    "is_correct": true,
    "feedback": "..."
  }
  ```
- **실제 결과:**
- **상태:** Not Run

---

#### TC-ANALYZE-004: 5MB 초과 이미지 업로드 실패
- **우선순위:** Medium
- **전제조건:**
  - 인증된 사용자
  - 6MB 이미지 파일
- **테스트 단계:**
  1. POST `/api/v1/analyze/image` 요청
  2. Form Data: `problem_id=1`, `image=<large_file>`
- **예상 결과:**
  - HTTP 413 Payload Too Large
  - 응답 Body: `{"detail": "Image file too large. Max size: 5MB"}`
- **실제 결과:**
- **상태:** Not Run

---

### 2.3 비동기 제출 (Submissions)

#### TC-SUB-001: 비동기 제출 202 응답
- **우선순위:** Critical
- **전제조건:**
  - 인증된 사용자
  - Redis/Celery 실행 중
- **테스트 단계:**
  1. POST `/api/v1/submissions` 요청
  2. Body:
  ```json
  {
    "problem_id": 1,
    "user_solution_latex": "x = 2",
    "user_solution_steps": ["풀이 과정"]
  }
  ```
- **예상 결과:**
  - HTTP 202 Accepted
  - 응답 Body:
  ```json
  {
    "submission_id": "abc123",
    "status": "pending",
    "status_url": "/api/v1/submissions/abc123/status"
  }
  ```
  - 응답 시간 < 1초
- **실제 결과:**
- **상태:** Not Run

---

#### TC-SUB-002: 제출 상태 조회 (처리 중)
- **우선순위:** Critical
- **전제조건:** TC-SUB-001 완료
- **테스트 단계:**
  1. GET `/api/v1/submissions/abc123/status` 요청
  2. Header: `Authorization: Bearer <token>`
- **예상 결과:**
  - HTTP 200 OK
  - 응답 Body:
  ```json
  {
    "submission_id": "abc123",
    "status": "processing",
    "progress": 50
  }
  ```
- **실제 결과:**
- **상태:** Not Run

---

#### TC-SUB-003: 제출 결과 조회 (완료)
- **우선순위:** Critical
- **전제조건:**
  - TC-SUB-001 완료
  - 백그라운드 작업 완료 (5초 경과)
- **테스트 단계:**
  1. GET `/api/v1/submissions/abc123/status` 요청
- **예상 결과:**
  - HTTP 200 OK
  - 응답 Body:
  ```json
  {
    "submission_id": "abc123",
    "status": "completed",
    "result_url": "/api/v1/results/xyz789"
  }
  ```
  2. GET `/api/v1/results/xyz789` 요청
  - HTTP 200 OK
  - 응답 Body: 분석 결과 (is_correct, feedback, ...)
- **실제 결과:**
- **상태:** Not Run

---

#### TC-SUB-004: WebSocket 실시간 상태 업데이트
- **우선순위:** High
- **전제조건:**
  - 인증된 사용자
  - WebSocket 지원
- **테스트 단계:**
  1. WebSocket 연결: `ws://localhost:8000/ws/v1/submissions/abc123`
  2. Header: `Authorization: Bearer <token>`
  3. 제출 생성 (TC-SUB-001)
- **예상 결과:**
  - WebSocket 연결 성공
  - 메시지 수신:
    1. `{"status": "pending"}`
    2. `{"status": "processing", "progress": 30}`
    3. `{"status": "processing", "progress": 70}`
    4. `{"status": "completed", "result_url": "..."}`
- **실제 결과:**
- **상태:** Not Run

---

### 2.4 문제 관리 (Problems)

#### TC-PROB-001: 문제 목록 조회 (페이지네이션)
- **우선순어:** High
- **전제조건:**
  - 문제 100개 존재
- **테스트 단계:**
  1. GET `/api/v1/problems?skip=0&limit=20` 요청
- **예상 결과:**
  - HTTP 200 OK
  - 응답 Body:
  ```json
  {
    "total": 100,
    "skip": 0,
    "limit": 20,
    "problems": [...]
  }
  ```
  - `problems` 배열 길이 = 20
- **실제 결과:**
- **상태:** Not Run

---

#### TC-PROB-002: 문제 추천 (개인화)
- **우선순위:** Critical
- **전제조건:**
  - 사용자 ID 1 (8학년)
  - 틀린 문제 히스토리: 개념 ID 3, 5 (방정식, 부등식)
- **테스트 단계:**
  1. GET `/api/v1/problems/recommend?user_id=1` 요청
  2. Header: `Authorization: Bearer <token>`
- **예상 결과:**
  - HTTP 200 OK
  - 응답 Body:
  ```json
  {
    "recommended_problems": [
      {"id": 12, "concept_id": 3, "difficulty": "medium"},
      {"id": 25, "concept_id": 5, "difficulty": "easy"}
    ]
  }
  ```
  - 추천 이유: 틀린 개념 위주, 난이도 조정
- **실제 결과:**
- **상태:** Not Run

---

#### TC-PROB-003: AI 유사 문제 생성
- **우선순위:** High
- **전제조건:**
  - 인증된 사용자
  - 원본 문제 ID 1 (이차방정식)
- **테스트 단계:**
  1. POST `/api/v1/problems/generate` 요청
  2. Body:
  ```json
  {
    "base_problem_id": 1,
    "count": 3
  }
  ```
- **예상 결과:**
  - HTTP 200 OK
  - 응답 Body:
  ```json
  {
    "generated_problems": [
      {"id": 101, "text": "x^2 - 5x + 6 = 0을 풀어라.", "answer": "x=2 또는 x=3"},
      {"id": 102, "text": "x^2 + 3x - 10 = 0을 풀어라.", "answer": "x=2 또는 x=-5"},
      {"id": 103, "text": "2x^2 - 8x + 6 = 0을 풀어라.", "answer": "x=1 또는 x=3"}
    ]
  }
  ```
  - 생성 시간 < 10초
- **실제 결과:**
- **상태:** Not Run

---

### 2.5 사용자 리포트 (Users)

#### TC-USER-001: 학습 리포트 조회
- **우선순위:** High
- **전제조건:**
  - 사용자 ID 1
  - 제출 히스토리 30개 (정답 20, 오답 10)
- **테스트 단계:**
  1. GET `/api/v1/users/1/report` 요청
  2. Header: `Authorization: Bearer <token>`
- **예상 결과:**
  - HTTP 200 OK
  - 응답 Body:
  ```json
  {
    "user_id": 1,
    "total_submissions": 30,
    "correct_count": 20,
    "accuracy": 66.7,
    "error_type_distribution": {
      "calculation": 5,
      "concept": 3,
      "procedure": 2
    },
    "weak_concepts": [3, 5],
    "streak_days": 7
  }
  ```
- **실제 결과:**
- **상태:** Not Run

---

#### TC-USER-002: 개념 습득 현황 조회
- **우선순위:** High
- **전제조건:**
  - 사용자 ID 1
  - 개념 3 (방정식): 7일 전 1회, 3일 전 1회, 오늘 1회 정답
- **테스트 단계:**
  1. GET `/api/v1/users/1/mastery` 요청
- **예상 결과:**
  - HTTP 200 OK
  - 응답 Body:
  ```json
  {
    "user_id": 1,
    "concept_mastery": [
      {
        "concept_id": 3,
        "concept_name": "일차방정식",
        "mastery_level": 0.8,
        "review_count": 3,
        "next_review_date": "2026-05-30"
      }
    ]
  }
  ```
- **실제 결과:**
- **상태:** Not Run

---

#### TC-USER-003: 오답 노트 조회
- **우선순위:** Medium
- **전제조건:**
  - 사용자 ID 1
  - 오답 10개
- **테스트 단계:**
  1. GET `/api/v1/users/1/wrong-notes?skip=0&limit=5` 요청
- **예상 결과:**
  - HTTP 200 OK
  - 응답 Body:
  ```json
  {
    "total": 10,
    "wrong_submissions": [
      {
        "submission_id": "abc123",
        "problem_id": 5,
        "error_type": "calculation",
        "submitted_at": "2026-05-21T10:30:00Z"
      }
    ]
  }
  ```
  - 배열 길이 = 5
- **실제 결과:**
- **상태:** Not Run

---

### 2.6 개념 관리 (Concepts)

#### TC-CONCEPT-001: 개념 목록 조회
- **우선순위:** Medium
- **전제조건:**
  - 개념 20개 등록 (8학년 수학 교육과정)
- **테스트 단계:**
  1. GET `/api/v1/concepts?grade_level=8` 요청
- **예상 결과:**
  - HTTP 200 OK
  - 응답 Body:
  ```json
  {
    "concepts": [
      {"id": 1, "name": "일차방정식", "grade_level": 8},
      {"id": 2, "name": "연립방정식", "grade_level": 8}
    ]
  }
  ```
- **실제 결과:**
- **상태:** Not Run

---

#### TC-CONCEPT-002: AI 개념 설명 생성
- **우선순위:** High
- **전제조건:**
  - 개념 ID 3 (일차방정식)
  - 사용자 학년 8학년
- **테스트 단계:**
  1. GET `/api/v1/concepts/3/explanation?grade_level=8` 요청
- **예상 결과:**
  - HTTP 200 OK
  - 응답 Body:
  ```json
  {
    "concept_id": 3,
    "explanation": "일차방정식은 미지수가 1개이고 차수가 1인 방정식입니다. ax + b = 0 형태로 나타낼 수 있습니다.",
    "examples": ["2x + 3 = 7", "5x - 10 = 0"]
  }
  ```
  - 설명 언어: 8학년 수준
- **실제 결과:**
- **상태:** Not Run

---

## 3. Mobile Application 테스트 케이스

### 3.1 로그인 및 회원가입

#### TC-MOBILE-AUTH-001: Kakao 소셜 로그인 성공
- **우선순위:** Critical
- **전제조건:**
  - Android 디바이스 (API 24+)
  - Kakao 앱 설치 (또는 웹뷰)
- **테스트 단계:**
  1. 앱 실행 → 로그인 화면
  2. "Kakao로 계속하기" 버튼 탭
  3. Kakao 계정 로그인 (또는 자동 로그인)
  4. 권한 동의
- **예상 결과:**
  - Kakao 로그인 성공
  - MathLens 백엔드 JWT 토큰 발급
  - 홈 화면으로 이동
  - AsyncStorage에 토큰 저장
- **실제 결과:**
- **상태:** Not Run

---

#### TC-MOBILE-AUTH-002: Google 소셜 로그인 성공
- **우선순위:** Critical
- **전제조건:**
  - Android 디바이스
  - Google 계정 존재
- **테스트 단계:**
  1. 앱 실행 → 로그인 화면
  2. "Google로 계속하기" 버튼 탭
  3. Google 계정 선택
- **예상 결과:**
  - Google 로그인 성공
  - 홈 화면 이동
  - JWT 토큰 저장
- **실제 결과:**
- **상태:** Not Run

---

#### TC-MOBILE-AUTH-003: 로그아웃
- **우선순위:** High
- **전제조건:**
  - 로그인 상태
- **테스트 단계:**
  1. 메뉴 → "로그아웃" 버튼 탭
  2. 확인 다이얼로그 → "확인" 탭
- **예상 결과:**
  - AsyncStorage에서 토큰 삭제
  - Redux store 초기화
  - 로그인 화면으로 이동
- **실제 결과:**
- **상태:** Not Run

---

### 3.2 펜 입력 캔버스

#### TC-MOBILE-CANVAS-001: 스타일러스 펜 입력
- **우선순위:** Critical
- **전제조건:**
  - 스타일러스 펜 지원 디바이스 (S Pen, Apple Pencil)
- **테스트 단계:**
  1. 홈 → "새 문제 풀기" → 캔버스 화면
  2. 스타일러스 펜으로 "x=2" 작성
- **예상 결과:**
  - 스트로크 실시간 렌더링
  - 필압 감지 (두께 변화)
  - 지연 시간 < 50ms
- **실제 결과:**
- **상태:** Not Run

---

#### TC-MOBILE-CANVAS-002: 손가락 터치 입력
- **우선순위:** High
- **전제조건:**
  - 터치스크린 디바이스
- **테스트 단계:**
  1. 캔버스 화면
  2. 손가락으로 "y=3x+5" 작성
- **예상 결과:**
  - 스트로크 렌더링
  - 스타일러스와 동일한 입력 정확도
- **실제 결과:**
- **상태:** Not Run

---

#### TC-MOBILE-CANVAS-003: 지우개 도구
- **우선순위:** High
- **전제조건:**
  - 캔버스에 스트로크 존재
- **테스트 단계:**
  1. 도구 선택 → "지우개" 탭
  2. 스트로크 위를 드래그
- **예상 결과:**
  - 겹치는 스트로크 삭제
  - 부분 지우기 지원
- **실제 결과:**
- **상태:** Not Run

---

#### TC-MOBILE-CANVAS-004: Undo/Redo
- **우선순위:** Medium
- **전제조건:**
  - 캔버스에 스트로크 3개 작성
- **테스트 단계:**
  1. "Undo" 버튼 탭 (2회)
  2. "Redo" 버튼 탭 (1회)
- **예상 결과:**
  - Undo: 마지막 스트로크 2개 제거
  - Redo: 최근 제거된 스트로크 1개 복원
  - 스트로크 히스토리 스택 관리
- **실제 결과:**
- **상태:** Not Run

---

#### TC-MOBILE-CANVAS-005: Zoom & Pan
- **우선순위:** Medium
- **전제조건:**
  - 캔버스 화면
- **테스트 단계:**
  1. Pinch 제스처 (확대)
  2. 두 손가락 드래그 (이동)
- **예상 결과:**
  - 캔버스 확대/축소 (최소 50%, 최대 200%)
  - 캔버스 이동 (스크롤)
  - 입력 모드와 충돌 없음
- **실제 결과:**
- **상태:** Not Run

---

### 3.3 손글씨 인식

#### TC-MOBILE-HTR-001: 실시간 수식 인식 (iink SDK)
- **우선순위:** Critical
- **전제조건:**
  - iink SDK 초기화
  - 인터넷 연결
- **테스트 단계:**
  1. 캔버스에 "x^2 + 3x - 10 = 0" 작성
  2. 1초 대기 (디바운스)
- **예상 결과:**
  - LaTeX 인식: `x^2 + 3x - 10 = 0`
  - 인식 시간 < 2초
  - 화면에 LaTeX 미리보기 표시
- **실제 결과:**
- **상태:** Not Run

---

#### TC-MOBILE-HTR-002: MathPix 폴백 인식
- **우선순위:** High
- **전제조건:**
  - iink SDK 인식 실패 (confidence < 0.7)
- **테스트 단계:**
  1. 캔버스에 복잡한 수식 작성
  2. iink 인식 → 신뢰도 낮음
  3. 자동으로 MathPix API 호출
- **예상 결과:**
  - MathPix 인식 결과 반환
  - 사용자에게 두 결과 비교 UI 표시
  - 사용자가 선택 가능
- **실제 결과:**
- **상태:** Not Run

---

#### TC-MOBILE-HTR-003: 수동 LaTeX 수정
- **우선순위:** High
- **전제조건:**
  - 인식 완료 상태
  - LaTeX: `x^2 + 3x - 10 = 0`
- **테스트 단계:**
  1. LaTeX 미리보기 탭
  2. 텍스트 입력 모드로 전환
  3. 수정: `x^2 + 5x - 10 = 0`
- **예상 결과:**
  - 텍스트 입력 필드 활성화
  - 수정 내용 실시간 반영
  - "확인" 버튼 → 수정 완료
- **실제 결과:**
- **상태:** Not Run

---

### 3.4 풀이 제출 및 결과

#### TC-MOBILE-SUB-001: 비동기 제출 및 로딩 인디케이터
- **우선순위:** Critical
- **전제조건:**
  - 로그인 상태
  - 문제 선택
  - 캔버스에 풀이 작성 완료
- **테스트 단계:**
  1. "제출" 버튼 탭
  2. 백엔드 POST `/api/v1/submissions` 호출
- **예상 결과:**
  - 로딩 인디케이터 표시
  - 1초 이내 HTTP 202 응답
  - "제출이 완료되었습니다. 분석 중..." 메시지
  - 상태 폴링 시작 (2초 간격)
- **실제 결과:**
- **상태:** Not Run

---

#### TC-MOBILE-SUB-002: WebSocket 실시간 상태 업데이트
- **우선순위:** High
- **전제조건:**
  - TC-MOBILE-SUB-001 완료
  - WebSocket 연결 성공
- **테스트 단계:**
  1. 백엔드 처리 진행 중
  2. WebSocket 메시지 수신
- **예상 결과:**
  - 진행률 바 업데이트 (0% → 30% → 70% → 100%)
  - 상태 메시지: "인식 중..." → "분석 중..." → "완료!"
- **실제 결과:**
- **상태:** Not Run

---

#### TC-MOBILE-SUB-003: 분석 결과 화면 (정답)
- **우선순위:** Critical
- **전제조건:**
  - 백엔드 분석 완료 (정답)
- **테스트 단계:**
  1. WebSocket 또는 폴링 → 완료 상태 수신
  2. 결과 화면으로 자동 이동
- **예상 결과:**
  - 화면 표시:
    - ✅ "정답입니다!"
    - 피드백: "근의 공식을 올바르게 적용했습니다."
    - "다음 문제" 버튼
- **실제 결과:**
- **상태:** Not Run

---

#### TC-MOBILE-SUB-004: 분석 결과 화면 (오답)
- **우선순위:** Critical
- **전제조건:**
  - 백엔드 분석 완료 (오답)
- **테스트 단계:**
  1. 결과 화면으로 이동
- **예상 결과:**
  - 화면 표시:
    - ❌ "오답입니다."
    - 오류 유형: "계산 실수"
    - 피드백: "2x = 4를 풀면 x = 2입니다."
    - 개념 설명 버튼
    - 유사 문제 추천 (3개)
    - "다시 풀어보기" 버튼
- **실제 결과:**
- **상태:** Not Run

---

### 3.5 학습 대시보드

#### TC-MOBILE-DASH-001: 학습 리포트 조회
- **우선순위:** High
- **전제조건:**
  - 로그인 상태
  - 제출 히스토리 20개
- **테스트 단계:**
  1. 하단 네비게이션 → "대시보드" 탭
- **예상 결과:**
  - 화면 표시:
    - 총 제출 수: 20
    - 정답률: 70%
    - 오류 유형 분포 (파이 차트)
    - 취약 개념 (Top 3)
    - 연속 학습일: 7일
- **실제 결과:**
- **상태:** Not Run

---

#### TC-MOBILE-DASH-002: 오답 노트 조회
- **우선순위:** Medium
- **전제조건:**
  - 오답 10개 존재
- **테스트 단계:**
  1. 대시보드 → "오답 노트" 버튼 탭
- **예상 결과:**
  - 오답 목록 화면
  - 각 항목: 문제 요약, 오류 유형, 제출 날짜
  - 탭 → 상세 화면 (문제, 내 풀이, 피드백)
- **실제 결과:**
- **상태:** Not Run

---

### 3.6 오프라인 모드

#### TC-MOBILE-OFFLINE-001: 오프라인 캔버스 입력
- **우선순위:** Medium
- **전제조건:**
  - 인터넷 연결 끊김
- **테스트 단계:**
  1. 캔버스 화면에서 풀이 작성
- **예상 결과:**
  - 스트로크 입력 정상 동작
  - 손글씨 인식 실패 (iink SDK 오프라인 미지원)
  - "오프라인 상태입니다. 제출은 온라인 시 가능합니다." 메시지
- **실제 결과:**
- **상태:** Not Run

---

#### TC-MOBILE-OFFLINE-002: 로컬 캐싱 및 동기화
- **우선순위:** Medium
- **전제조건:**
  - 오프라인 상태에서 풀이 3개 작성
- **테스트 단계:**
  1. 인터넷 연결 복구
  2. 앱이 온라인 상태 감지
- **예상 결과:**
  - 자동으로 로컬 데이터 백엔드 동기화
  - "3개의 제출이 동기화되었습니다." 알림
  - 제출 히스토리 업데이트
- **실제 결과:**
- **상태:** Not Run

---

## 4. Integration 테스트 케이스

### 4.1 End-to-End 플로우

#### TC-E2E-001: 신규 사용자 온보딩 플로우
- **우선순위:** Critical
- **전제조건:**
  - 앱 최초 실행
- **테스트 단계:**
  1. 앱 실행 → 온보딩 화면 (튜토리얼)
  2. "Kakao로 계속하기" → 회원가입
  3. 프로필 설정 (학년, 닉네임)
  4. 홈 화면 → "첫 문제 풀어보기" 탭
  5. 문제 선택 → 캔버스에 풀이 작성 → 제출
  6. 결과 확인 → "다음 문제" 탭
- **예상 결과:**
  - 전체 플로우 완료 시간 < 5분
  - 모든 화면 정상 이동
  - 백엔드 데이터 저장 확인
- **실제 결과:**
- **상태:** Not Run

---

#### TC-E2E-002: 틀린 문제 → 개념 복습 → 유사 문제 재도전
- **우선순위:** Critical
- **전제조건:**
  - 로그인 상태
- **테스트 단계:**
  1. 문제 ID 5 (일차방정식) 풀이 → 오답 제출
  2. 결과 화면 → "개념 설명 보기" 버튼 탭
  3. 개념 설명 화면 → "유사 문제 풀어보기" 탭
  4. AI 생성 유사 문제 3개 표시 → 첫 번째 문제 선택
  5. 캔버스에 풀이 → 제출 → 정답
- **예상 결과:**
  - 개념 습득 점수 증가
  - 다음 복습 날짜 스케줄링 (에빙하우스 곡선)
  - 대시보드에 반영
- **실제 결과:**
- **상태:** Not Run

---

#### TC-E2E-003: 주간 학습 리포트 조회
- **우선순위:** High
- **전제조건:**
  - 7일 연속 사용
  - 제출 30개
- **테스트 단계:**
  1. 대시보드 → "주간 리포트" 탭
- **예상 결과:**
  - 화면 표시:
    - 이번 주 제출 수: 30
    - 정답률: 75%
    - 가장 많이 틀린 개념: 이차방정식
    - 개선 제안: "방정식 풀이를 더 연습해보세요."
- **실제 결과:**
- **상태:** Not Run

---

## 5. Performance 테스트 케이스

### 5.1 부하 테스트 (Load Testing)

#### TC-PERF-001: 동기 분석 응답 시간
- **우선순위:** High
- **전제조건:**
  - Backend API 실행 중
  - GPT-4o API 정상
- **테스트 단계:**
  1. Locust로 동시 사용자 100명 시뮬레이션
  2. POST `/api/v1/analyze` 요청 (동기)
  3. 10분간 실행
- **예상 결과:**
  - 평균 응답 시간 ≤ 5초
  - P95 응답 시간 ≤ 8초
  - 에러율 ≤ 1%
- **실제 결과:**
- **상태:** Not Run

---

#### TC-PERF-002: 비동기 제출 처리량
- **우선순위:** High
- **전제조건:**
  - Celery worker 4개 실행
  - Redis 정상
- **테스트 단계:**
  1. Locust로 동시 사용자 500명
  2. POST `/api/v1/submissions` 요청 (비동기)
  3. 202 응답 후 상태 폴링
- **예상 결과:**
  - 202 응답 시간 ≤ 1초
  - 전체 처리 시간 (제출 → 완료) ≤ 10초
  - 처리량 ≥ 100 req/sec
- **실제 결과:**
- **상태:** Not Run

---

#### TC-PERF-003: WebSocket 동시 연결
- **우선순위:** Medium
- **전제조건:**
  - Backend WebSocket 서버 실행
- **테스트 단계:**
  1. k6로 WebSocket 연결 1,000개 동시 생성
  2. 각 연결당 메시지 10개 송수신
- **예상 결과:**
  - 연결 성공률 ≥ 99%
  - 메시지 지연 시간 ≤ 100ms
  - 서버 CPU ≤ 80%, Memory ≤ 2GB
- **실제 결과:**
- **상태:** Not Run

---

### 5.2 스트레스 테스트 (Stress Testing)

#### TC-PERF-004: 최대 부하 테스트
- **우선순위:** Medium
- **전제조건:**
  - Staging 환경
- **테스트 단계:**
  1. Locust로 사용자 수 점진적 증가 (0 → 1,000명)
  2. 에러율 5% 도달 시점 확인
- **예상 결과:**
  - 에러율 5% 도달 시점: 동시 사용자 ≥ 800명
  - 시스템 크래시 없음
  - 복구 시간 < 1분
- **실제 결과:**
- **상태:** Not Run

---

## 6. Security 테스트 케이스

### 6.1 인증 및 권한

#### TC-SEC-001: JWT 토큰 위조 방지
- **우선순위:** Critical
- **전제조건:**
  - 유효한 JWT 토큰 보유
- **테스트 단계:**
  1. JWT 토큰의 payload 수정 (user_id 변경)
  2. 서명은 유지
  3. GET `/api/v1/auth/me` 요청
- **예상 결과:**
  - HTTP 401 Unauthorized
  - 응답: `{"detail": "Invalid token signature"}`
- **실제 결과:**
- **상태:** Not Run

---

#### TC-SEC-002: 타인 리소스 접근 차단
- **우선순위:** Critical
- **전제조건:**
  - 사용자 A (ID 1) 로그인
  - 사용자 B (ID 2) 존재
- **테스트 단계:**
  1. 사용자 A의 토큰으로 요청
  2. GET `/api/v1/users/2/report` (사용자 B의 리포트)
- **예상 결과:**
  - HTTP 403 Forbidden
  - 응답: `{"detail": "Not authorized to access this resource"}`
- **실제 결과:**
- **상태:** Not Run

---

### 6.2 입력 검증

#### TC-SEC-003: SQL Injection 방어
- **우선순위:** Critical
- **전제조건:**
  - Backend API 실행
- **테스트 단계:**
  1. POST `/api/v1/auth/register` 요청
  2. Body: `{"username": "admin' OR '1'='1", "email": "test@example.com", "password": "Pass123!"}`
- **예상 결과:**
  - SQL Injection 시도 차단
  - 사용자 생성 실패 (입력 검증 오류)
  - 데이터베이스 영향 없음
- **실제 결과:**
- **상태:** Not Run

---

#### TC-SEC-004: XSS 방어
- **우선순위:** High
- **전제조건:**
  - Mobile 앱
- **테스트 단계:**
  1. 피드백 텍스트에 `<script>alert('XSS')</script>` 포함
  2. 결과 화면에 피드백 표시
- **예상 결과:**
  - 스크립트 실행 안 됨
  - 텍스트가 이스케이프되어 표시: `&lt;script&gt;...`
- **실제 결과:**
- **상태:** Not Run

---

### 6.3 민감 정보 보호

#### TC-SEC-005: 비밀번호 암호화 저장
- **우선순위:** Critical
- **전제조건:**
  - 사용자 등록 완료
- **테스트 단계:**
  1. 데이터베이스 직접 조회
  2. SELECT password_hash FROM users WHERE id=1
- **예상 결과:**
  - 비밀번호 평문 저장 안 됨
  - bcrypt 해시 형식: `$2b$12$...`
- **실제 결과:**
- **상태:** Not Run

---

#### TC-SEC-006: API 키 노출 방지
- **우선순위:** Critical
- **전제조건:**
  - Backend 소스 코드
- **테스트 단계:**
  1. 소스 코드 검색: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`
  2. 환경 변수로만 로드 확인
- **예상 결과:**
  - 소스 코드에 평문 API 키 없음
  - `.env` 파일은 `.gitignore`에 포함
  - Git 히스토리에도 API 키 없음
- **실제 결과:**
- **상태:** Not Run

---

## 7. 부록

### 7.1 테스트 실행 가이드

**Backend Unit Tests:**
```bash
cd backend
pytest --tb=short -q
```

**Backend Coverage Report:**
```bash
pytest --cov=app --cov-report=html
open htmlcov/index.html
```

**Mobile Unit Tests:**
```bash
cd mobile
npm test
```

**E2E Tests (Detox):**
```bash
cd mobile
npm run detox:build
npm run detox:test
```

**Performance Tests (Locust):**
```bash
cd backend/tests/performance
locust -f load_test.py --host=http://localhost:8000
```

---

### 7.2 테스트 데이터 준비

**Seed Data:**
```bash
cd backend
python -m app.scripts.seed_data
```

**Mock GPT-4o Responses:**
```python
# tests/conftest.py
@pytest.fixture
def mock_openai(mocker):
    mocker.patch('app.services.analysis.openai_client.chat.completions.create',
                 return_value={'is_correct': True, 'feedback': '정답입니다!'})
```

---

### 7.3 버그 리포트 템플릿

**GitHub Issue Template:**
```markdown
## 버그 설명
간단한 버그 설명

## 재현 단계
1. ...
2. ...
3. ...

## 예상 동작
무엇이 일어나야 하는지

## 실제 동작
실제로 무엇이 일어났는지

## 환경
- OS: [Android 12, iOS 15]
- 앱 버전: [v1.0.0]
- 디바이스: [Pixel 6, iPhone 13]

## 스크린샷
(선택사항)

## 우선순위
- [ ] Critical
- [ ] High
- [ ] Medium
- [ ] Low
```

---

**문서 이력:**

| 버전 | 날짜 | 작성자 | 변경 내용 |
|------|------|--------|----------|
| v1.0 | 2026-05-22 | QA팀 | 초안 작성 |
