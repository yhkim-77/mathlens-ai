# MathLens AI 🧮

> 손글씨 수학 풀이 인식 기반 AI 개인 맞춤형 수학 튜터 — 백엔드 API

[![CI](https://github.com/yhkim-77/mathlens-ai/actions/workflows/ci.yml/badge.svg)](https://github.com/yhkim-77/mathlens-ai/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📱 소개

MathLens AI는 학습자가 스마트 기기 위에 펜 또는 손가락으로 수학 풀이 과정을 작성하면, AI가 이를 인식하고 분석하여 오답의 근본 원인을 찾아 맞춤형 피드백과 반복 학습을 제공하는 개인 수학 튜터입니다.

### 핵심 기능

- ✍️ **손글씨 풀이 제출** — Base64 이미지 + LaTeX 제출
- 🧠 **AI 풀이 분석** — GPT-4o 기반 오답 원인 분류 (개념/절차/계산/문제이해)
- 💡 **맞춤형 피드백** — 학년 수준에 맞춘 개념 재설명 생성
- 🔁 **반복 학습 시스템** — 에빙하우스 간격 반복, 개념 습득 추적
- 📊 **학습 리포트** — 취약 개념, 오답 유형 분포, 연속 학습일
- 🤖 **AI 유사 문제 생성** — GPT-4o로 동일 개념·다른 숫자 문제 자동 생성
- ⚡ **비동기 처리 + WebSocket** — 202 즉시 응답, 실시간 처리 상태 전달

---

## 🗂️ 프로젝트 구조

```
mathlens-ai/
├── backend/                  # AI 백엔드 서버 (FastAPI + SQLAlchemy)
│   ├── app/
│   │   ├── api/              # API 라우터
│   │   │   ├── auth.py       # 인증 (JWT, 회원가입/로그인)
│   │   │   ├── analyze.py    # 동기 풀이 분석
│   │   │   ├── submissions.py # 비동기 제출 + WebSocket
│   │   │   ├── problems.py   # 문제은행 + 추천 + AI 생성
│   │   │   ├── users.py      # 학습 리포트 + 오답노트
│   │   │   └── concepts.py   # 개념 목록 + 설명
│   │   ├── core/
│   │   │   ├── config.py     # 환경변수 설정
│   │   │   ├── database.py   # SQLAlchemy 비동기 DB
│   │   │   └── security.py   # JWT 유틸리티
│   │   ├── models/
│   │   │   └── models.py     # ORM 모델 (User, Problem, Submission, ...)
│   │   ├── services/
│   │   │   ├── analysis.py   # GPT-4o 분석 서비스
│   │   │   └── problems.py   # 문제 추천 + 개념 습득 서비스
│   │   └── main.py
│   ├── tests/                # pytest 테스트 (22개)
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env.example          # 환경변수 예제
│   └── pytest.ini
├── mobile/                   # React Native 모바일 앱
│   ├── android/              # Android 네이티브 코드
│   ├── src/
│   │   ├── navigation/       # React Navigation
│   │   ├── screens/          # 화면 컴포넌트
│   │   ├── services/         # API 클라이언트
│   │   ├── store/            # Redux 상태 관리
│   │   └── utils/            # 유틸리티
│   └── package.json
├── docker-compose.yml        # API + PostgreSQL
├── docs/
│   ├── RFP_통합본.md
│   ├── PRD_통합본.md
│   ├── SRS.md                      # 소프트웨어 요구사항 명세서
│   ├── Functional_Design_Document.md  # 기능 설계서
│   ├── Detailed_Design_Document.md    # 상세 설계서
│   ├── QA_Validation_Plan.md       # QA 검증 계획서
│   ├── Test_Cases.md               # 테스트 케이스 문서
│   └── CI_CD_Documentation.md      # CI/CD 문서
└── .github/workflows/
    ├── ci.yml                # 테스트 + Docker 빌드 (push/PR)
    └── release.yml           # 릴리즈 생성 + GHCR 이미지 푸시 (tag)
```

---

## 🚀 시작하기

### Docker Compose (권장)

```bash
git clone https://github.com/yhkim-77/mathlens-ai.git
cd mathlens-ai

# .env 파일 생성 (선택)
echo "OPENAI_API_KEY=sk-..." > .env
echo "SECRET_KEY=$(openssl rand -hex 32)" >> .env

docker compose up
```

API 서버: http://localhost:8000  
Swagger UI: http://localhost:8000/docs

### 로컬 개발

#### Backend

```bash
cd backend

# .env 파일 생성 (backend/.env.example 참고)
cp .env.example .env
# .env 파일에 SECRET_KEY와 OPENAI_API_KEY 설정

pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Mobile (Android)

```bash
cd mobile

# 의존성 설치
npm install --legacy-peer-deps

# Android 에뮬레이터 실행 (또는 실제 기기 연결)
npm run android
```

---

## 📡 API 엔드포인트

| Method | Path | 설명 |
|--------|------|------|
| POST | `/api/v1/auth/register` | 회원가입 |
| POST | `/api/v1/auth/token` | 로그인 (JWT 발급) |
| POST | `/api/v1/auth/refresh` | 토큰 갱신 |
| GET  | `/api/v1/auth/me` | 내 정보 |
| POST | `/api/v1/submissions` | 풀이 제출 (비동기, 202) |
| GET  | `/api/v1/submissions/{id}/status` | 처리 상태 폴링 |
| GET  | `/api/v1/results/{id}` | 분석 결과 조회 |
| WS   | `/ws/v1/submissions/{id}` | 실시간 상태 WebSocket |
| POST | `/api/v1/analyze` | 동기 풀이 분석 |
| POST | `/api/v1/analyze/image` | 이미지 파일 업로드 분석 |
| GET  | `/api/v1/problems` | 문제 목록 |
| POST | `/api/v1/problems` | 문제 등록 |
| GET  | `/api/v1/problems/recommend` | 개인화 문제 추천 |
| POST | `/api/v1/problems/generate` | AI 유사 문제 생성 |
| GET  | `/api/v1/problems/{id}` | 문제 상세 |
| GET  | `/api/v1/users/{id}/report` | 학습 리포트 |
| GET  | `/api/v1/users/{id}/mastery` | 개념 습득 현황 |
| GET  | `/api/v1/users/{id}/wrong-notes` | 오답 노트 |
| GET  | `/api/v1/concepts` | 개념 목록 |
| POST | `/api/v1/concepts` | 개념 등록 |
| GET  | `/api/v1/concepts/{id}` | 개념 상세 |
| GET  | `/api/v1/concepts/{id}/explanation` | AI 개념 설명 |

---

## 🛠️ 기술 스택

| 영역 | 기술 |
|------|------|
| Backend | Python 3.11, FastAPI, SQLAlchemy 2.0 (async) |
| Database | SQLite (개발), PostgreSQL (운영) |
| AI/ML | OpenAI GPT-4o, Anthropic Claude (백업) |
| 인증 | JWT (python-jose), bcrypt |
| Mobile | React Native 0.74, Redux Toolkit, TypeScript |
| 인프라 | Docker, Docker Compose, GitHub Actions, GHCR |

---

## ⚙️ 환경변수

백엔드 설정을 위해 `backend/.env` 파일을 생성하세요. `backend/.env.example` 파일을 참고하여 필요한 값을 설정하세요.

| 변수 | 기본값 | 설명 |
|------|--------|------|
| `DATABASE_URL` | `sqlite+aiosqlite:///./mathlens.db` | DB 연결 |
| `SECRET_KEY` | *(자동 생성, 프로덕션에서 고정값 필수)* | JWT 서명 키 |
| `OPENAI_API_KEY` | - | GPT-4o 사용 (미설정 시 mock 응답) |
| `ANTHROPIC_API_KEY` | - | Claude 백업 |
| `MATHPIX_APP_ID` / `MATHPIX_APP_KEY` | - | MathPix OCR |

**보안 주의사항:**
- 프로덕션 환경에서는 반드시 강력한 `SECRET_KEY`를 설정하세요: `openssl rand -hex 32`
- `.env` 파일은 Git에 커밋하지 마세요 (이미 .gitignore에 포함됨)

---

## 🧪 테스트

```bash
cd backend
pytest --tb=short -q
# 22 passed
```

---

## 🚢 릴리즈

Git 태그를 푸시하면 GitHub Actions가 자동으로:
1. 테스트 실행
2. Docker 이미지 빌드 → GHCR 푸시
3. GitHub Release 생성 (changelog 포함)

```bash
git tag v1.0.0
git push origin v1.0.0
```

---

## 📋 개발 로드맵

- [x] Phase 0: 백엔드 API 구현 (FastAPI + SQLAlchemy + GPT-4o)
- [x] Phase 0: CI/CD 파이프라인 + 릴리즈 자동화
- [x] Phase 1: Android 앱 (React Native + Redux Toolkit)
- [ ] Phase 1: iOS 앱 (React Native iOS 지원)
- [ ] Phase 2: 손글씨 인식 SDK 통합 (iink 또는 대체 솔루션)
- [ ] Phase 2: 학부모 대시보드, 문제은행 확충
- [ ] Phase 3: 온디바이스 AI, 실시간 협업

---

## 📄 문서

### 프로젝트 관리
- [Project History](docs/Project_History.md) — 프로젝트 이력서 (마일스톤, 버전 이력, ADR)

### 기획 및 요구사항
- [RFP 통합본](docs/RFP_통합본.md) — 제안요청서
- [PRD 통합본](docs/PRD_통합본.md) — 제품 요구사항 문서
- [SRS](docs/SRS.md) — 소프트웨어 요구사항 명세서

### 설계
- [Functional Design Document](docs/Functional_Design_Document.md) — 기능 설계서
- [Detailed Design Document](docs/Detailed_Design_Document.md) — 상세 설계서
- [Database Design Document](docs/Database_Design_Document.md) — 데이터베이스 설계서
- [API Design Document](docs/API_Design_Document.md) — API 설계서

### QA 및 테스트
- [QA Validation Plan](docs/QA_Validation_Plan.md) — QA 검증 계획서
- [Test Cases](docs/Test_Cases.md) — 테스트 케이스 문서

### DevOps
- [CI/CD Documentation](docs/CI_CD_Documentation.md) — CI/CD 파이프라인 문서

---

## 📜 라이선스

MIT License
