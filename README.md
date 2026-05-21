# MathLens AI 🧮

> 손글씨 수학 풀이 인식 기반 AI 개인 맞춤형 수학 튜터 모바일 애플리케이션

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/Platform-iOS%20%7C%20Android-blue.svg)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)]()

---

## 📱 소개

MathLens AI는 학습자가 스마트 기기 위에 펜 또는 손가락으로 수학 풀이 과정을 작성하면, AI가 이를 인식하고 분석하여 오답의 근본 원인을 찾아 맞춤형 피드백과 반복 학습을 제공하는 모바일 앱입니다.

### 핵심 기능

- ✍️ **손글씨 수식 인식** — 펜/터치 입력을 실시간으로 수식 변환
- 🧠 **AI 풀이 분석** — 오답 원인을 개념 오류 / 절차 오류 / 계산 실수로 분류
- 💡 **맞춤형 개념 설명** — 학습자 수준에 맞춘 개인화 피드백 제공
- 🔁 **반복 학습 시스템** — 동일 유형 문제 재출제로 완전 학습 유도
- 📊 **학습 리포트** — 취약 개념 및 학습 현황 시각화

---

## 🗂️ 프로젝트 구조

```
mathlens-ai/
├── android/                  # Android 앱 (Kotlin + Jetpack Compose)
│   └── app/src/main/
│       ├── java/com/mathlens/ai/
│       │   ├── ui/           # UI 컴포넌트
│       │   ├── ai/           # AI 분석 모듈
│       │   ├── data/         # 데이터 레이어
│       │   └── utils/        # 유틸리티
│       └── res/              # 리소스
├── ios/                      # iOS 앱 (Swift + SwiftUI)
│   └── MathLensAI/
│       ├── Views/            # SwiftUI 뷰
│       ├── ViewModels/       # 뷰모델
│       ├── Services/         # 서비스 레이어
│       └── Models/           # 데이터 모델
├── backend/                  # AI 백엔드 서버 (FastAPI)
│   └── app/
│       ├── api/              # API 라우터
│       ├── services/         # 비즈니스 로직
│       └── models/           # 데이터 모델
├── docs/                     # 문서
│   ├── RFP.md                # 제안요청서
│   └── ARCHITECTURE.md       # 시스템 아키텍처
└── .github/workflows/        # CI/CD
```

---

## 🚀 시작하기

### Android

```bash
cd android
./gradlew assembleDebug
```

### iOS

```bash
cd ios
pod install
open MathLensAI.xcworkspace
```

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## 🛠️ 기술 스택

| 영역 | 기술 |
|------|------|
| Android | Kotlin, Jetpack Compose, Android Ink API, ML Kit |
| iOS | Swift, SwiftUI, PencilKit, Vision Framework |
| Backend | Python, FastAPI, PostgreSQL, Redis |
| AI/ML | LLM (Claude/GPT-4o), HTR 엔진, MathPix API |
| 인프라 | AWS, Docker, GitHub Actions |

---

## 📋 개발 로드맵

- [x] 프로젝트 초기 설정
- [ ] Phase 1: MVP (손글씨 인식 + AI 분석 + 기본 피드백)
- [ ] Phase 2: 기능 확장 (학부모 대시보드, 문제은행)
- [ ] Phase 3: 고도화 (온디바이스 AI, 실시간 협업)

---

## 📄 문서

- [RFP 문서 v1.0](docs/RFP.md)
- [RFP 문서 v1.1](docs/RFP_v1.1.md)
- [RFP 문서 v2.0](docs/RFP_v2.0.md) — 펜 수식 인식 기술 현실 구현 방안 중심 최신판
- [PRD (제품 요구사항 문서)](docs/PRD.md)
- [시스템 아키텍처](docs/ARCHITECTURE.md)

---

## 🤝 기여하기

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📜 라이선스

MIT License — 자세한 내용은 [LICENSE](LICENSE) 파일을 참고하세요.

---

## 👤 개발자

**melchi45**
- GitHub: [@melchi45](https://github.com/melchi45)
