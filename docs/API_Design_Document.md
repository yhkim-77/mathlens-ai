# MathLens AI — API 설계 문서 (API Design Document)

**문서 버전:** v1.0
**작성일:** 2026-05-22
**문서 유형:** API Design Document
**작성자:** MathLens AI 개발팀
**상태:** 초안 (Draft)

---

## 목차

1. [개요](#1-개요)
2. [API 아키텍처](#2-api-아키텍처)
3. [인증 및 권한](#3-인증-및-권한)
4. [공통 사항](#4-공통-사항)
5. [API 엔드포인트 명세](#5-api-엔드포인트-명세)
   - [5.1 인증 API](#51-인증-api)
   - [5.2 풀이 제출 및 분석 API](#52-풀이-제출-및-분석-api)
   - [5.3 문제은행 API](#53-문제은행-api)
   - [5.4 사용자 관리 API](#54-사용자-관리-api)
   - [5.5 개념 관리 API](#55-개념-관리-api)
6. [WebSocket 프로토콜](#6-websocket-프로토콜)
7. [에러 코드 정의](#7-에러-코드-정의)
8. [Rate Limiting](#8-rate-limiting)
9. [보안 고려사항](#9-보안-고려사항)
10. [API 버전 관리](#10-api-버전-관리)

---

## 1. 개요

### 1.1 문서 목적

본 문서는 MathLens AI 백엔드 서비스의 REST API 및 WebSocket 프로토콜 명세를 정의합니다. 모바일 클라이언트 개발자와 백엔드 개발자 간의 인터페이스 계약을 명확히 하고, API 통합 및 테스트를 위한 기준을 제공합니다.

### 1.2 API 개요

- **Base URL**: `https://api.mathlens.ai/api/v1`
- **프로토콜**: HTTPS (TLS 1.3)
- **데이터 포맷**: JSON
- **문자 인코딩**: UTF-8
- **인증 방식**: JWT Bearer Token
- **API 버전**: v1

### 1.3 대상 독자

- 모바일 앱 개발자 (iOS/Android)
- 백엔드 API 개발자
- QA 엔지니어
- DevOps 엔지니어

---

## 2. API 아키텍처

### 2.1 계층 구조

```
┌───────────────────────────────────────────────────────┐
│                  Client Layer                         │
│              (React Native App)                       │
└────────────────────┬──────────────────────────────────┘
                     │ HTTPS / WSS
                     │
┌────────────────────▼──────────────────────────────────┐
│               API Gateway Layer                       │
│                  (FastAPI)                            │
│  - JWT Authentication Middleware                      │
│  - Rate Limiting Middleware                           │
│  - CORS Middleware                                    │
│  - Request Validation                                 │
└────────────────────┬──────────────────────────────────┘
                     │
┌────────────────────▼──────────────────────────────────┐
│              Application Layer                        │
│              (API Routers + Services)                 │
│  - /api/v1/auth          (인증)                       │
│  - /api/v1/submissions   (풀이 제출)                  │
│  - /api/v1/analyze       (동기 분석)                  │
│  - /api/v1/problems      (문제은행)                   │
│  - /api/v1/users         (사용자 관리)                │
│  - /api/v1/concepts      (개념 관리)                  │
└────────────────────┬──────────────────────────────────┘
                     │
┌────────────────────▼──────────────────────────────────┐
│              Integration Layer                        │
│  - OpenAI GPT-4o API                                  │
│  - Anthropic Claude API (Fallback)                    │
│  - PostgreSQL Database                                │
│  - AWS S3 Storage                                     │
└───────────────────────────────────────────────────────┘
```

### 2.2 통신 방식

#### 2.2.1 REST API
- **동기 방식**: 요청 즉시 응답 반환
- **비동기 방식**: 202 Accepted 반환 후 별도 조회

#### 2.2.2 WebSocket
- **실시간 상태 업데이트**: 풀이 분석 진행 상황 전달
- **연결 유지**: Keep-alive ping/pong

---

## 3. 인증 및 권한

### 3.1 JWT 토큰 기반 인증

#### 3.1.1 토큰 구조

**Access Token**
- **유효기간**: 1시간
- **Payload**:
  ```json
  {
    "sub": "user_id (UUID)",
    "type": "access",
    "exp": 1716389400,
    "iat": 1716385800
  }
  ```
- **서명 알고리즘**: HS256

**Refresh Token**
- **유효기간**: 30일
- **Payload**:
  ```json
  {
    "sub": "user_id (UUID)",
    "type": "refresh",
    "exp": 1718981400,
    "iat": 1716385800
  }
  ```

#### 3.1.2 인증 헤더

모든 인증이 필요한 엔드포인트는 다음 헤더를 포함해야 합니다:

```http
Authorization: Bearer {access_token}
```

#### 3.1.3 토큰 갱신 플로우

```
[Client]
    │
    │ 1. API 호출 (Access Token)
    │
    ▼
[Server]
    │
    │ 2. 401 Unauthorized (Token Expired)
    │
    ▼
[Client]
    │
    │ 3. POST /api/v1/auth/refresh
    │    Body: { "refresh_token": "..." }
    │
    ▼
[Server]
    │
    │ 4. 새로운 Access Token 발급
    │
    ▼
[Client]
    │
    │ 5. 원래 API 재요청
```

---

## 4. 공통 사항

### 4.1 HTTP 상태 코드

| 상태 코드 | 의미 | 사용 예시 |
|----------|------|----------|
| 200 OK | 요청 성공 | GET, PUT, DELETE 성공 |
| 201 Created | 리소스 생성 성공 | POST 생성 성공 |
| 202 Accepted | 비동기 요청 수락 | 풀이 제출 수락 |
| 400 Bad Request | 잘못된 요청 | 유효성 검증 실패 |
| 401 Unauthorized | 인증 실패 | 토큰 없음/만료/잘못됨 |
| 403 Forbidden | 권한 없음 | 접근 권한 부족 |
| 404 Not Found | 리소스 없음 | 존재하지 않는 ID |
| 409 Conflict | 리소스 충돌 | 이메일 중복 |
| 413 Payload Too Large | 페이로드 크기 초과 | 이미지 크기 초과 |
| 429 Too Many Requests | 요청 횟수 초과 | Rate limit 도달 |
| 500 Internal Server Error | 서버 오류 | 예상치 못한 서버 에러 |
| 503 Service Unavailable | 서비스 일시 중단 | 외부 API 장애 |

### 4.2 공통 에러 응답 포맷

```json
{
  "error": "ERROR_CODE",
  "message": "사용자에게 표시할 한국어 메시지",
  "detail": "개발자용 상세 정보 (선택적)",
  "timestamp": "2026-05-22T10:30:00Z",
  "request_id": "uuid"
}
```

### 4.3 페이지네이션

페이지네이션이 적용되는 엔드포인트는 다음 쿼리 파라미터를 사용합니다:

```
?limit=20&offset=0
```

**응답 포맷**:
```json
{
  "items": [...],
  "total": 100,
  "limit": 20,
  "offset": 0,
  "has_more": true
}
```

### 4.4 타임스탬프 포맷

모든 날짜/시간은 ISO 8601 형식을 사용합니다:
```
2026-05-22T10:30:00Z
```

### 4.5 요청 크기 제한

| 항목 | 최대 크기 |
|------|----------|
| JSON 페이로드 | 5 MB |
| Base64 이미지 | 2 MB (인코딩 후) |
| 파일 업로드 | 10 MB |

---

## 5. API 엔드포인트 명세

### 5.1 인증 API

#### 5.1.1 회원가입

**Endpoint**: `POST /api/v1/auth/register`

**설명**: 이메일과 비밀번호로 신규 회원가입

**인증**: 불필요

**요청 바디**:
```json
{
  "email": "student@example.com",
  "password": "SecurePassword123!",
  "display_name": "홍길동",
  "grade": "middle_2"
}
```

**필드 설명**:
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| email | string | O | 이메일 주소 (고유) |
| password | string | O | 비밀번호 (최소 8자, 영문+숫자+특수문자) |
| display_name | string | X | 표시 이름 |
| grade | string | X | 학년 (middle_1 ~ high_3, reexaminee) |

**성공 응답** (201 Created):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**에러 응답**:
- `400 Bad Request`: 유효성 검증 실패
  ```json
  {
    "error": "VALIDATION_ERROR",
    "message": "비밀번호는 최소 8자 이상이어야 합니다.",
    "detail": {"field": "password", "constraint": "min_length"}
  }
  ```
- `409 Conflict`: 이메일 중복
  ```json
  {
    "error": "EMAIL_ALREADY_EXISTS",
    "message": "이미 가입된 이메일입니다."
  }
  ```

---

#### 5.1.2 로그인

**Endpoint**: `POST /api/v1/auth/token`

**설명**: 이메일과 비밀번호로 로그인하여 JWT 토큰 발급

**인증**: 불필요

**요청 형식**: `application/x-www-form-urlencoded` (OAuth2 표준)

**요청 바디**:
```
username=student@example.com&password=SecurePassword123!
```

**필드 설명**:
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| username | string | O | 이메일 주소 (OAuth2 표준 필드명) |
| password | string | O | 비밀번호 |

**성공 응답** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**에러 응답**:
- `401 Unauthorized`: 인증 실패
  ```json
  {
    "error": "INVALID_CREDENTIALS",
    "message": "이메일 또는 비밀번호가 올바르지 않습니다."
  }
  ```

---

#### 5.1.3 토큰 갱신

**Endpoint**: `POST /api/v1/auth/refresh`

**설명**: Refresh Token으로 새로운 Access Token 발급

**인증**: 불필요 (Refresh Token 필요)

**요청 바디**:
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**성공 응답** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**에러 응답**:
- `401 Unauthorized`: Refresh Token 유효하지 않음
  ```json
  {
    "error": "INVALID_REFRESH_TOKEN",
    "message": "유효하지 않은 갱신 토큰입니다."
  }
  ```

---

#### 5.1.4 내 정보 조회

**Endpoint**: `GET /api/v1/auth/me`

**설명**: 현재 로그인한 사용자의 정보 조회

**인증**: 필수 (JWT)

**성공 응답** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "student@example.com",
  "display_name": "홍길동",
  "grade": "middle_2"
}
```

**에러 응답**:
- `401 Unauthorized`: 토큰 없음/만료
  ```json
  {
    "error": "UNAUTHORIZED",
    "message": "인증이 필요합니다."
  }
  ```

---

### 5.2 풀이 제출 및 분석 API

#### 5.2.1 비동기 풀이 제출 (권장)

**Endpoint**: `POST /api/v1/submissions`

**설명**: 손글씨 풀이 이미지를 제출하여 AI 분석 요청 (비동기 처리)

**인증**: 필수 (JWT)

**요청 바디**:
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "problem_id": "660e8400-e29b-41d4-a716-446655440001",
  "session_id": "770e8400-e29b-41d4-a716-446655440002",
  "image_base64": "iVBORw0KGgoAAAANSUhEUgAA...",
  "image_mime_type": "image/png",
  "recognized_latex": "2x + 3 = 7 \\\\ 2x = 4 \\\\ x = 2",
  "stroke_metadata": {
    "stroke_count": 42,
    "total_duration_ms": 35000,
    "canvas_size": {"width": 1080, "height": 1440}
  },
  "client_timestamp": "2026-05-22T10:30:00Z",
  "device_info": {
    "platform": "ios",
    "os_version": "17.4",
    "device_model": "iPad Pro 12.9"
  }
}
```

**필드 설명**:
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| user_id | string (UUID) | O | 사용자 ID |
| problem_id | string (UUID) | X | 문제 ID (문제은행 문제일 경우) |
| session_id | string (UUID) | X | 학습 세션 ID |
| image_base64 | string | O | Base64 인코딩된 캔버스 이미지 (< 2MB) |
| image_mime_type | string | O | 이미지 MIME 타입 (image/png 또는 image/jpeg) |
| recognized_latex | string | X | 클라이언트에서 사전 인식한 LaTeX (iink SDK) |
| stroke_metadata | object | X | 스트로크 메타데이터 |
| client_timestamp | string | X | 클라이언트 제출 시각 (ISO 8601) |
| device_info | object | X | 디바이스 정보 |

**성공 응답** (202 Accepted):
```json
{
  "submission_id": "880e8400-e29b-41d4-a716-446655440003",
  "status": "received",
  "websocket_url": "/ws/v1/submissions/880e8400-e29b-41d4-a716-446655440003",
  "estimated_processing_time_ms": 5000
}
```

**에러 응답**:
- `400 Bad Request`: 유효성 검증 실패
  ```json
  {
    "error": "SUBMISSION_IMAGE_TOO_LARGE",
    "message": "이미지 크기는 2MB 이하여야 합니다."
  }
  ```
- `400 Bad Request`: 빈 캔버스
  ```json
  {
    "error": "SUBMISSION_EMPTY_CANVAS",
    "message": "캔버스가 비어있습니다."
  }
  ```
- `404 Not Found`: 문제 없음
  ```json
  {
    "error": "PROBLEM_NOT_FOUND",
    "message": "문제를 찾을 수 없습니다."
  }
  ```
- `413 Payload Too Large`: 이미지 크기 초과
- `429 Too Many Requests`: Rate limit 초과

---

#### 5.2.2 제출 상태 조회 (폴링)

**Endpoint**: `GET /api/v1/submissions/{submission_id}/status`

**설명**: 제출된 풀이의 처리 상태 조회 (WebSocket 대안)

**인증**: 필수 (JWT)

**경로 파라미터**:
| 파라미터 | 타입 | 설명 |
|----------|------|------|
| submission_id | string (UUID) | 제출 ID |

**성공 응답** (200 OK):

**처리 중**:
```json
{
  "submission_id": "880e8400-e29b-41d4-a716-446655440003",
  "status": "processing",
  "result": null
}
```

**처리 완료**:
```json
{
  "submission_id": "880e8400-e29b-41d4-a716-446655440003",
  "status": "completed",
  "result": {
    "is_correct": false,
    "recognized_latex": "2x + 3 = 7 \\\\ 2x = 7 - 3 \\\\ x = 2",
    "steps": [
      "2x + 3 = 7",
      "2x = 7 - 3",
      "x = 2"
    ],
    "errors": [
      {
        "step_order": 2,
        "error_type": "procedural",
        "error_subtype": "sign_error",
        "description": "이항할 때 부호를 바꾸지 않았습니다.",
        "correct_expression": "2x = 7 - 3 = 4"
      }
    ],
    "feedback": "등식의 성질에서 이항할 때는 부호를 반대로 바꿔야 해요. 3을 오른쪽으로 이항하면 -3이 됩니다. 따라서 2x = 7 - 3 = 4가 되어야 합니다.",
    "concept_explanation": "등식의 이항 규칙: 등식의 한 항을 다른 쪽으로 이동할 때 부호를 바꿉니다...",
    "confidence": 0.92
  }
}
```

**상태 값**:
| 상태 | 설명 |
|------|------|
| received | 제출 접수됨 |
| processing | AI 분석 진행 중 |
| completed | 분석 완료 |
| failed | 처리 실패 |

**에러 응답**:
- `404 Not Found`: 제출 없음
  ```json
  {
    "error": "SUBMISSION_NOT_FOUND",
    "message": "제출을 찾을 수 없습니다."
  }
  ```

---

#### 5.2.3 분석 결과 상세 조회

**Endpoint**: `GET /api/v1/results/{submission_id}`

**설명**: 완료된 제출의 전체 분석 결과 조회

**인증**: 필수 (JWT)

**경로 파라미터**:
| 파라미터 | 타입 | 설명 |
|----------|------|------|
| submission_id | string (UUID) | 제출 ID |

**성공 응답** (200 OK):
```json
{
  "submission_id": "880e8400-e29b-41d4-a716-446655440003",
  "problem_id": "660e8400-e29b-41d4-a716-446655440001",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "submitted_at": "2026-05-22T10:30:00Z",
  "status": "completed",
  "htr_result": {
    "raw_latex": "2x + 3 = 7 \\\\ 2x = 7 - 3 \\\\ x = 2",
    "steps": [
      "2x + 3 = 7",
      "2x = 7 - 3",
      "x = 2"
    ],
    "overall_confidence": 0.96
  },
  "analysis_result": {
    "is_correct": false,
    "error_type": "procedural",
    "error_subtype": "sign_error",
    "error_step": 2,
    "feedback_text": "등식의 성질에서 이항할 때는 부호를 반대로 바꿔야 해요...",
    "concept_explanation": "등식의 이항 규칙: 등식의 한 항을 다른 쪽으로 이동할 때...",
    "concept_tags_inferred": ["일차방정식", "이항", "등식의 성질"],
    "confidence": 0.92,
    "processing_time_ms": 3245
  }
}
```

**에러 응답**:
- `404 Not Found`: 제출 없음

---

#### 5.2.4 동기 분석 (간단 테스트용)

**Endpoint**: `POST /api/v1/analyze`

**설명**: 동기 방식으로 즉시 분석 결과 반환 (테스트/데모용, 프로덕션에서는 비추천)

**인증**: 선택적 (테스트용)

**요청 바디**:
```json
{
  "image_base64": "iVBORw0KGgoAAAANSUhEUgAA...",
  "problem_id": null,
  "problem_text": "다음 일차방정식을 푸시오: 2x + 3 = 7",
  "recognized_latex": null,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "student_grade": "middle_2"
}
```

**성공 응답** (200 OK):
```json
{
  "is_correct": false,
  "recognized_latex": "2x + 3 = 7 \\\\ 2x = 7 - 3 \\\\ x = 2",
  "steps": ["2x + 3 = 7", "2x = 7 - 3", "x = 2"],
  "errors": [
    {
      "step": 2,
      "error_type": "procedural",
      "description": "이항할 때 부호를 바꾸지 않았습니다.",
      "correct_expression": "2x = 7 - 3 = 4"
    }
  ],
  "concept_understanding": "등식의 이항 규칙을 정확히 이해하지 못했습니다.",
  "feedback": "등식의 성질에서 이항할 때는 부호를 반대로 바꿔야 해요...",
  "concept_explanation": "등식의 이항 규칙: 등식의 한 항을 다른 쪽으로...",
  "recommended_concept_tags": ["일차방정식", "이항"],
  "confidence": 0.92,
  "processing_time_ms": 3245
}
```

**에러 응답**:
- `400 Bad Request`: 빈 이미지
- `503 Service Unavailable`: AI API 장애

---

#### 5.2.5 이미지 파일 업로드 분석

**Endpoint**: `POST /api/v1/analyze/image`

**설명**: 이미지 파일을 직접 업로드하여 분석 (Base64 대신 multipart)

**인증**: 선택적

**Content-Type**: `multipart/form-data`

**요청 파라미터**:
| 파라미터 | 타입 | 필수 | 설명 |
|----------|------|------|------|
| file | file | O | 이미지 파일 (PNG, JPEG, < 10MB) |
| user_id | string | X | 사용자 ID |
| problem_id | string | X | 문제 ID |
| student_grade | string | X | 학년 (기본: middle_2) |

**성공 응답** (200 OK):
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "problem_id": "660e8400-e29b-41d4-a716-446655440001",
  "is_correct": false,
  "recognized_latex": "2x + 3 = 7 ...",
  "steps": [...],
  "errors": [...],
  "feedback": "...",
  "concept_explanation": "...",
  "recommended_concept_tags": [...],
  "confidence": 0.92,
  "processing_time_ms": 3500
}
```

**에러 응답**:
- `400 Bad Request`: 이미지 크기 초과
- `400 Bad Request`: 지원하지 않는 파일 형식

---

### 5.3 문제은행 API

#### 5.3.1 문제 목록 조회

**Endpoint**: `GET /api/v1/problems`

**설명**: 문제은행 문제 목록을 필터링하여 조회

**인증**: 필수 (JWT)

**쿼리 파라미터**:
| 파라미터 | 타입 | 필수 | 기본값 | 설명 |
|----------|------|------|--------|------|
| grade | string | X | - | 학년 필터 (middle_1 ~ high_3) |
| subject | string | X | - | 과목 필터 (algebra, geometry, calculus, statistics) |
| difficulty | integer | X | - | 난이도 필터 (1 ~ 5) |
| concept_tag | string | X | - | 개념 태그 필터 |
| status | string | X | active | 문제 상태 (active, draft, archived) |
| limit | integer | X | 20 | 최대 조회 개수 (≤ 100) |

**성공 응답** (200 OK):
```json
[
  {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "title": "일차방정식 기본 문제",
    "content_text": "다음 일차방정식을 푸시오: 2x + 3 = 7",
    "subject": "algebra",
    "grade": "middle_2",
    "difficulty": 2,
    "concept_tags": ["일차방정식", "이항"],
    "error_type_tags": ["procedural", "sign_error"],
    "source": "bank",
    "status": "active",
    "estimated_solve_time_min": 5,
    "image_url": null
  }
]
```

---

#### 5.3.2 문제 상세 조회

**Endpoint**: `GET /api/v1/problems/{problem_id}`

**설명**: 특정 문제의 상세 정보 조회

**인증**: 필수 (JWT)

**경로 파라미터**:
| 파라미터 | 타입 | 설명 |
|----------|------|------|
| problem_id | string (UUID) | 문제 ID |

**성공 응답** (200 OK):
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "title": "일차방정식 기본 문제",
  "content_text": "다음 일차방정식을 푸시오: 2x + 3 = 7",
  "subject": "algebra",
  "grade": "middle_2",
  "difficulty": 2,
  "concept_tags": ["일차방정식", "이항"],
  "error_type_tags": ["procedural", "sign_error"],
  "source": "bank",
  "status": "active",
  "estimated_solve_time_min": 5,
  "image_url": null
}
```

**에러 응답**:
- `404 Not Found`: 문제 없음
  ```json
  {
    "error": "PROBLEM_NOT_FOUND",
    "message": "문제를 찾을 수 없습니다."
  }
  ```

---

#### 5.3.3 개인화 문제 추천

**Endpoint**: `GET /api/v1/problems/recommend`

**설명**: 사용자의 학습 이력을 기반으로 맞춤형 문제 추천

**인증**: 필수 (JWT)

**쿼리 파라미터**:
| 파라미터 | 타입 | 필수 | 기본값 | 설명 |
|----------|------|------|--------|------|
| user_id | string (UUID) | O | - | 사용자 ID |
| grade | string | O | - | 학년 |
| subject | string | X | - | 과목 제한 |
| difficulty_min | integer | X | 1 | 최소 난이도 (1 ~ 5) |
| difficulty_max | integer | X | 5 | 최대 난이도 (1 ~ 5) |
| concept_tag | string | X | - | 특정 개념 태그 지정 |
| limit | integer | X | 1 | 추천 문제 개수 (≤ 10) |

**성공 응답** (200 OK):
```json
{
  "problems": [
    {
      "problem_id": "660e8400-e29b-41d4-a716-446655440001",
      "title": "일차방정식 기본 문제",
      "content_text": "다음 일차방정식을 푸시오: 2x + 3 = 7",
      "subject": "algebra",
      "grade": "middle_2",
      "difficulty": 2,
      "concept_tags": ["일차방정식", "이항"],
      "estimated_solve_time_min": 5
    }
  ],
  "recommendation_meta": {
    "reason": "개념 기반 추천",
    "algorithm_version": "1.0"
  }
}
```

**추천 알고리즘**:
1. 사용자의 최근 30일 오답 이력 분석
2. 취약 개념 식별 (mastery_score < 0.6)
3. 취약 개념 70%, 강점 개념 30% 비율로 출제
4. 최근 7일 내 풀이한 문제 제외
5. 연속 3회 정답 시 난이도 +1 조정

**에러 응답**:
- `404 Not Found`: 추천 가능한 문제 없음
  ```json
  {
    "error": "NO_PROBLEMS_AVAILABLE",
    "message": "추천할 수 있는 문제가 없습니다."
  }
  ```

---

#### 5.3.4 문제 등록

**Endpoint**: `POST /api/v1/problems`

**설명**: 문제은행에 새로운 문제 등록

**인증**: 필수 (JWT, 관리자 권한)

**요청 바디**:
```json
{
  "title": "일차방정식 기본 문제",
  "content_text": "다음 일차방정식을 푸시오: 2x + 3 = 7",
  "subject": "algebra",
  "grade": "middle_2",
  "difficulty": 2,
  "concept_tags": ["일차방정식", "이항"],
  "error_type_tags": ["procedural"],
  "answer_latex": "x = 2",
  "curriculum_code": "9MA02-01"
}
```

**성공 응답** (201 Created):
```json
{
  "id": "990e8400-e29b-41d4-a716-446655440010",
  "title": "일차방정식 기본 문제",
  "content_text": "다음 일차방정식을 푸시오: 2x + 3 = 7",
  "subject": "algebra",
  "grade": "middle_2",
  "difficulty": 2,
  "concept_tags": ["일차방정식", "이항"],
  "error_type_tags": ["procedural"],
  "source": "bank",
  "status": "active",
  "estimated_solve_time_min": 5,
  "image_url": null
}
```

---

#### 5.3.5 AI 유사 문제 생성

**Endpoint**: `POST /api/v1/problems/generate`

**설명**: GPT-4o를 사용하여 기존 문제와 유사한 새 문제 생성

**인증**: 필수 (JWT)

**요청 바디**:
```json
{
  "concept_tags": ["일차방정식", "이항"],
  "difficulty": 2,
  "error_type": "procedural",
  "grade": "middle_2",
  "source_problem_id": "660e8400-e29b-41d4-a716-446655440001"
}
```

**필드 설명**:
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| concept_tags | array[string] | O | 개념 태그 목록 |
| difficulty | integer | O | 난이도 (1 ~ 5) |
| error_type | string | O | 목표 오류 유형 |
| grade | string | O | 학년 |
| source_problem_id | string (UUID) | X | 참조할 원본 문제 ID |

**성공 응답** (200 OK):
```json
{
  "problem_id": "aa0e8400-e29b-41d4-a716-446655440020",
  "problem_latex": "다음 일차방정식을 푸시오: 3x - 5 = 10",
  "answer_latex": "x = 5",
  "hint": "먼저 -5를 오른쪽으로 이항해보세요.",
  "concept_ids": ["일차방정식", "이항"]
}
```

**에러 응답**:
- `503 Service Unavailable`: GPT-4o API 장애
  ```json
  {
    "error": "LLM_API_UNAVAILABLE",
    "message": "AI 서비스가 일시적으로 사용할 수 없습니다. 잠시 후 다시 시도해주세요."
  }
  ```

---

### 5.4 사용자 관리 API

#### 5.4.1 학습 리포트 조회

**Endpoint**: `GET /api/v1/users/{user_id}/report`

**설명**: 사용자의 학습 통계 및 리포트 조회

**인증**: 필수 (JWT, 본인 또는 학부모)

**경로 파라미터**:
| 파라미터 | 타입 | 설명 |
|----------|------|------|
| user_id | string (UUID) | 사용자 ID |

**쿼리 파라미터**:
| 파라미터 | 타입 | 필수 | 기본값 | 설명 |
|----------|------|------|--------|------|
| period | string | X | week | 조회 기간 (week, month, all) |
| start_date | string | X | - | 시작 날짜 (ISO 8601) |
| end_date | string | X | - | 종료 날짜 (ISO 8601) |

**성공 응답** (200 OK):
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "period": "week",
  "summary": {
    "total_problems_solved": 42,
    "correct_count": 35,
    "accuracy_rate": 0.833,
    "total_learning_time_min": 280,
    "consecutive_days": 7,
    "daily_goal_achievement_rate": 0.857
  },
  "error_distribution": {
    "conceptual": 3,
    "procedural": 5,
    "computational": 2,
    "comprehension": 1
  },
  "weak_concepts": [
    {
      "concept_id": "일차방정식_이항",
      "concept_name": "일차방정식 이항",
      "mastery_score": 0.45,
      "error_count": 5,
      "last_error_date": "2026-05-21T15:30:00Z"
    },
    {
      "concept_id": "분수_계산",
      "concept_name": "분수 사칙연산",
      "mastery_score": 0.52,
      "error_count": 3,
      "last_error_date": "2026-05-20T14:20:00Z"
    }
  ],
  "daily_activity": [
    {"date": "2026-05-16", "problems_solved": 5, "accuracy": 0.8},
    {"date": "2026-05-17", "problems_solved": 6, "accuracy": 0.833},
    {"date": "2026-05-18", "problems_solved": 7, "accuracy": 0.857},
    {"date": "2026-05-19", "problems_solved": 5, "accuracy": 0.6},
    {"date": "2026-05-20", "problems_solved": 8, "accuracy": 0.875},
    {"date": "2026-05-21", "problems_solved": 6, "accuracy": 0.833},
    {"date": "2026-05-22", "problems_solved": 5, "accuracy": 1.0}
  ]
}
```

---

#### 5.4.2 개념 습득 현황 조회

**Endpoint**: `GET /api/v1/users/{user_id}/mastery`

**설명**: 사용자의 개념별 습득 현황 조회

**인증**: 필수 (JWT, 본인 또는 학부모)

**경로 파라미터**:
| 파라미터 | 타입 | 설명 |
|----------|------|------|
| user_id | string (UUID) | 사용자 ID |

**쿼리 파라미터**:
| 파라미터 | 타입 | 필수 | 기본값 | 설명 |
|----------|------|------|--------|------|
| status | string | X | all | 상태 필터 (learning, mastered, review_due, all) |
| subject | string | X | - | 과목 필터 |

**성공 응답** (200 OK):
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "concepts": [
    {
      "concept_id": "일차방정식_기본",
      "concept_name": "일차방정식 기본",
      "subject": "algebra",
      "mastery_score": 0.85,
      "status": "mastered",
      "consecutive_correct": 5,
      "last_practiced": "2026-05-20T10:30:00Z",
      "next_review_at": "2026-05-27T10:30:00Z"
    },
    {
      "concept_id": "일차방정식_이항",
      "concept_name": "일차방정식 이항",
      "subject": "algebra",
      "mastery_score": 0.45,
      "status": "learning",
      "consecutive_correct": 0,
      "last_practiced": "2026-05-21T15:30:00Z",
      "next_review_at": null
    },
    {
      "concept_id": "분수_덧셈",
      "concept_name": "분수 덧셈",
      "subject": "algebra",
      "mastery_score": 0.75,
      "status": "review_due",
      "consecutive_correct": 3,
      "last_practiced": "2026-05-15T14:00:00Z",
      "next_review_at": "2026-05-22T14:00:00Z"
    }
  ],
  "summary": {
    "total_concepts": 45,
    "mastered_count": 30,
    "learning_count": 12,
    "review_due_count": 3
  }
}
```

---

#### 5.4.3 오답 노트 조회

**Endpoint**: `GET /api/v1/users/{user_id}/wrong-notes`

**설명**: 사용자의 오답 문제 목록 조회

**인증**: 필수 (JWT, 본인)

**경로 파라미터**:
| 파라미터 | 타입 | 설명 |
|----------|------|------|
| user_id | string (UUID) | 사용자 ID |

**쿼리 파라미터**:
| 파라미터 | 타입 | 필수 | 기본값 | 설명 |
|----------|------|------|--------|------|
| error_type | string | X | - | 오류 유형 필터 (conceptual, procedural, computational, comprehension) |
| concept_tag | string | X | - | 개념 태그 필터 |
| start_date | string | X | - | 시작 날짜 (ISO 8601) |
| end_date | string | X | - | 종료 날짜 (ISO 8601) |
| limit | integer | X | 20 | 최대 조회 개수 |
| offset | integer | X | 0 | 페이지 오프셋 |

**성공 응답** (200 OK):
```json
{
  "items": [
    {
      "submission_id": "880e8400-e29b-41d4-a716-446655440003",
      "problem_id": "660e8400-e29b-41d4-a716-446655440001",
      "problem_title": "일차방정식 기본 문제",
      "problem_text": "다음 일차방정식을 푸시오: 2x + 3 = 7",
      "error_type": "procedural",
      "error_subtype": "sign_error",
      "solved_at": "2026-05-21T15:30:00Z",
      "concept_tags": ["일차방정식", "이항"],
      "feedback_preview": "이항할 때 부호를 바꾸지 않았습니다...",
      "retry_count": 0,
      "mastered": false
    }
  ],
  "total": 15,
  "limit": 20,
  "offset": 0,
  "has_more": false
}
```

---

### 5.5 개념 관리 API

#### 5.5.1 개념 목록 조회

**Endpoint**: `GET /api/v1/concepts`

**설명**: 교육과정 개념 목록 조회

**인증**: 선택적

**쿼리 파라미터**:
| 파라미터 | 타입 | 필수 | 기본값 | 설명 |
|----------|------|------|--------|------|
| grade | string | X | - | 학년 필터 |
| subject | string | X | - | 과목 필터 |
| parent_id | string | X | - | 상위 개념 ID (계층 구조) |

**성공 응답** (200 OK):
```json
[
  {
    "id": "일차방정식_기본",
    "name": "일차방정식의 기본",
    "subject": "algebra",
    "grade": "middle_1",
    "description": "일차방정식의 정의와 기본 성질",
    "parent_id": null,
    "curriculum_code": "9MA02-01",
    "difficulty_level": 1,
    "prerequisite_concept_ids": []
  },
  {
    "id": "일차방정식_이항",
    "name": "일차방정식의 이항",
    "subject": "algebra",
    "grade": "middle_1",
    "description": "등식의 성질을 이용한 이항 규칙",
    "parent_id": "일차방정식_기본",
    "curriculum_code": "9MA02-01",
    "difficulty_level": 2,
    "prerequisite_concept_ids": ["일차방정식_기본", "등식의_성질"]
  }
]
```

---

#### 5.5.2 개념 상세 조회

**Endpoint**: `GET /api/v1/concepts/{concept_id}`

**설명**: 특정 개념의 상세 정보 조회

**인증**: 선택적

**경로 파라미터**:
| 파라미터 | 타입 | 설명 |
|----------|------|------|
| concept_id | string | 개념 ID |

**성공 응답** (200 OK):
```json
{
  "id": "일차방정식_이항",
  "name": "일차방정식의 이항",
  "subject": "algebra",
  "grade": "middle_1",
  "description": "등식의 성질을 이용한 이항 규칙을 학습합니다.",
  "parent_id": "일차방정식_기본",
  "curriculum_code": "9MA02-01",
  "difficulty_level": 2,
  "prerequisite_concept_ids": ["일차방정식_기본", "등식의_성질"],
  "related_concept_ids": ["등식의_성질", "일차방정식_풀이"],
  "formula": "a + c = b \\Rightarrow a = b - c",
  "examples": [
    {
      "title": "예제 1",
      "problem": "x + 3 = 7일 때 x의 값을 구하시오.",
      "solution": "x = 7 - 3 = 4"
    }
  ],
  "common_errors": [
    {
      "error_type": "sign_error",
      "description": "이항 시 부호를 바꾸지 않는 오류",
      "example": "x + 3 = 7 → x = 7 + 3 (잘못됨)"
    }
  ]
}
```

---

#### 5.5.3 AI 개념 설명 생성

**Endpoint**: `GET /api/v1/concepts/{concept_id}/explanation`

**설명**: GPT-4o를 사용하여 학생 수준에 맞는 개념 설명 생성

**인증**: 필수 (JWT)

**경로 파라미터**:
| 파라미터 | 타입 | 설명 |
|----------|------|------|
| concept_id | string | 개념 ID |

**쿼리 파라미터**:
| 파라미터 | 타입 | 필수 | 기본값 | 설명 |
|----------|------|------|--------|------|
| grade | string | O | - | 학생 학년 |
| context | string | X | - | 추가 컨텍스트 (오답 유형 등) |

**성공 응답** (200 OK):
```json
{
  "concept_id": "일차방정식_이항",
  "concept_name": "일차방정식의 이항",
  "explanation": "등식에서 한 항을 다른 쪽으로 이동하는 것을 '이항'이라고 해요. 이항할 때는 반드시 부호를 반대로 바꿔야 합니다.\n\n예를 들어, x + 3 = 7에서 +3을 오른쪽으로 이항하면 x = 7 - 3이 됩니다.\n\n왜 부호를 바꿔야 할까요? 양쪽에서 같은 수를 빼거나 더하는 등식의 성질 때문입니다. x + 3 = 7의 양쪽에서 3을 빼면 x = 7 - 3이 되죠!",
  "formula_latex": "a + c = b \\Rightarrow a = b - c",
  "key_points": [
    "이항 = 등식의 한쪽에 있는 항을 다른 쪽으로 옮기는 것",
    "이항할 때는 부호를 반대로 바꾼다 (+ ↔ -)",
    "등식의 성질(양변에 같은 수를 더하거나 빼도 등식이 성립)이 기본 원리"
  ],
  "examples": [
    {
      "problem": "x + 5 = 12",
      "solution": "x = 12 - 5 = 7"
    },
    {
      "problem": "x - 3 = 10",
      "solution": "x = 10 + 3 = 13"
    }
  ],
  "video_url": "https://example.com/video/transposition",
  "practice_problem_ids": [
    "660e8400-e29b-41d4-a716-446655440001",
    "660e8400-e29b-41d4-a716-446655440002"
  ]
}
```

---

#### 5.5.4 개념 등록 (관리자)

**Endpoint**: `POST /api/v1/concepts`

**설명**: 새로운 개념을 교육과정에 등록

**인증**: 필수 (JWT, 관리자 권한)

**요청 바디**:
```json
{
  "id": "이차방정식_근의공식",
  "name": "이차방정식의 근의 공식",
  "subject": "algebra",
  "grade": "middle_3",
  "description": "이차방정식을 근의 공식으로 푸는 방법",
  "parent_id": "이차방정식_기본",
  "curriculum_code": "9MA03-02",
  "difficulty_level": 4,
  "prerequisite_concept_ids": ["이차방정식_기본", "판별식"],
  "formula": "x = \\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}"
}
```

**성공 응답** (201 Created):
```json
{
  "id": "이차방정식_근의공식",
  "name": "이차방정식의 근의 공식",
  "subject": "algebra",
  "grade": "middle_3",
  "description": "이차방정식을 근의 공식으로 푸는 방법",
  "parent_id": "이차방정식_기본",
  "curriculum_code": "9MA03-02",
  "difficulty_level": 4,
  "prerequisite_concept_ids": ["이차방정식_기본", "판별식"],
  "formula": "x = \\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}",
  "created_at": "2026-05-22T11:00:00Z"
}
```

---

## 6. WebSocket 프로토콜

### 6.1 연결 엔드포인트

**URL**: `wss://api.mathlens.ai/ws/v1/submissions/{submission_id}`

**프로토콜**: WebSocket Secure (WSS)

**인증**: JWT 토큰 (연결 시 전송)

### 6.2 연결 플로우

```
[Client]
    │
    │ 1. WebSocket 연결 시도
    │    wss://api.mathlens.ai/ws/v1/submissions/{submission_id}
    │
    ▼
[Server]
    │
    │ 2. 연결 수락 (HTTP 101 Switching Protocols)
    │
    ▼
[Client]
    │
    │ 3. 인증 메시지 전송
    │    {"type": "auth", "token": "jwt_access_token"}
    │
    ▼
[Server]
    │
    │ 4. 인증 성공 확인
    │    {"type": "auth_success"}
    │
    ▼
[Server → Client]
    │
    │ 5. 상태 업데이트 전송 (비동기 처리 진행 중)
    │    - received
    │    - processing
    │    - htr_done
    │    - analysis_done
    │
    ▼
[Client]
    │
    │ 6. Ping 응답 (연결 유지)
    │    {"type": "pong"}
```

### 6.3 메시지 포맷

#### 6.3.1 Client → Server

**인증 메시지**:
```json
{
  "type": "auth",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Pong 응답**:
```json
{
  "type": "pong"
}
```

#### 6.3.2 Server → Client

**인증 성공**:
```json
{
  "type": "auth_success",
  "submission_id": "880e8400-e29b-41d4-a716-446655440003"
}
```

**상태 업데이트: 접수**:
```json
{
  "type": "status",
  "submission_id": "880e8400-e29b-41d4-a716-446655440003",
  "stage": "received",
  "timestamp": "2026-05-22T10:30:00Z"
}
```

**상태 업데이트: 처리 중**:
```json
{
  "type": "status",
  "submission_id": "880e8400-e29b-41d4-a716-446655440003",
  "stage": "processing",
  "timestamp": "2026-05-22T10:30:01Z"
}
```

**상태 업데이트: HTR 완료**:
```json
{
  "type": "status",
  "submission_id": "880e8400-e29b-41d4-a716-446655440003",
  "stage": "htr_done",
  "latex_preview": "2x + 3 = 7 \\\\ 2x = 4 \\\\ x = 2",
  "confidence": 0.96,
  "timestamp": "2026-05-22T10:30:03Z"
}
```

**상태 업데이트: 분석 완료**:
```json
{
  "type": "status",
  "submission_id": "880e8400-e29b-41d4-a716-446655440003",
  "stage": "analysis_done",
  "result_id": "bb0e8400-e29b-41d4-a716-446655440030",
  "is_correct": false,
  "timestamp": "2026-05-22T10:30:05Z"
}
```

**에러 메시지**:
```json
{
  "type": "error",
  "submission_id": "880e8400-e29b-41d4-a716-446655440003",
  "error_code": "HTR_TIMEOUT",
  "message": "손글씨 인식이 시간 초과되었습니다. 다시 시도해주세요.",
  "timestamp": "2026-05-22T10:30:10Z"
}
```

**Ping (연결 유지)**:
```json
{
  "type": "ping"
}
```

### 6.4 연결 종료

**정상 종료**: Client가 `close()` 호출
**비정상 종료**: Timeout, Network Error
**서버 종료**: 처리 완료 또는 에러 후 서버가 연결 종료

---

## 7. 에러 코드 정의

### 7.1 인증 에러 (4xx)

| 에러 코드 | HTTP 상태 | 설명 |
|----------|-----------|------|
| UNAUTHORIZED | 401 | 인증 토큰 없음 또는 유효하지 않음 |
| TOKEN_EXPIRED | 401 | 액세스 토큰 만료 |
| INVALID_REFRESH_TOKEN | 401 | 리프레시 토큰 유효하지 않음 |
| INVALID_CREDENTIALS | 401 | 이메일 또는 비밀번호 오류 |
| FORBIDDEN | 403 | 접근 권한 없음 |

### 7.2 요청 검증 에러 (4xx)

| 에러 코드 | HTTP 상태 | 설명 |
|----------|-----------|------|
| VALIDATION_ERROR | 400 | 요청 데이터 유효성 검증 실패 |
| SUBMISSION_EMPTY_CANVAS | 400 | 빈 캔버스 제출 |
| SUBMISSION_IMAGE_TOO_LARGE | 413 | 이미지 크기 초과 (> 2MB) |
| EMAIL_ALREADY_EXISTS | 409 | 이메일 중복 |

### 7.3 리소스 에러 (4xx)

| 에러 코드 | HTTP 상태 | 설명 |
|----------|-----------|------|
| PROBLEM_NOT_FOUND | 404 | 문제를 찾을 수 없음 |
| SUBMISSION_NOT_FOUND | 404 | 제출을 찾을 수 없음 |
| USER_NOT_FOUND | 404 | 사용자를 찾을 수 없음 |
| CONCEPT_NOT_FOUND | 404 | 개념을 찾을 수 없음 |
| NO_PROBLEMS_AVAILABLE | 404 | 추천 가능한 문제 없음 |

### 7.4 Rate Limiting 에러 (4xx)

| 에러 코드 | HTTP 상태 | 설명 |
|----------|-----------|------|
| RATE_LIMIT_EXCEEDED | 429 | API 호출 횟수 제한 초과 |

### 7.5 서버 에러 (5xx)

| 에러 코드 | HTTP 상태 | 설명 |
|----------|-----------|------|
| INTERNAL_SERVER_ERROR | 500 | 예상치 못한 서버 오류 |
| ANALYSIS_ERROR | 500 | AI 분석 실패 |
| HTR_TIMEOUT | 500 | 손글씨 인식 시간 초과 |
| LLM_API_UNAVAILABLE | 503 | GPT-4o API 일시 장애 |
| DATABASE_ERROR | 503 | 데이터베이스 연결 실패 |

---

## 8. Rate Limiting

### 8.1 제한 정책

| 엔드포인트 | 제한 | 기준 | 초과 시 복구 |
|-----------|------|------|------------|
| `POST /api/v1/submissions` | 60회/시간 | user_id | 1시간 후 |
| `GET /api/v1/problems/recommend` | 100회/시간 | user_id | 1시간 후 |
| `POST /api/v1/auth/token` | 5회/15분 | IP 주소 | 15분 후 |
| `POST /api/v1/problems/generate` | 10회/시간 | user_id | 1시간 후 |
| 기타 GET 엔드포인트 | 1000회/시간 | user_id | 1시간 후 |

### 8.2 Rate Limit 헤더

모든 응답에 다음 헤더가 포함됩니다:

```http
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1716389400
```

| 헤더 | 설명 |
|------|------|
| `X-RateLimit-Limit` | 시간당 최대 요청 수 |
| `X-RateLimit-Remaining` | 남은 요청 수 |
| `X-RateLimit-Reset` | 제한 초기화 시각 (Unix timestamp) |

### 8.3 429 응답 예시

```http
HTTP/1.1 429 Too Many Requests
Content-Type: application/json
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1716389400
Retry-After: 3600

{
  "error": "RATE_LIMIT_EXCEEDED",
  "message": "API 호출 횟수를 초과했습니다. 1시간 후 다시 시도해주세요.",
  "retry_after_seconds": 3600
}
```

---

## 9. 보안 고려사항

### 9.1 HTTPS 필수

- 모든 API 통신은 HTTPS (TLS 1.3) 사용
- HTTP 요청은 자동으로 HTTPS로 리다이렉트

### 9.2 JWT 보안

**토큰 저장**:
- **iOS**: Keychain
- **Android**: EncryptedSharedPreferences
- **절대 금지**: LocalStorage, SharedPreferences (평문)

**토큰 갱신**:
- Access Token 만료 10분 전 자동 갱신 권장
- Refresh Token 만료 시 재로그인 필요

### 9.3 입력 검증

**서버 측**:
- 모든 입력에 대해 타입, 길이, 형식 검증
- SQL Injection 방지: ORM 파라미터 바인딩
- XSS 방지: HTML 이스케이프 처리

**클라이언트 측**:
- 최소한의 검증 (UX 개선용)
- 서버 검증을 신뢰의 기준으로 삼음

### 9.4 개인정보 보호

**수집 최소화**:
- 필수: 이메일, 학년
- 선택: 이름, 생년월일

**보존 기간**:
- 풀이 이미지: 분석 후 30일 (사용자 설정 가능)
- 분석 결과: 계정 삭제 시까지
- 오답 노트: 계정 삭제 시까지

**GDPR 준수**:
- 데이터 삭제 요청 지원 (`DELETE /api/v1/users/{user_id}`)
- 데이터 내보내기 지원 (`GET /api/v1/users/{user_id}/export`)

### 9.5 CORS 설정

**허용 Origin**:
- `https://mathlens.ai`
- `https://app.mathlens.ai`
- 개발 환경: `http://localhost:*` (개발 모드만)

**허용 메서드**: GET, POST, PUT, DELETE, OPTIONS

**허용 헤더**: Authorization, Content-Type

---

## 10. API 버전 관리

### 10.1 버전 관리 정책

**현재 버전**: v1 (`/api/v1`)

**하위 호환성**:
- 새로운 필드 추가: 하위 호환 유지
- 필드 제거/변경: 신규 버전 릴리즈 (v2)

**Deprecation 정책**:
- 신규 버전 릴리즈 후 6개월 동안 구버전 유지
- 3개월 전 Deprecation 공지
- 응답 헤더에 `Deprecation` 헤더 포함

### 10.2 API 변경 이력

| 버전 | 릴리즈 날짜 | 주요 변경 사항 |
|------|------------|---------------|
| v1.0 | 2026-05-22 | 초기 API 릴리즈 |

---

## 부록

### A. 샘플 코드

#### A.1 Python (requests)

```python
import requests

# 로그인
response = requests.post(
    "https://api.mathlens.ai/api/v1/auth/token",
    data={"username": "student@example.com", "password": "password123"}
)
tokens = response.json()
access_token = tokens["access_token"]

# 문제 추천
response = requests.get(
    "https://api.mathlens.ai/api/v1/problems/recommend",
    params={"user_id": "550e8400-e29b-41d4-a716-446655440000", "grade": "middle_2"},
    headers={"Authorization": f"Bearer {access_token}"}
)
problems = response.json()
print(problems)
```

#### A.2 TypeScript (Axios)

```typescript
import axios from 'axios';

const api = axios.create({
  baseURL: 'https://api.mathlens.ai/api/v1',
});

// 로그인
const loginResponse = await api.post('/auth/token', {
  username: 'student@example.com',
  password: 'password123',
}, {
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
});

const { access_token } = loginResponse.data;

// 풀이 제출
const submissionResponse = await api.post('/submissions', {
  user_id: '550e8400-e29b-41d4-a716-446655440000',
  problem_id: '660e8400-e29b-41d4-a716-446655440001',
  image_base64: 'iVBORw0KGgoAAAANSUhEUgAA...',
  image_mime_type: 'image/png',
}, {
  headers: { Authorization: `Bearer ${access_token}` }
});

console.log(submissionResponse.data);
```

---

**문서 개정 이력**:

| 버전 | 날짜 | 변경 내용 | 작성자 |
|------|------|-----------|--------|
| v1.0 | 2026-05-22 | 초기 API 설계 문서 작성 | MathLens AI 개발팀 |

---

*본 문서는 MathLens AI 프로젝트의 공식 API 명세서입니다.*

*© 2026 MathLens AI Project. All rights reserved.*
