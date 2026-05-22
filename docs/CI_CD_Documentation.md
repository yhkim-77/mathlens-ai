# MathLens AI — CI/CD 문서

**문서 버전:** v1.0
**작성일:** 2026년 5월 22일
**문서 유형:** CI/CD Documentation
**작성자:** MathLens AI DevOps팀
**상태:** 초안 (Draft)

---

## 목차

1. [개요](#1-개요)
2. [CI 파이프라인](#2-ci-파이프라인)
3. [Release 파이프라인](#3-release-파이프라인)
4. [환경 구성](#4-환경-구성)
5. [배포 프로세스](#5-배포-프로세스)
6. [모니터링 및 롤백](#6-모니터링-및-롤백)
7. [트러블슈팅](#7-트러블슈팅)
8. [부록](#8-부록)

---

## 1. 개요

### 1.1 목적

본 문서는 MathLens AI 프로젝트의 CI/CD (Continuous Integration / Continuous Deployment) 파이프라인을 정의합니다. GitHub Actions를 사용하여 자동화된 테스트, 빌드, 배포 프로세스를 구축합니다.

### 1.2 CI/CD 아키텍처

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   개발자     │────▶│  Git Push    │────▶│   GitHub    │
│   (Local)   │     │  /PR 생성    │     │  Repository │
└─────────────┘     └──────────────┘     └──────┬──────┘
                                                 │
                                    ┌────────────▼────────────┐
                                    │   GitHub Actions        │
                                    │   (CI Workflow)         │
                                    │  ┌──────────────────┐   │
                                    │  │ 1. Backend Test  │   │
                                    │  │ 2. Docker Build  │   │
                                    │  │ 3. Android Build │   │
                                    │  └──────────────────┘   │
                                    └─────────────────────────┘
                                                 │
                                    ┌────────────▼────────────┐
                                    │   Tag Push (v*.*.*)     │
                                    └────────────┬────────────┘
                                                 │
                                    ┌────────────▼────────────┐
                                    │  Release Workflow       │
                                    │  ┌──────────────────┐   │
                                    │  │ 1. Run Tests     │   │
                                    │  │ 2. Build Docker  │   │
                                    │  │ 3. Push to GHCR  │   │
                                    │  │ 4. Build Android │   │
                                    │  │ 5. Create Release│   │
                                    │  └──────────────────┘   │
                                    └─────────────────────────┘
                                                 │
                            ┌────────────────────┴────────────────────┐
                            │                                          │
                   ┌────────▼─────────┐                    ┌──────────▼────────┐
                   │  GHCR (Docker)   │                    │  GitHub Release   │
                   │  ghcr.io/yhkim-77│                    │  + Android APK    │
                   │  /mathlens-ai    │                    └───────────────────┘
                   └──────────────────┘
```

### 1.3 도구 스택

| 도구 | 용도 | 버전 |
|------|------|------|
| **GitHub Actions** | CI/CD 파이프라인 | - |
| **Docker** | 컨테이너화, 이미지 빌드 | 24+ |
| **GHCR** | Docker 이미지 레지스트리 | - |
| **pytest** | Backend 테스트 | 7+ |
| **Gradle** | Android 빌드 | 8+ |
| **Node.js** | Mobile 의존성 관리 | 20+ |

---

## 2. CI 파이프라인

### 2.1 Workflow 파일 위치

`.github/workflows/ci.yml`

### 2.2 트리거 조건

**Push 이벤트:**
- `main` 브랜치
- `develop` 브랜치

**Pull Request 이벤트:**
- `main` 브랜치로의 PR

```yaml
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
```

### 2.3 CI Jobs

#### 2.3.1 Backend Test Job

**Job ID:** `backend-test`

**목적:** Backend API 단위/통합 테스트 실행

**단계:**
1. **Checkout 코드**
   ```yaml
   - uses: actions/checkout@v4
   ```

2. **Python 3.11 설치**
   ```yaml
   - name: Set up Python
     uses: actions/setup-python@v5
     with:
       python-version: '3.11'
   ```

3. **의존성 설치**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **테스트 실행**
   ```bash
   cd backend
   pytest --tb=short -q
   ```

**성공 조건:**
- 모든 pytest 테스트 PASS (22개)
- 종료 코드 0

**실행 환경:**
- Runner: `ubuntu-latest`
- 예상 실행 시간: 2-3분

---

#### 2.3.2 Backend Docker Build Job

**Job ID:** `backend-docker-build`

**목적:** Backend Docker 이미지 빌드 검증

**의존성:** `backend-test` (테스트 성공 후 실행)

**단계:**
1. **Checkout 코드**

2. **Docker Buildx 설정**
   ```yaml
   - name: Set up Docker Buildx
     uses: docker/setup-buildx-action@v3
   ```

3. **Docker 이미지 빌드**
   ```yaml
   - name: Build Docker image
     uses: docker/build-push-action@v5
     with:
       context: ./backend
       push: false
       tags: mathlens-ai-backend:ci
       cache-from: type=gha
       cache-to: type=gha,mode=max
   ```

**성공 조건:**
- Docker 이미지 빌드 성공
- 이미지 크기 < 1GB

**캐싱:**
- GitHub Actions Cache 사용 (`type=gha`)
- 빌드 시간 단축 (첫 빌드 5분 → 캐시 후 2분)

---

#### 2.3.3 Android Build Job

**Job ID:** `android-build`

**목적:** Android Debug APK 빌드

**단계:**
1. **Checkout 코드**

2. **Node.js 20 설치**
   ```yaml
   - name: Set up Node.js
     uses: actions/setup-node@v4
     with:
       node-version: '20'
   ```

3. **JS 의존성 설치**
   ```bash
   cd mobile
   npm install --legacy-peer-deps
   ```

4. **JDK 17 설치**
   ```yaml
   - name: Set up JDK 17
     uses: actions/setup-java@v4
     with:
       java-version: '17'
       distribution: 'temurin'
       cache: gradle
   ```

5. **Gradle 캐싱**
   ```yaml
   - name: Cache Gradle packages
     uses: actions/cache@v4
     with:
       path: |
         ~/.gradle/caches
         ~/.gradle/wrapper
       key: gradle-${{ runner.os }}-${{ hashFiles('mobile/android/**/*.gradle*') }}
   ```

6. **Gradlew 실행 권한 부여**
   ```bash
   cd mobile/android
   chmod +x gradlew
   ```

7. **local.properties 생성**
   ```bash
   echo "sdk.dir=$ANDROID_HOME" > local.properties
   ```

8. **Debug APK 빌드**
   ```bash
   ./gradlew assembleDebug --no-daemon
   ```
   - `--no-daemon`: CI 환경 최적화
   - `JAVA_OPTS: '-Xmx4g'`: 메모리 할당

9. **APK 아티팩트 업로드**
   ```yaml
   - name: Upload debug APK
     uses: actions/upload-artifact@v4
     with:
       name: app-debug
       path: mobile/android/app/build/outputs/apk/debug/app-debug.apk
       retention-days: 7
   ```

**성공 조건:**
- APK 파일 생성 (`app-debug.apk`)
- 빌드 에러 0건

**예상 실행 시간:** 8-12분

---

### 2.4 CI 성공 기준

**전체 CI 성공 조건:**
- ✅ `backend-test` PASS
- ✅ `backend-docker-build` PASS
- ✅ `android-build` PASS

**실패 시 동작:**
- PR 머지 차단 (GitHub Branch Protection)
- 실패 알림 (GitHub Notifications)
- 개발자가 수정 후 재푸시

---

## 3. Release 파이프라인

### 3.1 Workflow 파일 위치

`.github/workflows/release.yml`

### 3.2 트리거 조건

**Tag Push 이벤트:**
- 패턴: `v*.*.*` (예: `v1.0.0`, `v2.1.3`)

```yaml
on:
  push:
    tags:
      - 'v*.*.*'
```

### 3.3 Release Jobs

#### 3.3.1 Test Job

**Job ID:** `test`

**목적:** 릴리즈 전 테스트 재실행

**단계:**
- CI의 `backend-test`와 동일
- Python 3.11, pytest 실행

**중요성:** 릴리즈 품질 보증

---

#### 3.3.2 Build & Push Docker Image Job

**Job ID:** `build-and-push`

**목적:** Backend Docker 이미지 빌드 및 GHCR 푸시

**의존성:** `test` (테스트 성공 후 실행)

**단계:**
1. **Checkout 코드**

2. **Docker Buildx 설정**

3. **GHCR 로그인**
   ```yaml
   - name: Log in to GitHub Container Registry
     uses: docker/login-action@v3
     with:
       registry: ghcr.io
       username: ${{ github.actor }}
       password: ${{ secrets.GITHUB_TOKEN }}
   ```

4. **메타데이터 추출**
   ```yaml
   - name: Extract metadata
     id: meta
     uses: docker/metadata-action@v5
     with:
       images: ghcr.io/${{ github.repository }}/backend
       tags: |
         type=semver,pattern={{version}}
         type=semver,pattern={{major}}.{{minor}}
         type=sha,prefix=sha-
   ```
   **생성되는 태그 예시 (v1.2.3):**
   - `ghcr.io/yhkim-77/mathlens-ai/backend:1.2.3`
   - `ghcr.io/yhkim-77/mathlens-ai/backend:1.2`
   - `ghcr.io/yhkim-77/mathlens-ai/backend:sha-abc1234`

5. **이미지 빌드 & 푸시**
   ```yaml
   - name: Build and push
     uses: docker/build-push-action@v5
     with:
       context: ./backend
       push: true
       tags: ${{ steps.meta.outputs.tags }}
       labels: ${{ steps.meta.outputs.labels }}
       cache-from: type=gha
       cache-to: type=gha,mode=max
   ```

**출력:**
- `image_digest`: SHA256 이미지 다이제스트

---

#### 3.3.3 Build Android Release APK Job

**Job ID:** `build-android-release`

**목적:** Android Release APK 빌드

**의존성:** `test` (테스트 성공 후 실행)

**단계:**
- CI의 `android-build`와 유사
- **차이점:** `./gradlew assembleRelease` (Release APK)

**출력:**
- `app-release.apk` (서명 안 된 APK)
- 아티팩트 업로드: `name: app-release`

**참고:** 프로덕션 배포 시 서명 필요 (추후 개선)

---

#### 3.3.4 Create GitHub Release Job

**Job ID:** `release`

**목적:** GitHub Release 생성 및 아티팩트 첨부

**의존성:** `build-and-push`, `build-android-release` (두 Job 완료 후 실행)

**단계:**
1. **Checkout 코드 (전체 히스토리)**
   ```yaml
   - uses: actions/checkout@v4
     with:
       fetch-depth: 0
   ```

2. **Android APK 다운로드**
   ```yaml
   - name: Download Android APK
     uses: actions/download-artifact@v4
     with:
       name: app-release
       path: artifacts/
   ```

3. **Changelog 생성**
   ```bash
   TAG=${GITHUB_REF#refs/tags/}
   PREV_TAG=$(git tag --sort=-version:refname | grep -v "^${TAG}$" | head -1)
   if [ -z "$PREV_TAG" ]; then
     COMMITS=$(git log --oneline --pretty=format:"- %s (%h)")
   else
     COMMITS=$(git log --oneline --pretty=format:"- %s (%h)" "${PREV_TAG}..HEAD")
   fi
   ```
   - 이전 태그와 현재 태그 사이의 커밋 로그 추출
   - 포맷: `- 커밋 메시지 (해시)`

4. **GitHub Release 생성**
   ```yaml
   - name: Create Release
     uses: softprops/action-gh-release@v2
     with:
       tag_name: ${{ steps.changelog.outputs.TAG }}
       name: MathLens AI ${{ steps.changelog.outputs.TAG }}
       files: artifacts/app-release.apk
       body: |
         ## MathLens AI ${{ steps.changelog.outputs.TAG }}

         ### 📱 Android APK
         Download **app-release.apk** from the release assets below.

         ### 🐳 Docker Image (Backend)
         ```
         ghcr.io/${{ github.repository }}/backend:${{ steps.changelog.outputs.TAG }}
         ```

         ### 📋 Changes
         ${{ steps.changelog.outputs.CHANGELOG }}
       draft: false
       prerelease: ${{ contains(steps.changelog.outputs.TAG, '-') }}
   ```
   - `prerelease`: 태그에 `-`가 포함되면 프리릴리즈 (예: `v1.0.0-beta`)
   - `files`: APK 파일 첨부

**결과:**
- GitHub Release 페이지 자동 생성
- Android APK 다운로드 가능
- Docker 이미지 사용 가이드 포함

---

### 3.4 Release 프로세스

**릴리즈 생성 단계:**

1. **로컬에서 태그 생성**
   ```bash
   git tag v1.0.0
   ```

2. **태그 푸시**
   ```bash
   git push origin v1.0.0
   ```

3. **GitHub Actions 자동 실행**
   - `test` → `build-and-push` + `build-android-release` → `release`
   - 예상 실행 시간: 15-20분

4. **Release 페이지 확인**
   - https://github.com/yhkim-77/mathlens-ai/releases
   - Android APK 다운로드
   - Docker 이미지 GHCR에서 pull 가능

---

## 4. 환경 구성

### 4.1 GitHub Secrets

**현재 사용 중인 Secrets:**

| Secret 이름 | 설명 | 사용 위치 |
|------------|------|----------|
| `GITHUB_TOKEN` | GitHub Actions 자동 생성 토큰 | GHCR 로그인, Release 생성 |

**추가 권장 Secrets (프로덕션):**

| Secret 이름 | 설명 | 사용 목적 |
|------------|------|----------|
| `OPENAI_API_KEY` | OpenAI GPT-4o API 키 | Backend 테스트, E2E 테스트 |
| `ANDROID_KEYSTORE` | Android 앱 서명 키스토어 (Base64) | Release APK 서명 |
| `ANDROID_KEYSTORE_PASSWORD` | 키스토어 비밀번호 | Release APK 서명 |
| `SLACK_WEBHOOK_URL` | Slack 알림 웹훅 | 배포 알림 |

**Secrets 설정 방법:**
1. GitHub 저장소 → Settings → Secrets and variables → Actions
2. "New repository secret" 클릭
3. Name/Value 입력 후 저장

---

### 4.2 GitHub Actions 권한

**필요한 권한 (Workflow 파일에 설정):**

**ci.yml:**
```yaml
permissions:
  contents: read
```
- `contents:read`: 코드 체크아웃

**release.yml:**
```yaml
permissions:
  contents: write
  packages: write
```
- `contents:write`: Release 생성, 태그 푸시
- `packages:write`: GHCR에 이미지 푸시

---

### 4.3 Branch Protection Rules

**추천 설정 (main 브랜치):**

1. **Require pull request reviews before merging**
   - 리뷰어 1명 이상 승인 필요

2. **Require status checks to pass before merging**
   - `backend-test` ✅
   - `backend-docker-build` ✅
   - `android-build` ✅

3. **Require branches to be up to date before merging**
   - PR이 최신 main 브랜치 기반이어야 함

4. **Do not allow bypassing the above settings**
   - 관리자도 보호 규칙 준수

**설정 방법:**
- GitHub 저장소 → Settings → Branches → Add branch protection rule

---

## 5. 배포 프로세스

### 5.1 Backend 배포 (Docker)

**프로덕션 서버 배포:**

1. **GHCR에서 이미지 Pull**
   ```bash
   docker pull ghcr.io/yhkim-77/mathlens-ai/backend:1.0.0
   ```

2. **환경 변수 설정**
   ```bash
   # .env 파일 생성
   cat > .env <<EOF
   DATABASE_URL=postgresql+asyncpg://user:pass@db:5432/mathlens
   SECRET_KEY=$(openssl rand -hex 32)
   OPENAI_API_KEY=sk-...
   ENVIRONMENT=production
   EOF
   ```

3. **Docker Compose로 실행**
   ```yaml
   # docker-compose.prod.yml
   version: '3.8'
   services:
     api:
       image: ghcr.io/yhkim-77/mathlens-ai/backend:1.0.0
       env_file: .env
       ports:
         - "8000:8000"
       depends_on:
         - db
         - redis
     db:
       image: postgres:14
       environment:
         POSTGRES_DB: mathlens
         POSTGRES_USER: user
         POSTGRES_PASSWORD: pass
     redis:
       image: redis:7-alpine
   ```

   ```bash
   docker compose -f docker-compose.prod.yml up -d
   ```

4. **헬스체크 확인**
   ```bash
   curl http://localhost:8000/health
   # Expected: {"status": "healthy"}
   ```

---

### 5.2 Mobile 배포 (Android)

**Google Play Store 배포:**

1. **Release APK 다운로드**
   - GitHub Release 페이지에서 `app-release.apk` 다운로드

2. **APK 서명 (jarsigner)**
   ```bash
   jarsigner -verbose -sigalg SHA256withRSA -digestalg SHA-256 \
     -keystore my-release-key.keystore app-release.apk my-key-alias
   ```

3. **Zipalign**
   ```bash
   zipalign -v 4 app-release.apk app-release-aligned.apk
   ```

4. **Google Play Console 업로드**
   - https://play.google.com/console
   - 내부 테스트 트랙 → 프로덕션 트랙 순차 배포

**참고:** Android App Bundle (AAB) 사용 권장 (향후 개선)

---

### 5.3 배포 체크리스트

**릴리즈 전 확인사항:**

- [ ] 모든 테스트 PASS (pytest, E2E)
- [ ] Staging 환경에서 QA 완료
- [ ] 보안 스캔 완료 (OWASP ZAP, Bandit)
- [ ] 성능 테스트 완료 (Locust)
- [ ] 데이터베이스 마이그레이션 스크립트 준비
- [ ] Rollback 계획 수립
- [ ] 모니터링 알림 설정 확인
- [ ] 문서 업데이트 (README, API 문서)

**릴리즈 후 확인사항:**

- [ ] 프로덕션 헬스체크 정상
- [ ] 주요 API 엔드포인트 응답 확인
- [ ] 에러 로그 모니터링 (Sentry, CloudWatch)
- [ ] 성능 메트릭 모니터링 (응답 시간, CPU, 메모리)
- [ ] 사용자 피드백 수집

---

## 6. 모니터링 및 롤백

### 6.1 모니터링 도구

**추천 도구:**

| 도구 | 용도 | 설정 |
|------|------|------|
| **Sentry** | 에러 추적, 크래시 리포팅 | SDK 통합 (Python, React Native) |
| **Prometheus + Grafana** | 메트릭 수집, 대시보드 | FastAPI metrics 엔드포인트 |
| **CloudWatch / StackDriver** | 로그 수집, 알림 | Docker 로그 드라이버 |
| **UptimeRobot** | 가동 시간 모니터링, 알림 | HTTP 헬스체크 |

**주요 모니터링 메트릭:**
- API 응답 시간 (P50, P95, P99)
- 에러율 (4xx, 5xx)
- 처리량 (requests/sec)
- CPU/메모리 사용률
- 데이터베이스 연결 풀 상태

---

### 6.2 Rollback 전략

**Backend 롤백 (Docker):**

1. **이전 버전 이미지로 재배포**
   ```bash
   docker compose -f docker-compose.prod.yml down
   docker pull ghcr.io/yhkim-77/mathlens-ai/backend:1.0.0
   docker compose -f docker-compose.prod.yml up -d
   ```

2. **데이터베이스 마이그레이션 롤백 (필요 시)**
   ```bash
   alembic downgrade -1
   ```

**Mobile 롤백 (Android):**
- Google Play Console → "이전 버전 복원" (단계 롤백)
- 긴급: 앱 스토어에서 일시적으로 숨기기 (최후 수단)

**롤백 판단 기준:**
- Critical 버그 발견 (데이터 손실, 크래시)
- 에러율 > 5%
- 응답 시간 P95 > 10초
- 사용자 불만 급증

---

## 7. 트러블슈팅

### 7.1 CI 실패 원인 및 해결

#### 문제 1: Backend Test 실패

**증상:**
```
FAILED tests/test_auth.py::test_register_user - AssertionError
```

**원인:**
- 테스트 코드 오류
- 의존성 버전 불일치
- 환경 변수 누락

**해결:**
1. 로컬에서 테스트 재실행
   ```bash
   cd backend
   pytest tests/test_auth.py::test_register_user -v
   ```
2. 의존성 업데이트
   ```bash
   pip install -r requirements.txt --upgrade
   ```
3. 테스트 수정 후 재푸시

---

#### 문제 2: Android Build 실패 (Gradle)

**증상:**
```
FAILURE: Build failed with an exception.
* What went wrong:
Execution failed for task ':app:mergeDebugResources'.
> Resource linking failed
```

**원인:**
- Gradle 캐시 손상
- 리소스 파일 충돌
- 메모리 부족

**해결:**
1. **Gradle 캐시 초기화**
   ```bash
   ./gradlew clean
   rm -rf ~/.gradle/caches
   ```

2. **메모리 증가** (ci.yml)
   ```yaml
   env:
     JAVA_OPTS: '-Xmx6g'  # 4g → 6g
   ```

3. **리소스 파일 검증**
   - `mobile/android/app/src/main/res/` 확인
   - 중복/손상된 리소스 제거

---

#### 문제 3: Docker Image Push 실패

**증상:**
```
Error: denied: permission_denied
```

**원인:**
- `GITHUB_TOKEN` 권한 부족
- GHCR 패키지 삭제 후 재푸시 (권한 문제)

**해결:**
1. **Workflow 권한 확인** (release.yml)
   ```yaml
   permissions:
     contents: write
     packages: write
   ```

2. **수동 로그인 테스트**
   ```bash
   echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin
   ```

3. **GHCR 패키지 권한 설정**
   - GitHub → Packages → mathlens-ai → Settings → "Add access"

---

### 7.2 자주 묻는 질문 (FAQ)

**Q1: CI가 너무 느려요 (20분 이상 소요). 어떻게 개선하나요?**

A1:
- Gradle/pip 캐싱 확인 (`actions/cache`)
- Docker Buildx 캐시 활성화 (`cache-from/to: type=gha`)
- 테스트 병렬 실행 (`pytest -n auto`)
- Self-hosted runner 사용 (GitHub Enterprise)

---

**Q2: Release를 생성했는데 Docker 이미지가 GHCR에 없어요.**

A2:
- GitHub Actions 로그 확인 → `build-and-push` Job 실패 여부
- GHCR 패키지 페이지 확인: https://github.com/yhkim-77/mathlens-ai/pkgs/container/mathlens-ai%2Fbackend
- `GITHUB_TOKEN` 권한 확인 (`packages:write`)

---

**Q3: Android APK를 다운로드했는데 설치가 안 돼요.**

A3:
- **서명 안 된 APK**: Release APK는 서명이 필요합니다.
- **ADB 설치**:
  ```bash
  adb install app-release.apk
  ```
- **디바이스 설정**: "알 수 없는 소스" 허용

---

## 8. 부록

### 8.1 Workflow 파일 전체 구조

#### ci.yml 구조
```
ci.yml
├── on: [push, pull_request]
├── permissions: {contents: read}
└── jobs:
    ├── backend-test
    │   ├── Set up Python
    │   ├── Install dependencies
    │   └── Run pytest
    ├── backend-docker-build (needs: backend-test)
    │   ├── Set up Docker Buildx
    │   └── Build image (no push)
    └── android-build
        ├── Set up Node.js
        ├── Install JS deps
        ├── Set up JDK
        ├── Cache Gradle
        └── Build debug APK
```

#### release.yml 구조
```
release.yml
├── on: {push: {tags: ['v*.*.*']}}
├── permissions: {contents: write, packages: write}
└── jobs:
    ├── test
    │   └── Run pytest
    ├── build-and-push (needs: test)
    │   ├── Login to GHCR
    │   ├── Extract metadata
    │   └── Build & Push Docker
    ├── build-android-release (needs: test)
    │   └── Build release APK
    └── release (needs: [build-and-push, build-android-release])
        ├── Download APK
        ├── Generate changelog
        └── Create GitHub Release
```

---

### 8.2 배포 환경 비교

| 환경 | 용도 | 인프라 | 데이터 | 배포 주기 |
|------|------|--------|--------|----------|
| **Development** | 개발자 로컬 | Docker Compose | Mock 데이터 | 실시간 (코드 변경 시) |
| **CI** | 자동화 테스트 | GitHub Actions | In-memory SQLite | PR/Push 시 |
| **Staging** | QA 검증 | AWS/GCP | 익명화 프로덕션 데이터 | 태그 푸시 시 (수동) |
| **Production** | 실제 서비스 | AWS/GCP | 실제 사용자 데이터 | 릴리즈 승인 후 (수동) |

---

### 8.3 GitHub Actions 비용 최적화

**무료 티어 한도 (GitHub Free):**
- Public 저장소: 무제한
- Private 저장소: 2,000분/월

**비용 절감 팁:**
1. **캐싱 적극 활용**
   - Gradle, pip, npm 캐싱
   - Docker layer 캐싱

2. **불필요한 Job 제거**
   - `[skip ci]` 커밋 메시지 사용 (문서 변경 시)

3. **Self-hosted Runner 사용** (고급)
   - AWS EC2, 온프레미스 서버

4. **Workflow 최적화**
   - Job 병렬 실행
   - 실패 시 빠른 종료 (`fail-fast: true`)

---

### 8.4 참고 자료

**공식 문서:**
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Build Push Action](https://github.com/docker/build-push-action)
- [Gradle Caching in CI](https://docs.gradle.org/current/userguide/build_cache.html)

**관련 문서:**
- [QA_Validation_Plan.md](./QA_Validation_Plan.md) — QA 검증 계획
- [Test_Cases.md](./Test_Cases.md) — 테스트 케이스
- [Deployment_Guide.md](./Deployment_Guide.md) — 배포 가이드 (예정)

---

**문서 이력:**

| 버전 | 날짜 | 작성자 | 변경 내용 |
|------|------|--------|----------|
| v1.0 | 2026-05-22 | DevOps팀 | 초안 작성 |
