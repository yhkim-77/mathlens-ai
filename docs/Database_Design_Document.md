# MathLens AI — Database Design Document (데이터베이스 설계서)

**Document Version:** v1.0
**Date:** 2026-05-22
**Document Type:** Database Design Document (DDD)
**Author:** MathLens AI Engineering Team
**Status:** Draft

---

## Table of Contents

1. [개요 (Overview)](#1-개요-overview)
2. [데이터베이스 아키텍처 (Database Architecture)](#2-데이터베이스-아키텍처-database-architecture)
3. [물리적 데이터 모델 (Physical Data Model)](#3-물리적-데이터-모델-physical-data-model)
4. [테이블 상세 설계 (Table Specifications)](#4-테이블-상세-설계-table-specifications)
5. [인덱스 전략 (Indexing Strategy)](#5-인덱스-전략-indexing-strategy)
6. [관계 및 제약조건 (Relationships & Constraints)](#6-관계-및-제약조건-relationships--constraints)
7. [데이터 타입 및 도메인 (Data Types & Domains)](#7-데이터-타입-및-도메인-data-types--domains)
8. [성능 최적화 (Performance Optimization)](#8-성능-최적화-performance-optimization)
9. [백업 및 복구 전략 (Backup & Recovery)](#9-백업-및-복구-전략-backup--recovery)
10. [마이그레이션 전략 (Migration Strategy)](#10-마이그레이션-전략-migration-strategy)
11. [보안 및 접근 제어 (Security & Access Control)](#11-보안-및-접근-제어-security--access-control)

---

## 1. 개요 (Overview)

### 1.1 목적 (Purpose)

본 데이터베이스 설계 문서는 MathLens AI 시스템의 데이터 저장소 설계를 상세히 정의합니다. 이 문서는 개발자, DBA, 시스템 관리자가 데이터베이스 구조를 이해하고 구현하는 데 필요한 모든 정보를 제공합니다.

### 1.2 범위 (Scope)

이 문서는 다음을 포함합니다:

- 관계형 데이터베이스 스키마 (PostgreSQL 15+)
- 테이블 구조 및 컬럼 정의
- 인덱스 및 제약조건
- 관계 다이어그램 (ERD)
- 쿼리 최적화 전략
- 데이터 마이그레이션 계획

다음은 범위 밖입니다:

- 애플리케이션 레벨 비즈니스 로직
- API 명세 (별도 문서 참조)
- 프론트엔드 UI/UX 설계

### 1.3 데이터베이스 기술 스택 (Technology Stack)

| 항목 | 선택 기술 | 버전 | 이유 |
|------|----------|------|------|
| **RDBMS** | PostgreSQL | 15+ | 고급 데이터 타입(JSONB, Array), 트랜잭션 ACID 보장, 확장성 |
| **개발 환경 DB** | SQLite | 3.40+ | 로컬 개발 편의성, Zero-configuration |
| **ORM** | SQLAlchemy | 2.0+ | Python 비동기 지원, 타입 안전성 |
| **마이그레이션** | Alembic | 1.12+ | SQLAlchemy 공식 마이그레이션 도구 |
| **연결 풀링** | asyncpg | 0.29+ | PostgreSQL 고성능 비동기 드라이버 |

---

## 2. 데이터베이스 아키텍처 (Database Architecture)

### 2.1 전체 아키텍처 다이어그램

```
┌─────────────────────────────────────────────────────────────────┐
│                     Application Layer                           │
│                    (FastAPI + SQLAlchemy)                        │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ asyncpg / psycopg2
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                   Connection Pool (PgBouncer)                   │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │
┌────────────────────────▼────────────────────────────────────────┐
│              PostgreSQL 15 Primary (Read/Write)                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Database: mathlens_production                           │   │
│  │  ├── Schema: public (default)                            │   │
│  │  │   ├── users                                           │   │
│  │  │   ├── problems                                        │   │
│  │  │   ├── submissions                                     │   │
│  │  │   ├── recognition_results                            │   │
│  │  │   ├── concept_mastery                                │   │
│  │  │   └── user_problem_history                           │   │
│  │  └── Schema: analytics (future)                          │   │
│  └──────────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────────┘
                         │ Streaming Replication
                         │
┌────────────────────────▼────────────────────────────────────────┐
│          PostgreSQL 15 Replica (Read-Only)                      │
│          (Used for analytics & reporting queries)               │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 데이터베이스 인스턴스 구성

#### Production 환경

| 항목 | 구성 |
|------|------|
| Primary | PostgreSQL 15 (Multi-AZ) — RDS 또는 자체 호스팅 |
| Replica | 1대 이상 (읽기 전용, 분석 쿼리용) |
| Backup | 자동 일일 백업, 7일 보관, Point-in-Time Recovery 활성화 |
| Storage | SSD (IOPS 최소 3000) |
| CPU/Memory | 최소 4 vCPU, 16GB RAM (확장 가능) |

#### Development 환경

| 항목 | 구성 |
|------|------|
| Local | SQLite 3.40+ (docker-compose로 PostgreSQL 사용 권장) |
| Staging | PostgreSQL 15 (단일 인스턴스) |

---

## 3. 물리적 데이터 모델 (Physical Data Model)

### 3.1 Entity Relationship Diagram (ERD)

```
┌─────────────┐
│   users     │
├─────────────┤
│ id (PK)     │◄──────┐
│ email       │       │
│ password    │       │
│ name        │       │
│ grade       │       │
│ ...         │       │
└─────────────┘       │
                      │ user_id (FK)
                      │
        ┌─────────────┴──────────────┬─────────────────────┐
        │                            │                     │
┌───────▼─────────┐      ┌──────────▼──────────┐   ┌─────▼────────────┐
│  submissions    │      │ concept_mastery     │   │ user_problem_    │
├─────────────────┤      ├─────────────────────┤   │   history        │
│ id (PK)         │      │ id (PK)             │   ├──────────────────┤
│ user_id (FK)    │      │ user_id (FK)        │   │ id (PK)          │
│ problem_id (FK) │──┐   │ concept_id          │   │ user_id (FK)     │
│ image_s3_key    │  │   │ mastery_score       │   │ problem_id (FK)  │
│ status          │  │   │ consecutive_correct │   │ submission_id    │
│ submitted_at    │  │   │ status              │   │ is_correct       │
│ ...             │  │   │ ...                 │   │ error_type       │
└─────────┬───────┘  │   └─────────────────────┘   │ ...              │
          │          │                              └──────────────────┘
          │          │
          │ submission_id (FK)
          │          │
┌─────────▼──────────┴───┐
│ recognition_results    │
├────────────────────────┤
│ id (PK)                │
│ submission_id (FK,UQ)  │
│ is_correct             │
│ error_steps (JSONB)    │
│ feedback_text          │
│ correct_solution_latex │
│ confidence             │
│ ...                    │
└────────────────────────┘

┌─────────────┐
│  problems   │
├─────────────┤
│ id (PK)     │◄────────────────┐
│ title       │                 │ problem_id (FK)
│ content_text│                 │
│ answer_latex│        ┌────────┴──────────┐
│ subject     │        │  submissions      │
│ grade       │        │  (FK relationship)│
│ difficulty  │        └───────────────────┘
│ concept_tags│
│ status      │
│ ...         │
└─────────────┘
```

### 3.2 데이터베이스 스키마 구조

```
mathlens_production (Database)
│
├── public (Schema) — 기본 애플리케이션 데이터
│   ├── users
│   ├── problems
│   ├── submissions
│   ├── recognition_results
│   ├── concept_mastery
│   └── user_problem_history
│
└── analytics (Schema) — 분석 및 리포트 데이터 (Phase 2+)
    ├── daily_active_users
    ├── submission_stats
    └── concept_performance_aggregates
```

---

## 4. 테이블 상세 설계 (Table Specifications)

### 4.1 users (사용자)

**목적**: 학습자 및 학부모/교사 계정 정보 저장

**DDL**:

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255),
    name VARCHAR(100) NOT NULL,
    grade VARCHAR(20) NOT NULL,
    current_difficulty INT DEFAULT 3 CHECK (current_difficulty BETWEEN 1 AND 5),
    daily_goal INT DEFAULT 5,
    notification_enabled BOOLEAN DEFAULT TRUE,
    profile_image_key VARCHAR(255),
    oauth_provider VARCHAR(50),  -- 'apple', 'google', 'kakao', NULL for password
    oauth_sub VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_active_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_users_email ON users (email);
CREATE INDEX idx_users_grade ON users (grade);
CREATE INDEX idx_users_last_active ON users (last_active_at DESC);

-- Comments
COMMENT ON TABLE users IS '학습자 및 학부모/교사 계정';
COMMENT ON COLUMN users.grade IS '학년: middle_1, middle_2, middle_3, high_1, high_2, high_3, reexaminee';
COMMENT ON COLUMN users.current_difficulty IS '현재 난이도 레벨 (1=하, 5=상)';
COMMENT ON COLUMN users.oauth_provider IS 'OAuth 제공자: apple, google, kakao';
```

**컬럼 설명**:

| 컬럼명 | 데이터 타입 | NULL | 기본값 | 설명 |
|--------|-----------|------|--------|------|
| id | UUID | NO | gen_random_uuid() | 사용자 고유 ID |
| email | VARCHAR(255) | NO | - | 이메일 (로그인 ID) |
| hashed_password | VARCHAR(255) | YES | - | bcrypt 해시 비밀번호 (OAuth의 경우 NULL) |
| name | VARCHAR(100) | NO | - | 사용자 이름 |
| grade | VARCHAR(20) | NO | - | 학년 (middle_1 ~ high_3, reexaminee) |
| current_difficulty | INT | NO | 3 | 현재 추천 문제 난이도 (1~5) |
| daily_goal | INT | NO | 5 | 일일 학습 목표 문제 수 |
| notification_enabled | BOOLEAN | NO | TRUE | 푸시 알림 활성화 여부 |
| profile_image_key | VARCHAR(255) | YES | - | S3 프로필 이미지 키 |
| oauth_provider | VARCHAR(50) | YES | - | OAuth 제공자 (apple/google/kakao) |
| oauth_sub | VARCHAR(255) | YES | - | OAuth Subject (제공자별 고유 ID) |
| created_at | TIMESTAMP WITH TIME ZONE | NO | CURRENT_TIMESTAMP | 계정 생성일 |
| last_active_at | TIMESTAMP WITH TIME ZONE | YES | - | 마지막 활동 일시 |
| updated_at | TIMESTAMP WITH TIME ZONE | NO | CURRENT_TIMESTAMP | 마지막 업데이트 일시 |

---

### 4.2 problems (문제)

**목적**: 문제은행 데이터 저장

**DDL**:

```sql
CREATE TABLE problems (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    content_text TEXT NOT NULL,
    content_image_key VARCHAR(255),
    answer_latex TEXT NOT NULL,
    solution_steps JSONB,
    subject VARCHAR(50) NOT NULL,
    grade VARCHAR(20) NOT NULL,
    difficulty INT NOT NULL CHECK (difficulty BETWEEN 1 AND 5),
    concept_tags TEXT[] NOT NULL,
    error_type_tags TEXT[],
    curriculum_code VARCHAR(50),
    source VARCHAR(50) DEFAULT 'bank',
    status VARCHAR(20) DEFAULT 'active',
    parent_problem_id UUID REFERENCES problems(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_problems_grade_difficulty ON problems (grade, difficulty, status);
CREATE INDEX idx_problems_subject ON problems (subject);
CREATE INDEX idx_problems_status ON problems (status);
CREATE INDEX idx_problems_concept_tags ON problems USING GIN (concept_tags);
CREATE INDEX idx_problems_source ON problems (source);

-- Comments
COMMENT ON TABLE problems IS '문제은행 테이블';
COMMENT ON COLUMN problems.content_text IS '문제 내용 (LaTeX 포함 가능)';
COMMENT ON COLUMN problems.solution_steps IS '정답 풀이 단계 (JSONB 배열)';
COMMENT ON COLUMN problems.subject IS '과목: algebra, geometry, calculus, statistics';
COMMENT ON COLUMN problems.concept_tags IS '개념 태그 배열 (예: ["이차방정식", "인수분해"])';
COMMENT ON COLUMN problems.source IS '출처: bank, llm_generated, textbook, user_uploaded';
COMMENT ON COLUMN problems.status IS '상태: draft, review, active, archived';
COMMENT ON COLUMN problems.parent_problem_id IS '원본 문제 ID (유사 문제 생성 시)';
```

**solution_steps JSONB 구조 예시**:

```json
[
  {
    "step": 1,
    "latex": "2x + 3 = 7",
    "description": "주어진 방정식",
    "type": "given"
  },
  {
    "step": 2,
    "latex": "2x = 7 - 3",
    "description": "3을 우변으로 이항",
    "type": "transformation"
  },
  {
    "step": 3,
    "latex": "2x = 4",
    "description": "우변 계산",
    "type": "simplification"
  },
  {
    "step": 4,
    "latex": "x = 2",
    "description": "양변을 2로 나눔",
    "type": "solution"
  }
]
```

---

### 4.3 submissions (제출)

**목적**: 학습자의 풀이 제출 이력 저장

**DDL**:

```sql
CREATE TABLE submissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    problem_id UUID NOT NULL REFERENCES problems(id),
    session_id UUID,
    image_s3_key VARCHAR(255),
    recognized_latex TEXT,
    stroke_metadata JSONB,
    device_info JSONB,
    status VARCHAR(20) DEFAULT 'received',
    submitted_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP WITH TIME ZONE,
    processing_time_ms INT
);

-- Indexes
CREATE INDEX idx_submissions_user_submitted ON submissions (user_id, submitted_at DESC);
CREATE INDEX idx_submissions_problem ON submissions (problem_id);
CREATE INDEX idx_submissions_status ON submissions (status);
CREATE INDEX idx_submissions_session ON submissions (session_id);

-- Comments
COMMENT ON TABLE submissions IS '학습자 풀이 제출 이력';
COMMENT ON COLUMN submissions.session_id IS '클라이언트 세션 ID (여러 제출을 그룹화)';
COMMENT ON COLUMN submissions.image_s3_key IS 'S3에 저장된 캔버스 이미지 키';
COMMENT ON COLUMN submissions.recognized_latex IS 'iink/MathPix 인식 결과 LaTeX';
COMMENT ON COLUMN submissions.stroke_metadata IS '스트로크 메타데이터 (개수, 작성 시간 등)';
COMMENT ON COLUMN submissions.device_info IS '디바이스 정보 (플랫폼, OS 버전 등)';
COMMENT ON COLUMN submissions.status IS '상태: received, processing, completed, failed';
```

**stroke_metadata JSONB 구조 예시**:

```json
{
  "stroke_count": 42,
  "total_duration_ms": 35000,
  "canvas_size": {
    "width": 1080,
    "height": 1440
  },
  "input_type": "stylus",
  "avg_pressure": 0.67
}
```

**device_info JSONB 구조 예시**:

```json
{
  "platform": "ios",
  "os_version": "17.4",
  "app_version": "1.0.0",
  "device_model": "iPad Pro (11-inch)",
  "screen_size": {
    "width": 834,
    "height": 1194
  }
}
```

---

### 4.4 recognition_results (인식 결과)

**목적**: AI 분석 결과 저장

**DDL**:

```sql
CREATE TABLE recognition_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    submission_id UUID UNIQUE NOT NULL REFERENCES submissions(id) ON DELETE CASCADE,
    is_correct BOOLEAN NOT NULL,
    error_steps JSONB,
    concept_understanding_summary TEXT,
    feedback_text TEXT,
    correct_solution_latex TEXT,
    concept_tags_inferred TEXT[],
    llm_model_version VARCHAR(50),
    prompt_template_id UUID,
    confidence FLOAT CHECK (confidence BETWEEN 0 AND 1),
    processing_time_ms INT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_results_submission ON recognition_results (submission_id);
CREATE INDEX idx_results_correct ON recognition_results (is_correct);
CREATE INDEX idx_results_confidence ON recognition_results (confidence);

-- Comments
COMMENT ON TABLE recognition_results IS 'AI 분석 및 인식 결과';
COMMENT ON COLUMN recognition_results.error_steps IS '오류 단계 상세 정보 (JSONB 배열)';
COMMENT ON COLUMN recognition_results.concept_understanding_summary IS '개념 이해도 요약';
COMMENT ON COLUMN recognition_results.feedback_text IS '학습자에게 제공할 피드백 메시지';
COMMENT ON COLUMN recognition_results.llm_model_version IS '사용된 LLM 모델 (예: gpt-4o, claude-3.5-sonnet)';
COMMENT ON COLUMN recognition_results.confidence IS 'AI 분석 신뢰도 (0.0 ~ 1.0)';
```

**error_steps JSONB 구조 예시**:

```json
[
  {
    "step_order": 2,
    "error_type": "procedural",
    "error_subtype": "sign_error",
    "description": "이항 시 부호가 바뀌지 않았습니다.",
    "student_expression": "2x = 7 + 3",
    "correct_expression": "2x = 7 - 3",
    "confidence": 0.94
  }
]
```

---

### 4.5 concept_mastery (개념 습득)

**목적**: 학습자의 개념별 습득 현황 추적

**DDL**:

```sql
CREATE TABLE concept_mastery (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    concept_id VARCHAR(100) NOT NULL,
    mastery_score FLOAT DEFAULT 0.5 CHECK (mastery_score BETWEEN 0 AND 1),
    consecutive_correct INT DEFAULT 0,
    total_attempts INT DEFAULT 0,
    correct_attempts INT DEFAULT 0,
    status VARCHAR(20) DEFAULT 'learning',
    next_review_at TIMESTAMP WITH TIME ZONE,
    last_practiced_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_id, concept_id)
);

-- Indexes
CREATE INDEX idx_mastery_user_concept ON concept_mastery (user_id, concept_id);
CREATE INDEX idx_mastery_user_status ON concept_mastery (user_id, status, next_review_at);
CREATE INDEX idx_mastery_score ON concept_mastery (mastery_score);

-- Comments
COMMENT ON TABLE concept_mastery IS '학습자별 개념 습득 현황';
COMMENT ON COLUMN concept_mastery.concept_id IS '개념 ID (예: concept_linear_equation)';
COMMENT ON COLUMN concept_mastery.mastery_score IS '습득 점수 (0.0 ~ 1.0, EWMA 알고리즘)';
COMMENT ON COLUMN concept_mastery.consecutive_correct IS '연속 정답 횟수';
COMMENT ON COLUMN concept_mastery.status IS '상태: learning, mastered, review_due, forgotten';
COMMENT ON COLUMN concept_mastery.next_review_at IS '다음 복습 예정 일시 (간격 반복)';
```

---

### 4.6 user_problem_history (문제 풀이 이력)

**목적**: 학습자의 문제별 풀이 이력 간단 기록

**DDL**:

```sql
CREATE TABLE user_problem_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    problem_id UUID NOT NULL REFERENCES problems(id),
    submission_id UUID REFERENCES submissions(id),
    is_correct BOOLEAN NOT NULL,
    error_type VARCHAR(50),
    time_spent_seconds INT,
    solved_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_history_user_problem ON user_problem_history (user_id, problem_id);
CREATE INDEX idx_history_user_date ON user_problem_history (user_id, solved_at DESC);
CREATE INDEX idx_history_correct ON user_problem_history (is_correct);
CREATE INDEX idx_history_error_type ON user_problem_history (error_type);

-- Comments
COMMENT ON TABLE user_problem_history IS '학습자별 문제 풀이 이력 (요약)';
COMMENT ON COLUMN user_problem_history.error_type IS '오류 유형: conceptual, procedural, computational, comprehension';
COMMENT ON COLUMN user_problem_history.time_spent_seconds IS '문제 풀이에 소요된 시간 (초)';
```

---

## 5. 인덱스 전략 (Indexing Strategy)

### 5.1 인덱스 목록

| 테이블 | 인덱스명 | 컬럼 | 타입 | 목적 |
|--------|---------|------|------|------|
| users | idx_users_email | email | B-tree UNIQUE | 로그인 쿼리 최적화 |
| users | idx_users_grade | grade | B-tree | 학년별 집계 |
| users | idx_users_last_active | last_active_at DESC | B-tree | 활성 사용자 조회 |
| problems | idx_problems_grade_difficulty | (grade, difficulty, status) | Composite B-tree | 추천 문제 필터 |
| problems | idx_problems_concept_tags | concept_tags | GIN | 태그 기반 검색 |
| problems | idx_problems_status | status | B-tree | 상태별 필터 |
| submissions | idx_submissions_user_submitted | (user_id, submitted_at DESC) | Composite B-tree | 사용자별 이력 조회 |
| submissions | idx_submissions_status | status | B-tree | 처리 대기 큐 조회 |
| submissions | idx_submissions_session | session_id | B-tree | 세션별 그룹화 |
| recognition_results | idx_results_submission | submission_id | B-tree UNIQUE | 조인 최적화 |
| recognition_results | idx_results_correct | is_correct | B-tree | 정답률 집계 |
| concept_mastery | idx_mastery_user_concept | (user_id, concept_id) | Composite B-tree UNIQUE | 개념 습득 조회 |
| concept_mastery | idx_mastery_user_status | (user_id, status, next_review_at) | Composite B-tree | 복습 스케줄 조회 |
| user_problem_history | idx_history_user_problem | (user_id, problem_id) | Composite B-tree | 중복 문제 방지 |
| user_problem_history | idx_history_user_date | (user_id, solved_at DESC) | Composite B-tree | 최근 이력 조회 |

### 5.2 인덱스 설계 원칙

1. **WHERE 절 컬럼 우선**: 자주 필터링되는 컬럼에 인덱스 생성
2. **복합 인덱스 순서**: 선택도가 높은 컬럼을 앞쪽에 배치
3. **JSONB GIN 인덱스**: JSONB 컬럼 내 키 검색이 필요한 경우
4. **Array GIN 인덱스**: TEXT[] 배열의 요소 검색
5. **Partial Index**: 특정 조건에만 인덱스 (예: `WHERE status = 'active'`)
6. **Covering Index**: SELECT 컬럼까지 포함하여 인덱스 온리 스캔

### 5.3 인덱스 성능 모니터링

```sql
-- 사용되지 않는 인덱스 찾기
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
WHERE idx_scan = 0
ORDER BY pg_relation_size(indexrelid) DESC;

-- 테이블별 인덱스 크기
SELECT
    tablename,
    indexname,
    pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
FROM pg_stat_user_indexes
ORDER BY pg_relation_size(indexrelid) DESC;
```

---

## 6. 관계 및 제약조건 (Relationships & Constraints)

### 6.1 외래 키 관계

```sql
-- submissions → users
ALTER TABLE submissions
    ADD CONSTRAINT fk_submissions_user
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

-- submissions → problems
ALTER TABLE submissions
    ADD CONSTRAINT fk_submissions_problem
    FOREIGN KEY (problem_id) REFERENCES problems(id) ON DELETE RESTRICT;

-- recognition_results → submissions
ALTER TABLE recognition_results
    ADD CONSTRAINT fk_results_submission
    FOREIGN KEY (submission_id) REFERENCES submissions(id) ON DELETE CASCADE;

-- concept_mastery → users
ALTER TABLE concept_mastery
    ADD CONSTRAINT fk_mastery_user
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

-- user_problem_history → users
ALTER TABLE user_problem_history
    ADD CONSTRAINT fk_history_user
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

-- user_problem_history → problems
ALTER TABLE user_problem_history
    ADD CONSTRAINT fk_history_problem
    FOREIGN KEY (problem_id) REFERENCES problems(id) ON DELETE CASCADE;

-- user_problem_history → submissions
ALTER TABLE user_problem_history
    ADD CONSTRAINT fk_history_submission
    FOREIGN KEY (submission_id) REFERENCES submissions(id) ON DELETE SET NULL;

-- problems → problems (self-reference)
ALTER TABLE problems
    ADD CONSTRAINT fk_problems_parent
    FOREIGN KEY (parent_problem_id) REFERENCES problems(id) ON DELETE SET NULL;
```

### 6.2 제약조건 설명

| 외래 키 | ON DELETE 동작 | 이유 |
|---------|---------------|------|
| submissions.user_id → users.id | CASCADE | 사용자 삭제 시 제출 이력도 함께 삭제 |
| submissions.problem_id → problems.id | RESTRICT | 문제는 제출 이력이 있으면 삭제 불가 (archived 상태로 변경) |
| recognition_results.submission_id → submissions.id | CASCADE | 제출 삭제 시 분석 결과도 함께 삭제 |
| concept_mastery.user_id → users.id | CASCADE | 사용자 삭제 시 습득 현황도 함께 삭제 |
| user_problem_history.user_id → users.id | CASCADE | 사용자 삭제 시 이력도 함께 삭제 |
| user_problem_history.submission_id → submissions.id | SET NULL | 제출 삭제 시 이력 레코드는 유지 (submission_id만 NULL) |
| problems.parent_problem_id → problems.id | SET NULL | 원본 문제 삭제 시 생성된 문제는 유지 |

### 6.3 체크 제약조건

```sql
-- users.current_difficulty: 1~5 범위
ALTER TABLE users
    ADD CONSTRAINT check_user_difficulty
    CHECK (current_difficulty BETWEEN 1 AND 5);

-- problems.difficulty: 1~5 범위
ALTER TABLE problems
    ADD CONSTRAINT check_problem_difficulty
    CHECK (difficulty BETWEEN 1 AND 5);

-- concept_mastery.mastery_score: 0~1 범위
ALTER TABLE concept_mastery
    ADD CONSTRAINT check_mastery_score
    CHECK (mastery_score BETWEEN 0 AND 1);

-- recognition_results.confidence: 0~1 범위
ALTER TABLE recognition_results
    ADD CONSTRAINT check_result_confidence
    CHECK (confidence BETWEEN 0 AND 1);
```

---

## 7. 데이터 타입 및 도메인 (Data Types & Domains)

### 7.1 공통 도메인 정의

```sql
-- 학년 열거형
CREATE TYPE grade_enum AS ENUM (
    'middle_1', 'middle_2', 'middle_3',
    'high_1', 'high_2', 'high_3',
    'reexaminee', 'adult'
);

-- 과목 열거형
CREATE TYPE subject_enum AS ENUM (
    'algebra',
    'geometry',
    'calculus',
    'statistics',
    'probability'
);

-- 제출 상태 열거형
CREATE TYPE submission_status_enum AS ENUM (
    'received',
    'processing',
    'completed',
    'failed'
);

-- 문제 상태 열거형
CREATE TYPE problem_status_enum AS ENUM (
    'draft',
    'review',
    'active',
    'archived'
);

-- 개념 습득 상태 열거형
CREATE TYPE mastery_status_enum AS ENUM (
    'learning',
    'mastered',
    'review_due',
    'forgotten'
);

-- 오류 유형 열거형
CREATE TYPE error_type_enum AS ENUM (
    'conceptual',
    'procedural',
    'computational',
    'comprehension'
);
```

**참고**: Phase 1에서는 VARCHAR로 저장하고, Phase 2에서 ENUM 타입으로 마이그레이션 권장.

### 7.2 JSONB 데이터 구조 표준

#### error_steps JSONB 스키마

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "array",
  "items": {
    "type": "object",
    "required": ["step_order", "error_type", "description"],
    "properties": {
      "step_order": {
        "type": "integer",
        "minimum": 1
      },
      "error_type": {
        "type": "string",
        "enum": ["conceptual", "procedural", "computational", "comprehension"]
      },
      "error_subtype": {
        "type": "string"
      },
      "description": {
        "type": "string",
        "maxLength": 1000
      },
      "student_expression": {
        "type": "string"
      },
      "correct_expression": {
        "type": "string"
      },
      "confidence": {
        "type": "number",
        "minimum": 0,
        "maximum": 1
      }
    }
  }
}
```

---

## 8. 성능 최적화 (Performance Optimization)

### 8.1 쿼리 최적화 전략

#### 8.1.1 문제 추천 쿼리 최적화

**요구사항**: 사용자의 학년/난이도/취약 개념을 기반으로 문제 추천 (P99 < 1초)

**Before (비최적화)**:

```sql
-- N+1 쿼리 문제
SELECT * FROM problems WHERE grade = 'middle_2' AND difficulty = 3;
-- 별도 쿼리로 개념 필터링
SELECT * FROM problems WHERE 'linear_equation' = ANY(concept_tags);
```

**After (최적화)**:

```sql
-- 단일 쿼리 + 인덱스 활용
SELECT p.id, p.title, p.content_text, p.answer_latex, p.difficulty
FROM problems p
WHERE p.grade = 'middle_2'
  AND p.difficulty = 3
  AND p.status = 'active'
  AND p.concept_tags && ARRAY['linear_equation', 'fraction']  -- Array overlap operator
  AND p.id NOT IN (
      -- 최근 7일 풀이한 문제 제외 (서브쿼리 최적화)
      SELECT problem_id
      FROM user_problem_history
      WHERE user_id = '...'
        AND solved_at > CURRENT_TIMESTAMP - INTERVAL '7 days'
  )
ORDER BY RANDOM()
LIMIT 1;

-- 또는 Lateral Join 사용
SELECT p.id, p.title, p.content_text
FROM problems p
WHERE p.grade = 'middle_2'
  AND p.difficulty = 3
  AND p.status = 'active'
  AND NOT EXISTS (
      SELECT 1
      FROM user_problem_history h
      WHERE h.problem_id = p.id
        AND h.user_id = '...'
        AND h.solved_at > CURRENT_TIMESTAMP - INTERVAL '7 days'
  )
ORDER BY RANDOM()
LIMIT 1;
```

**성능 개선**:
- Before: 500-800ms
- After: 80-150ms (복합 인덱스 + EXISTS 사용)

#### 8.1.2 사용자 대시보드 쿼리 최적화

**요구사항**: 사용자의 최근 7일 통계 (제출 수, 정답률, 취약 개념 TOP 3)

```sql
-- 단일 CTE 쿼리로 모든 통계 계산
WITH recent_stats AS (
    SELECT
        COUNT(*) AS total_submissions,
        COUNT(*) FILTER (WHERE rr.is_correct) AS correct_count,
        ROUND(COUNT(*) FILTER (WHERE rr.is_correct)::NUMERIC / COUNT(*) * 100, 1) AS accuracy_rate,
        jsonb_agg(
            DISTINCT jsonb_build_object(
                'concept', unnest(rr.concept_tags_inferred),
                'error_count', COUNT(*) FILTER (WHERE NOT rr.is_correct)
            )
        ) AS weak_concepts
    FROM submissions s
    JOIN recognition_results rr ON rr.submission_id = s.id
    WHERE s.user_id = $1
      AND s.submitted_at > CURRENT_TIMESTAMP - INTERVAL '7 days'
)
SELECT * FROM recent_stats;
```

### 8.2 연결 풀링 (Connection Pooling)

```python
# backend/app/db.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# 연결 풀 설정
engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,           # 최소 연결 수
    max_overflow=10,        # 추가 연결 가능 수
    pool_pre_ping=True,     # 연결 유효성 자동 검사
    pool_recycle=3600,      # 1시간마다 연결 재생성 (MySQL 8시간 타임아웃 방지)
    echo=False              # SQL 로그 출력 (개발 시 True)
)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
```

### 8.3 읽기 복제본 사용

```python
# 읽기 전용 쿼리는 Replica로 라우팅
from sqlalchemy import select

# 쓰기 (Primary)
async with async_session() as session:
    user = User(email="test@example.com", name="Test")
    session.add(user)
    await session.commit()

# 읽기 (Replica)
async with async_session(bind=replica_engine) as session:
    stmt = select(Problem).where(Problem.status == "active")
    result = await session.execute(stmt)
    problems = result.scalars().all()
```

---

## 9. 백업 및 복구 전략 (Backup & Recovery)

### 9.1 백업 정책

| 백업 유형 | 주기 | 보관 기간 | 방법 |
|----------|------|----------|------|
| Full Backup | 매일 02:00 (KST) | 7일 | `pg_basebackup` 또는 AWS RDS 자동 스냅샷 |
| Incremental Backup | 6시간마다 | 24시간 | WAL (Write-Ahead Log) 아카이빙 |
| Point-in-Time Recovery | 연속 | 7일 | WAL 아카이빙 + WAL 재생 |

### 9.2 백업 스크립트 (예시)

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/var/backups/postgresql"
DB_NAME="mathlens_production"

# Full backup
pg_basebackup -h localhost -U postgres -D "$BACKUP_DIR/full_$DATE" -Ft -z -Xs -P

# WAL archiving (continuous)
# postgresql.conf:
# wal_level = replica
# archive_mode = on
# archive_command = 'cp %p /var/backups/postgresql/wal/%f'

# 7일 이상 오래된 백업 삭제
find "$BACKUP_DIR" -type d -mtime +7 -exec rm -rf {} \;

echo "Backup completed: $BACKUP_DIR/full_$DATE"
```

### 9.3 복구 절차

#### 전체 복구 (Full Recovery)

```bash
# 1. PostgreSQL 중지
sudo systemctl stop postgresql

# 2. 기존 데이터 디렉토리 백업
mv /var/lib/postgresql/15/main /var/lib/postgresql/15/main.old

# 3. 백업 복원
tar -xzf /var/backups/postgresql/full_20260522_020000/base.tar.gz -C /var/lib/postgresql/15/main

# 4. 소유권 설정
chown -R postgres:postgres /var/lib/postgresql/15/main

# 5. PostgreSQL 시작
sudo systemctl start postgresql
```

#### Point-in-Time Recovery (PITR)

```bash
# recovery.conf 파일 생성
cat > /var/lib/postgresql/15/main/recovery.conf <<EOF
restore_command = 'cp /var/backups/postgresql/wal/%f %p'
recovery_target_time = '2026-05-22 15:30:00 KST'
EOF

# PostgreSQL 재시작 (recovery 모드로 시작)
sudo systemctl restart postgresql
```

---

## 10. 마이그레이션 전략 (Migration Strategy)

### 10.1 Alembic 설정

```bash
# Alembic 초기화
cd backend
alembic init alembic

# 마이그레이션 생성
alembic revision --autogenerate -m "Initial schema"

# 마이그레이션 적용
alembic upgrade head

# 롤백
alembic downgrade -1
```

### 10.2 마이그레이션 파일 예시

```python
# alembic/versions/001_initial_schema.py

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    # users 테이블 생성
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(), nullable=False, server_default=sa.text('gen_random_uuid()')),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('hashed_password', sa.String(255), nullable=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('grade', sa.String(20), nullable=False),
        sa.Column('current_difficulty', sa.Integer(), server_default='3', nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )

    # 인덱스 생성
    op.create_index('idx_users_email', 'users', ['email'])

def downgrade():
    op.drop_index('idx_users_email', table_name='users')
    op.drop_table('users')
```

### 10.3 Zero-Downtime 마이그레이션

**원칙**:
1. 기존 컬럼 삭제 금지 (deprecated 표시 후 다음 릴리스에서 삭제)
2. 새 컬럼 추가 시 NULL 허용 또는 DEFAULT 값 설정
3. 인덱스 생성 시 `CONCURRENTLY` 옵션 사용

**예시**:

```sql
-- ❌ BAD: 즉시 컬럼 삭제 (애플리케이션 오류 발생 가능)
ALTER TABLE users DROP COLUMN old_field;

-- ✅ GOOD: 단계적 마이그레이션
-- Step 1: 애플리케이션 코드에서 old_field 사용 중지
-- Step 2: 다음 릴리스에서 컬럼 삭제
ALTER TABLE users DROP COLUMN old_field;

-- 인덱스 생성 (잠금 없음)
CREATE INDEX CONCURRENTLY idx_submissions_processed ON submissions (processed_at);
```

---

## 11. 보안 및 접근 제어 (Security & Access Control)

### 11.1 데이터베이스 사용자 역할

```sql
-- 읽기 전용 사용자 (분석/리포트용)
CREATE ROLE readonly_user LOGIN PASSWORD 'secure_password';
GRANT CONNECT ON DATABASE mathlens_production TO readonly_user;
GRANT USAGE ON SCHEMA public TO readonly_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO readonly_user;

-- 애플리케이션 사용자 (읽기/쓰기)
CREATE ROLE app_user LOGIN PASSWORD 'secure_password';
GRANT CONNECT ON DATABASE mathlens_production TO app_user;
GRANT USAGE ON SCHEMA public TO app_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO app_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO app_user;
```

### 11.2 행 수준 보안 (Row-Level Security)

```sql
-- 사용자는 자신의 데이터만 조회 가능
ALTER TABLE submissions ENABLE ROW LEVEL SECURITY;

CREATE POLICY submissions_user_policy ON submissions
    FOR SELECT
    USING (user_id = current_setting('app.current_user_id')::UUID);

-- 애플리케이션에서 설정
-- SET app.current_user_id = 'user_uuid';
```

### 11.3 민감 데이터 암호화

```sql
-- pgcrypto 확장 활성화
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- 비밀번호 해시 (bcrypt)
-- 애플리케이션 레벨에서 처리 (Python bcrypt 라이브러리)

-- 필요 시 컬럼 수준 암호화
-- CREATE TABLE sensitive_data (
--     id UUID PRIMARY KEY,
--     encrypted_field BYTEA  -- pgp_sym_encrypt() 사용
-- );
```

### 11.4 감사 로그 (Audit Logging)

```sql
-- pgaudit 확장 활성화
CREATE EXTENSION IF NOT EXISTS pgaudit;

-- postgresql.conf 설정
-- pgaudit.log = 'write'
-- pgaudit.log_catalog = off
-- pgaudit.log_parameter = on

-- 모든 DML 작업 로그 기록
ALTER SYSTEM SET pgaudit.log = 'write';
SELECT pg_reload_conf();
```

---

## 부록 A: 초기 데이터 (Seed Data)

### A.1 문제은행 샘플 데이터

```sql
-- 샘플 문제 삽입
INSERT INTO problems (title, content_text, answer_latex, subject, grade, difficulty, concept_tags, status)
VALUES
    (
        '일차방정식 풀이',
        '다음 방정식을 풀어라: $2x + 3 = 7$',
        'x = 2',
        'algebra',
        'middle_1',
        1,
        ARRAY['일차방정식', '이항'],
        'active'
    ),
    (
        '이차방정식 인수분해',
        '다음 이차방정식을 인수분해하여 풀어라: $x^2 + 5x + 6 = 0$',
        'x = -2 \text{ or } x = -3',
        'algebra',
        'middle_3',
        3,
        ARRAY['이차방정식', '인수분해'],
        'active'
    ),
    (
        '피타고라스 정리',
        '직각삼각형에서 빗변의 길이가 5cm, 한 변의 길이가 3cm일 때 나머지 한 변의 길이를 구하여라.',
        '4 \text{ cm}',
        'geometry',
        'middle_2',
        2,
        ARRAY['피타고라스정리', '직각삼각형'],
        'active'
    );
```

---

## 부록 B: 성능 모니터링 쿼리

```sql
-- 테이블별 크기 확인
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS total_size,
    pg_size_pretty(pg_relation_size(schemaname||'.'||tablename)) AS table_size,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename) - pg_relation_size(schemaname||'.'||tablename)) AS index_size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- 느린 쿼리 찾기 (pg_stat_statements 필요)
SELECT
    calls,
    total_exec_time,
    mean_exec_time,
    query
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 20;

-- 테이블별 통계
SELECT
    schemaname,
    tablename,
    n_live_tup AS row_count,
    n_dead_tup AS dead_rows,
    last_vacuum,
    last_autovacuum
FROM pg_stat_user_tables
ORDER BY n_live_tup DESC;
```

---

**Document Revision History:**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| v1.0 | 2026-05-22 | Engineering Team | Initial database design document |

---

*본 문서는 내부 개발용입니다.*

*© 2026 MathLens AI Project. All rights reserved.*
