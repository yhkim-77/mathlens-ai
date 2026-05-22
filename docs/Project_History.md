# 프로젝트 이력서 (Project History)

> **MathLens AI** - 수학 풀이 인식 기반 AI 튜터 모바일 애플리케이션
>
> 본 문서는 MathLens AI 프로젝트의 주요 개발 이력, 의사결정, 마일스톤을 시간순으로 기록합니다.

---

## 📋 목차

1. [프로젝트 개요](#프로젝트-개요)
2. [버전 이력](#버전-이력)
3. [주요 마일스톤](#주요-마일스톤)
4. [아키텍처 변경 이력](#아키텍처-변경-이력)
5. [문서화 이력](#문서화-이력)
6. [기술 스택 진화](#기술-스택-진화)
7. [향후 계획](#향후-계획)

---

## 프로젝트 개요

### 프로젝트 정보

| 항목 | 내용 |
|------|------|
| **프로젝트명** | MathLens AI |
| **목적** | 학생의 수학 풀이 과정을 AI로 분석하여 개인화된 피드백과 학습 가이드를 제공하는 모바일 애플리케이션 |
| **시작일** | 2026년 초 (추정) |
| **Repository** | https://github.com/yhkim-77/mathlens-ai |
| **주요 언어** | Python (Backend), TypeScript/JavaScript (Mobile) |

### 핵심 기능

1. **손글씨 수식 인식 (HTR)**: 학생이 작성한 수학 풀이를 LaTeX로 변환
2. **AI 기반 오답 분석**: GPT-4o를 활용한 단계별 풀이 분석 및 오류 유형 분류
3. **개인화 학습 추천**: 개념 습득도 추적 및 맞춤형 문제 추천
4. **학습 대시보드**: 개념별 성취도, 오답 노트, 학습 리포트

---

## 버전 이력

### v0.1.0-alpha (현재 개발 단계)

**개발 기간**: 2026년 1월 ~ 현재

**구현 완료**:
- ✅ Backend API 서버 (FastAPI)
  - 인증/인가 (JWT)
  - 문제 관리 CRUD API
  - 제출 및 분석 API (동기/비동기)
  - WebSocket 실시간 상태 업데이트
- ✅ Mobile 앱 기본 구조 (React Native 0.74)
  - Redux Toolkit 상태 관리
  - TypeScript 기반 타입 안전성
  - Android 빌드 환경
- ✅ CI/CD 파이프라인
  - GitHub Actions 기반 자동화
  - Backend 테스트 및 Docker 빌드
  - Android APK 빌드 및 배포

**진행 중**:
- 🚧 Mobile UI/UX 개발
  - 펜 캔버스 인터페이스
  - 손글씨 인식 통합
  - 분석 결과 시각화
- 🚧 HTR 엔진 통합
- 🚧 AI 분석 파이프라인 정교화

---

## 주요 마일스톤

### 2026년 5월

#### 2026-05-22: 통합 문서화 완료
- **문서 추가**:
  - `QA_Validation_Plan.md`: 8주차 단계별 테스트 계획, 품질 게이트
  - `Test_Cases.md`: 80+ 상세 테스트 케이스 (Backend/Mobile/Integration/Performance/Security)
  - `CI_CD_Documentation.md`: CI/CD 파이프라인 상세 가이드, 트러블슈팅
  - `API_Design_Document.md`: REST/WebSocket API 명세, 인증 흐름, 에러 처리
  - `Database_Design_Document.md`: PostgreSQL 스키마, ERD, 쿼리 최적화 전략
  - `Detailed_Design_Document.md`: 컴포넌트 설계, 알고리즘 명세, 보안 설계
  - `Functional_Design_Document.md`: 기능 명세, 사용자 워크플로우, 수락 기준
  - `SRS.md`: IEEE 830 표준 요구사항 명세서
- **PR**: #22, #21, #20, #19, #18
- **의의**: 프로젝트 기획부터 구현, 테스트까지 전 주기 문서화 완료

#### 2026-05-22: RFP/PRD 개선 및 오픈소스 옵션 추가
- **문서 개선**:
  - `RFP_통합본.md`: 오답 추론 시스템, 실시간 스트로크 처리, 도형 인식 (Phase 3+)
  - `PRD_통합본.md`: 오답 알고리즘 상세화, TTS 구현 예제, Phase 4 로드맵 (음성 튜터, 멀티모달 AI, AR)
  - 무료/오픈소스 모델 활용 방안 추가: Pix2tex, TrOCR, DeepSeek-Math 7B, Qwen2.5-Math, Llama 3.1
  - 예산/계약 관련 내용 제거 (기술 문서 중립성 확보)
- **PR**: #14, #13
- **의의**: 상용 API 의존도 완화, 비용 효율성 향상 방안 제시

#### 2026-05-22: 빌드 오류 수정 및 보안 강화
- **수정 사항**:
  - Android styles.xml 리소스 참조 오류 수정 (`rn_edit_text_material` drawable 제거)
  - SECRET_KEY 자동 생성 (`os.urandom(32).hex()`)
  - CORS 설정 제한 (wildcard `["*"]` → 특정 origin 화이트리스트)
  - `.env.example` 템플릿 추가
  - SQLite DB 파일 Git 추적 제외 (`.gitignore`)
  - CI workflow Gradle wrapper 중복 다운로드 제거
- **PR**: #17, #16, #15
- **의의**: 프로덕션 보안 강화, CI/CD 안정성 향상

### 2026년 1월 ~ 4월 (추정)

#### Phase 1: 프로젝트 기획
- RFP 및 PRD 초안 작성
- 기술 스택 선정 (FastAPI, React Native, PostgreSQL, GPT-4o)
- 아키텍처 설계

#### Phase 2: Backend 개발
- FastAPI 서버 구축
- JWT 인증/인가
- 문제 관리 API
- 제출 및 분석 API (동기/비동기)
- WebSocket 실시간 통신
- PostgreSQL 데이터베이스 스키마 구현

#### Phase 3: Mobile 개발
- React Native 프로젝트 초기화
- Redux Toolkit 상태 관리 구조
- TypeScript 타입 정의
- Android 빌드 환경 설정

#### Phase 4: CI/CD 구축
- GitHub Actions workflow 설정
- Backend 테스트 자동화
- Docker 이미지 빌드 및 GHCR 배포
- Android APK 빌드 자동화

---

## 아키텍처 변경 이력

### 2026-05-22: 보안 설정 강화
- **변경 전**: 하드코딩된 SECRET_KEY, CORS wildcard 허용
- **변경 후**: 환경변수 기반 자동 생성 (`os.urandom(32).hex()`), CORS origin 화이트리스트
- **사유**: 프로덕션 환경 보안 강화, OWASP 권고사항 준수

### 2026 초: 초기 아키텍처 확정
- **Backend**: FastAPI (Python 3.11+)
- **Mobile**: React Native 0.74 + Redux Toolkit + TypeScript
- **Database**: PostgreSQL 15+
- **AI**: GPT-4o (primary), Claude 3.5 (fallback)
- **HTR**: MathPix API (상용) / Pix2tex, TrOCR (오픈소스 옵션)
- **Storage**: AWS S3 (이미지)
- **Deployment**: Docker + GitHub Container Registry

**설계 근거**:
- FastAPI: 비동기 처리, 자동 문서화, 타입 안전성
- React Native: 크로스 플랫폼 (Android/iOS)
- PostgreSQL: JSONB 지원, 복잡한 쿼리 최적화
- GPT-4o: 수학 추론 능력, LaTeX 파싱 정확도

---

## 문서화 이력

### 2026-05-22
| 문서명 | 버전 | 상태 | 비고 |
|--------|------|------|------|
| `QA_Validation_Plan.md` | v1.0 | ✅ 완료 | 8주차 테스트 계획, 품질 게이트 |
| `Test_Cases.md` | v1.0 | ✅ 완료 | 80+ 테스트 케이스 |
| `CI_CD_Documentation.md` | v1.0 | ✅ 완료 | 파이프라인 가이드 |
| `API_Design_Document.md` | v1.0 | ✅ 완료 | REST/WebSocket API 명세 |
| `Database_Design_Document.md` | v1.0 | ✅ 완료 | PostgreSQL 스키마, ERD |
| `Detailed_Design_Document.md` | v1.0 | ✅ 완료 | 컴포넌트 설계, 알고리즘 |
| `Functional_Design_Document.md` | v1.0 | ✅ 완료 | 기능 명세, 워크플로우 |
| `SRS.md` | v1.0 | ✅ 완료 | IEEE 830 요구사항 명세 |
| `RFP_통합본.md` | v2.0 | ✅ 개정 | 오픈소스 옵션, 예산 내용 제거 |
| `PRD_통합본.md` | v2.0 | ✅ 개정 | AI 분석 기능 상세화 |
| `README.md` | v1.3 | ✅ 최신화 | 문서 링크 재구성 |

### 문서화 원칙
1. **IEEE/ISO 표준 준수**: SRS는 IEEE 830-1998 기반
2. **한국어 우선**: 국내 개발팀 협업 고려
3. **기술 중립성**: 예산/계약 내용 제외
4. **추적 가능성**: 요구사항 ID 체계 (FR-XXX-YY)
5. **버전 관리**: Git 기반 문서 이력 관리

---

## 기술 스택 진화

### Backend

| 기술 | 버전 | 도입 시기 | 용도 |
|------|------|-----------|------|
| Python | 3.11+ | 2026 초 | 백엔드 언어 |
| FastAPI | 0.109+ | 2026 초 | Web 프레임워크 |
| SQLAlchemy | 2.0+ | 2026 초 | ORM (비동기) |
| PostgreSQL | 15+ | 2026 초 | 관계형 데이터베이스 |
| Alembic | - | 2026 초 | 마이그레이션 도구 |
| Pydantic | 2.0+ | 2026 초 | 데이터 검증 |
| JWT | - | 2026 초 | 인증/인가 |
| WebSockets | - | 2026 초 | 실시간 통신 |
| Docker | - | 2026 초 | 컨테이너화 |

### Mobile

| 기술 | 버전 | 도입 시기 | 용도 |
|------|------|-----------|------|
| React Native | 0.74 | 2026 초 | 모바일 프레임워크 |
| TypeScript | 5.0+ | 2026 초 | 정적 타입 시스템 |
| Redux Toolkit | 2.0+ | 2026 초 | 상태 관리 |
| React Navigation | - | 2026 초 | 화면 라우팅 |
| Axios | - | 2026 초 | HTTP 클라이언트 |

### AI/ML

| 기술 | 버전 | 도입 시기 | 용도 |
|------|------|-----------|------|
| GPT-4o | - | 2026 초 | 수학 풀이 분석 (primary) |
| Claude 3.5 | - | 2026 초 | AI 백업 (fallback) |
| MathPix | - | 계획 | HTR 상용 API |
| Pix2tex | - | 계획 | HTR 오픈소스 대안 |
| TrOCR | - | 계획 | HTR 오픈소스 대안 |
| DeepSeek-Math 7B | - | 검토 중 | 로컬 수학 추론 모델 |
| Qwen2.5-Math 7B | - | 검토 중 | 로컬 수학 추론 모델 |

### DevOps

| 기술 | 버전 | 도입 시기 | 용도 |
|------|------|-----------|------|
| GitHub Actions | - | 2026 초 | CI/CD 자동화 |
| GitHub Container Registry | - | 2026 초 | Docker 이미지 저장소 |
| Docker Compose | - | 2026 초 | 로컬 개발 환경 |
| AWS S3 | - | 계획 | 이미지 스토리지 |

---

## 향후 계획

### Phase 2 (단기, 2026 Q2-Q3)
- [ ] Mobile 펜 캔버스 구현 (60 FPS, 10ms 입력 지연)
- [ ] HTR 엔진 통합 (MathPix 또는 Pix2tex)
- [ ] AI 분석 파이프라인 정교화 (오답 추론 알고리즘)
- [ ] 개념 습득도 추적 (EWMA 알고리즘)
- [ ] 학습 대시보드 (개념별 성취도, 오답 노트)
- [ ] iOS 빌드 환경 구축
- [ ] 베타 테스트 (100명)

### Phase 3 (중기, 2026 Q4 ~ 2027 Q1)
- [ ] 도형 인식 (기하학 문제 지원)
- [ ] 실시간 스트로크 처리 (200ms 부분 인식)
- [ ] 온디바이스 AI 추론 (오프라인 모드)
- [ ] 문제 은행 확장 (1만 문제)
- [ ] 간격 반복 학습 알고리즘
- [ ] 프로덕션 배포 (1,000 CCU)
- [ ] 성능 최적화 (P95 < 5s)

### Phase 4 (장기, 2027 Q2+)
- [ ] 음성 튜터 (STT + LLM + TTS 파이프라인)
- [ ] 멀티모달 AI (GPT-4o Omni / Gemini 1.5 Pro)
- [ ] AR 기반 학습 (선택)
- [ ] 협력 학습 (스터디 그룹)
- [ ] 교사 대시보드 (학급 관리)
- [ ] 글로벌 확장 (영어, 일본어)

---

## 기술 부채 및 개선 계획

### 현재 기술 부채

1. **Mobile UI 미완성**
   - 현황: 기본 구조만 구현
   - 계획: Phase 2에서 펜 캔버스, 분석 결과 시각화 완성

2. **HTR 엔진 미통합**
   - 현황: API 구조만 준비, 실제 인식 미구현
   - 계획: MathPix API 통합 또는 Pix2tex 오픈소스 적용

3. **테스트 커버리지 부족**
   - 현황: 단위 테스트 미작성
   - 계획: QA_Validation_Plan.md 기반 70% 커버리지 목표

4. **문서-코드 동기화**
   - 현황: 문서가 일부 구현보다 앞섬
   - 계획: 코드 구현 후 문서 검증 및 업데이트

### 개선 계획

| 항목 | 우선순위 | 목표 시기 | 담당 |
|------|----------|-----------|------|
| Mobile UI 완성 | High | 2026 Q2 | Mobile Team |
| HTR 통합 | High | 2026 Q2 | Backend Team |
| 단위 테스트 작성 | Medium | 2026 Q3 | 전체 |
| 성능 최적화 | Medium | 2026 Q3 | Backend Team |
| 문서 동기화 | Low | 2026 Q3 | 전체 |

---

## 의사결정 기록 (ADR)

### ADR-001: FastAPI vs Django
- **결정일**: 2026년 1월 (추정)
- **결정**: FastAPI 채택
- **근거**: 비동기 처리 우수, 자동 API 문서화, 타입 힌트 지원
- **대안**: Django REST Framework (동기 처리, 무거운 프레임워크)

### ADR-002: React Native vs Flutter
- **결정일**: 2026년 1월 (추정)
- **결정**: React Native 채택
- **근거**: JavaScript/TypeScript 생태계, 커뮤니티 규모, 개발 편의성
- **대안**: Flutter (Dart 학습 곡선, 네이티브 모듈 통합 제한)

### ADR-003: GPT-4o vs Claude 3.5
- **결정일**: 2026년 1월 (추정)
- **결정**: GPT-4o primary, Claude 3.5 fallback
- **근거**: GPT-4o의 수학 추론 능력 우수, LaTeX 파싱 정확도
- **대안**: 로컬 모델 (DeepSeek-Math, 비용 절감 가능하나 정확도 검증 필요)

### ADR-004: SECRET_KEY 관리
- **결정일**: 2026-05-22
- **결정**: 환경변수 기반 자동 생성 (`os.urandom(32).hex()`)
- **근거**: 하드코딩된 키 보안 취약, 프로덕션 환경 안전성
- **대안**: 수동 설정 (운영 실수 가능성)

### ADR-005: CORS 정책
- **결정일**: 2026-05-22
- **결정**: 특정 origin 화이트리스트 (localhost, Android emulator)
- **근거**: wildcard CORS는 보안 취약, OWASP 권고사항 준수
- **대안**: 프록시 서버 (복잡도 증가)

### ADR-006: 오픈소스 AI 모델 활용
- **결정일**: 2026-05-22
- **결정**: 상용 API + 오픈소스 하이브리드 전략
- **근거**: 비용 효율성, vendor lock-in 회피, 오프라인 지원
- **후보**: Pix2tex (HTR), DeepSeek-Math 7B, Qwen2.5-Math (LLM)

---

## 기여자

| 이름 | 역할 | 기여 |
|------|------|------|
| yhkim-77 | Project Lead | 프로젝트 총괄, 기획, 아키텍처 설계 |
| Claude (AI Agent) | Documentation Engineer | 통합 문서화, 코드 리뷰, 빌드 수정 |
| Copilot (AI Agent) | Technical Writer | RFP/PRD 개선, 오픈소스 옵션 연구 |

---

## 라이선스

본 프로젝트는 MIT 라이선스 하에 배포됩니다.

---

## 참고 문서

- [RFP (제안 요청서)](./RFP_통합본.md)
- [PRD (제품 요구사항 정의서)](./PRD_통합본.md)
- [SRS (소프트웨어 요구사항 명세서)](./SRS.md)
- [Functional Design Document (기능 설계서)](./Functional_Design_Document.md)
- [Detailed Design Document (상세 설계서)](./Detailed_Design_Document.md)
- [Database Design Document (데이터베이스 설계서)](./Database_Design_Document.md)
- [API Design Document (API 설계서)](./API_Design_Document.md)
- [QA Validation Plan (품질 검증 계획)](./QA_Validation_Plan.md)
- [Test Cases (테스트 케이스)](./Test_Cases.md)
- [CI/CD Documentation (CI/CD 문서화)](./CI_CD_Documentation.md)
- [README](../README.md)

---

**최종 업데이트**: 2026-05-22
**문서 버전**: v1.0
**작성자**: Claude (AI Documentation Agent)
