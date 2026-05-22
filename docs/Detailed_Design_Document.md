# MathLens AI — Detailed Technical Design Document (상세 설계서)

**Document Version:** v1.0
**Date:** 2026-05-22
**Document Type:** Detailed Technical Design Document (TDD)
**Author:** MathLens AI Engineering Team
**Status:** Draft

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Architecture Overview](#2-architecture-overview)
3. [Component Design](#3-component-design)
4. [Data Flow Design](#4-data-flow-design)
5. [Algorithm Specifications](#5-algorithm-specifications)
6. [API Interface Design](#6-api-interface-design)
7. [Data Storage Design](#7-data-storage-design)
8. [Security Design](#8-security-design)
9. [Performance Optimization](#9-performance-optimization)
10. [Error Handling Strategy](#10-error-handling-strategy)

---

## 1. Introduction

### 1.1 Purpose

This Detailed Technical Design Document (TDD) provides in-depth technical specifications for implementing the MathLens AI system. It covers component architecture, algorithms, data structures, API contracts, and implementation guidelines.

### 1.2 Scope

This document details the technical design for:
- Backend API services (FastAPI)
- Mobile applications (React Native)
- AI processing pipeline (GPT-4o integration)
- Database schema and queries
- Integration points and protocols

### 1.3 Audience

- Software Engineers (Backend, Frontend, Mobile)
- AI/ML Engineers
- DevOps Engineers
- QA Engineers
- Technical Architects

---

## 2. Architecture Overview

### 2.1 System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client Layer                            │
├─────────────────────────────────────────────────────────────────┤
│  React Native Mobile App                                        │
│  ├── UI Components (React)                                      │
│  ├── State Management (Redux Toolkit)                           │
│  ├── API Client (Axios)                                         │
│  ├── WebSocket Client                                           │
│  └── Local Storage (AsyncStorage)                               │
└─────────────────┬───────────────────────────────────────────────┘
                  │ HTTPS / WSS
                  │
┌─────────────────▼───────────────────────────────────────────────┐
│                       API Gateway Layer                         │
├─────────────────────────────────────────────────────────────────┤
│  FastAPI Server                                                 │
│  ├── Authentication Middleware (JWT)                            │
│  ├── Rate Limiting Middleware                                   │
│  ├── CORS Middleware                                            │
│  └── Request Logging                                            │
└─────────────────┬───────────────────────────────────────────────┘
                  │
                  │
┌─────────────────▼───────────────────────────────────────────────┐
│                      Application Layer                          │
├─────────────────────────────────────────────────────────────────┤
│  API Routers                                                    │
│  ├── /api/v1/auth          (Authentication)                     │
│  ├── /api/v1/submissions   (Solution Submission)               │
│  ├── /api/v1/analyze       (Sync Analysis)                      │
│  ├── /api/v1/problems      (Problem Bank)                       │
│  ├── /api/v1/users         (User Management)                    │
│  └── /api/v1/concepts      (Concept Management)                 │
│                                                                 │
│  Service Layer                                                  │
│  ├── AnalysisService       (AI Analysis Logic)                  │
│  ├── ProblemService        (Recommendation Engine)              │
│  ├── UserService           (User Operations)                    │
│  ├── ConceptService        (Concept Tracking)                   │
│  └── AuthService           (Authentication)                     │
└─────────────────┬───────────────────────────────────────────────┘
                  │
                  │
┌─────────────────▼───────────────────────────────────────────────┐
│                    Integration Layer                            │
├─────────────────────────────────────────────────────────────────┤
│  External Services                                              │
│  ├── OpenAI GPT-4o API     (Primary AI Analysis)               │
│  ├── Anthropic Claude API  (Fallback)                           │
│  ├── MathPix OCR API       (HTR Fallback)                       │
│  └── AWS S3                (Image Storage)                      │
│                                                                 │
│  Async Processing (Future)                                     │
│  ├── Celery Workers        (Background Tasks)                   │
│  ├── Redis Queue           (Task Queue)                         │
│  └── WebSocket Server      (Real-time Updates)                  │
└─────────────────┬───────────────────────────────────────────────┘
                  │
                  │
┌─────────────────▼───────────────────────────────────────────────┐
│                       Data Layer                                │
├─────────────────────────────────────────────────────────────────┤
│  PostgreSQL Database (Production) / SQLite (Development)        │
│  ├── Users                                                      │
│  ├── Problems                                                   │
│  ├── Submissions                                                │
│  ├── RecognitionResults                                         │
│  ├── ConceptMastery                                             │
│  └── UserProblemHistory                                         │
│                                                                 │
│  AWS S3 Object Storage                                          │
│  ├── Solution Images                                            │
│  └── Problem Images                                             │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Technology Stack Details

#### Backend
- **Framework**: FastAPI 0.109+ (Python 3.11+)
- **ORM**: SQLAlchemy 2.0 (async)
- **Database**: PostgreSQL 15+ (production), SQLite (dev)
- **Authentication**: JWT (python-jose), bcrypt
- **API Documentation**: OpenAPI 3.0 (auto-generated by FastAPI)
- **Testing**: pytest, pytest-asyncio

#### Mobile
- **Framework**: React Native 0.74
- **Language**: TypeScript 5.0+
- **State Management**: Redux Toolkit
- **Navigation**: React Navigation 6
- **API Client**: Axios
- **Local Storage**: AsyncStorage
- **UI Components**: React Native Paper

#### AI/ML
- **Primary LLM**: OpenAI GPT-4o (via API)
- **Fallback LLM**: Anthropic Claude 3.5 Sonnet
- **HTR**: MyScript iink SDK (Phase 2), MathPix API (fallback)
- **Math Rendering**: KaTeX (via WebView)
- **Symbolic Math**: SymPy (Python)

---

## 3. Component Design

### 3.1 Backend Components

#### 3.1.1 Authentication Service

**File**: `backend/app/services/auth.py`

**Class**: `AuthService`

**Responsibilities:**
- User registration and login
- JWT token generation and validation
- Password hashing and verification
- Social OAuth integration

**Key Methods:**

```python
class AuthService:
    @staticmethod
    async def register_user(
        email: str,
        password: str,
        name: str,
        grade: str,
        db: AsyncSession
    ) -> User:
        """
        Register a new user.

        Args:
            email: User email (unique)
            password: Plain text password (will be hashed)
            name: User's full name
            grade: Grade level (middle_1 to high_3)
            db: Database session

        Returns:
            Created User object

        Raises:
            ValueError: If email already exists
            ValidationError: If input validation fails
        """
        # Check if email exists
        existing = await db.execute(
            select(User).where(User.email == email)
        )
        if existing.scalar_one_or_none():
            raise ValueError("Email already registered")

        # Hash password
        hashed_password = get_password_hash(password)

        # Create user
        user = User(
            email=email,
            hashed_password=hashed_password,
            name=name,
            grade=grade
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

        return user

    @staticmethod
    def create_access_token(
        user_id: str,
        expires_delta: timedelta = timedelta(hours=1)
    ) -> str:
        """
        Create JWT access token.

        Args:
            user_id: User UUID
            expires_delta: Token expiration time

        Returns:
            Encoded JWT string
        """
        to_encode = {
            "sub": user_id,
            "exp": datetime.utcnow() + expires_delta,
            "type": "access"
        }
        return jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm="HS256"
        )

    @staticmethod
    async def verify_token(token: str, db: AsyncSession) -> User:
        """
        Verify JWT token and return user.

        Args:
            token: JWT token string
            db: Database session

        Returns:
            User object

        Raises:
            HTTPException: If token invalid or expired
        """
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=["HS256"]
            )
            user_id = payload.get("sub")
            if not user_id:
                raise HTTPException(401, "Invalid token")

            user = await db.get(User, user_id)
            if not user:
                raise HTTPException(401, "User not found")

            return user

        except JWTError:
            raise HTTPException(401, "Invalid token")
```

---

#### 3.1.2 Analysis Service

**File**: `backend/app/services/analysis.py`

**Class**: `AnalysisService`

**Responsibilities:**
- Call GPT-4o API for solution analysis
- Parse AI response into structured format
- Classify error types
- Generate personalized feedback

**Key Methods:**

```python
class AnalysisService:
    def __init__(self):
        self.openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.claude_client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

    async def analyze_solution(
        self,
        problem: Problem,
        student_latex: str,
        student_image_base64: Optional[str],
        student_grade: str
    ) -> AnalysisResult:
        """
        Analyze student's solution using GPT-4o.

        Args:
            problem: Problem object
            student_latex: Recognized LaTeX solution
            student_image_base64: Base64 encoded solution image
            student_grade: Student's grade level

        Returns:
            AnalysisResult with error classification and feedback

        Raises:
            AnalysisError: If analysis fails
        """
        try:
            # Build prompt
            messages = self._build_analysis_prompt(
                problem, student_latex, student_image_base64, student_grade
            )

            # Call GPT-4o
            response = await self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=0.3,
                max_tokens=2000,
                response_format={"type": "json_object"}
            )

            # Parse response
            content = response.choices[0].message.content
            result_data = json.loads(content)

            # Validate and structure result
            return self._parse_analysis_result(result_data)

        except OpenAIError as e:
            # Fallback to Claude
            logger.warning(f"GPT-4o failed, falling back to Claude: {e}")
            return await self._analyze_with_claude(
                problem, student_latex, student_image_base64, student_grade
            )

    def _build_analysis_prompt(
        self,
        problem: Problem,
        student_latex: str,
        student_image_base64: Optional[str],
        student_grade: str
    ) -> List[Dict]:
        """Build messages for GPT-4o API."""
        system_prompt = f"""You are an expert math tutor analyzing a {student_grade} student's solution.

Analyze the student's work and identify:
1. Is the solution correct?
2. If incorrect, which step has the error?
3. What type of error (conceptual, procedural, computational, comprehension)?
4. What specific misconception does the student have?

Respond in JSON format:
{{
  "is_correct": bool,
  "error_steps": [
    {{
      "step_order": int,
      "error_type": "conceptual|procedural|computational|comprehension",
      "error_subtype": "specific_error",
      "description": "Korean explanation",
      "correct_expression": "LaTeX"
    }}
  ],
  "concept_understanding_summary": "Korean summary",
  "feedback_message": "Korean feedback (300-500 chars)",
  "recommended_concept_tags": ["tag1", "tag2"]
}}
"""

        user_content = [
            {
                "type": "text",
                "text": f"""Problem: {problem.content_text}

Correct Answer: {problem.answer_latex}

Student's Solution (LaTeX):
{student_latex}
"""
            }
        ]

        # Add image if available
        if student_image_base64:
            user_content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{student_image_base64}"
                }
            })

        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ]

    def _parse_analysis_result(self, data: Dict) -> AnalysisResult:
        """Parse and validate AI response."""
        return AnalysisResult(
            is_correct=data["is_correct"],
            error_steps=[
                ErrorStep(
                    step_order=step["step_order"],
                    error_type=step["error_type"],
                    error_subtype=step["error_subtype"],
                    description=step["description"],
                    correct_expression=step["correct_expression"]
                )
                for step in data.get("error_steps", [])
            ],
            concept_understanding_summary=data["concept_understanding_summary"],
            feedback_message=data["feedback_message"],
            recommended_concept_tags=data["recommended_concept_tags"]
        )
```

---

#### 3.1.3 Problem Recommendation Service

**File**: `backend/app/services/problems.py`

**Class**: `ProblemService`

**Responsibilities:**
- Recommend personalized problems
- Calculate concept mastery scores
- Adjust difficulty dynamically
- Generate similar problems via AI

**Key Methods:**

```python
class ProblemService:
    @staticmethod
    async def recommend_problem(
        user: User,
        db: AsyncSession
    ) -> Problem:
        """
        Recommend a personalized problem for the user.

        Algorithm:
        1. Get user's error history (last 30 days)
        2. Calculate concept mastery scores
        3. Identify weak concepts (mastery < 0.6)
        4. Query problems with 70% weak concepts, 30% strong concepts
        5. Adjust difficulty based on recent performance
        6. Filter out recently solved problems
        7. Return best match

        Args:
            user: User object
            db: Database session

        Returns:
            Recommended Problem

        Raises:
            NoProblemsError: If no suitable problems found
        """
        # Get weak concepts
        weak_concepts = await ProblemService._get_weak_concepts(user, db)

        # Get strong concepts (for review)
        strong_concepts = await ProblemService._get_strong_concepts(user, db)

        # Mix 70-30
        target_concepts = (
            random.sample(weak_concepts, k=min(2, len(weak_concepts))) +
            random.sample(strong_concepts, k=min(1, len(strong_concepts)))
        )

        # Get target difficulty
        difficulty = await ProblemService._calculate_target_difficulty(
            user, db
        )

        # Query problems
        stmt = (
            select(Problem)
            .where(
                Problem.grade == user.grade,
                Problem.status == "active",
                Problem.concept_tags.op("&&")(target_concepts),  # Array overlap
                Problem.difficulty == difficulty
            )
            .order_by(func.random())
            .limit(10)
        )

        results = await db.execute(stmt)
        candidates = results.scalars().all()

        if not candidates:
            raise NoProblemsError("No suitable problems found")

        # Filter recently solved
        recent_problem_ids = await ProblemService._get_recent_problem_ids(
            user, db, days=7
        )
        candidates = [p for p in candidates if p.id not in recent_problem_ids]

        if not candidates:
            # Expand search to all difficulties
            return await ProblemService._recommend_fallback(user, db)

        # Return first match (already randomized)
        return candidates[0]

    @staticmethod
    async def _get_weak_concepts(
        user: User,
        db: AsyncSession,
        threshold: float = 0.6
    ) -> List[str]:
        """Get concepts where user's mastery is below threshold."""
        stmt = (
            select(ConceptMastery.concept_id)
            .where(
                ConceptMastery.user_id == user.id,
                ConceptMastery.mastery_score < threshold
            )
        )
        result = await db.execute(stmt)
        return [row[0] for row in result.all()]

    @staticmethod
    async def _calculate_target_difficulty(
        user: User,
        db: AsyncSession
    ) -> int:
        """
        Calculate target difficulty based on recent performance.

        Rules:
        - 3 consecutive correct → increase difficulty
        - 2 consecutive incorrect → decrease difficulty
        - Otherwise → maintain current difficulty
        """
        # Get last 5 submissions
        stmt = (
            select(RecognitionResult.is_correct)
            .join(Submission)
            .where(Submission.user_id == user.id)
            .order_by(Submission.submitted_at.desc())
            .limit(5)
        )
        result = await db.execute(stmt)
        recent_results = [row[0] for row in result.all()]

        if not recent_results:
            return 3  # Default medium difficulty

        # Check patterns
        if recent_results[:3] == [True, True, True]:
            # 3 correct → increase
            return min(user.current_difficulty + 1, 5)
        elif recent_results[:2] == [False, False]:
            # 2 incorrect → decrease
            return max(user.current_difficulty - 1, 1)
        else:
            # Maintain
            return user.current_difficulty

    @staticmethod
    async def generate_similar_problem(
        source_problem: Problem,
        db: AsyncSession
    ) -> Problem:
        """
        Generate a similar problem using GPT-4o.

        Args:
            source_problem: Original problem
            db: Database session

        Returns:
            Newly generated Problem

        Raises:
            GenerationError: If generation fails
        """
        client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

        prompt = f"""Generate a similar math problem to the following,
keeping the same concept and difficulty but changing the numbers and context.

Original Problem:
{source_problem.content_text}

Concept Tags: {', '.join(source_problem.concept_tags)}
Grade: {source_problem.grade}
Difficulty: {source_problem.difficulty}/5

Generate a new problem with:
1. Same mathematical concept
2. Different numbers/variables
3. Similar difficulty level
4. LaTeX formatted answer

Respond in JSON:
{{
  "problem_text": "...",
  "answer_latex": "...",
  "hint": "..."
}}
"""

        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a math problem generator."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000,
            response_format={"type": "json_object"}
        )

        data = json.loads(response.choices[0].message.content)

        # Validate LaTeX
        try:
            parse_latex(data["answer_latex"])  # SymPy validation
        except Exception as e:
            raise GenerationError(f"Invalid LaTeX: {e}")

        # Create new problem
        new_problem = Problem(
            title=f"Generated from {source_problem.id}",
            content_text=data["problem_text"],
            answer_latex=data["answer_latex"],
            subject=source_problem.subject,
            grade=source_problem.grade,
            difficulty=source_problem.difficulty,
            concept_tags=source_problem.concept_tags,
            source="llm_generated",
            status="active"
        )

        db.add(new_problem)
        await db.commit()
        await db.refresh(new_problem)

        return new_problem
```

---

### 3.2 Mobile Components

#### 3.2.1 Redux Store Structure

```typescript
// store/index.ts

import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice';
import problemReducer from './slices/problemSlice';
import canvasReducer from './slices/canvasSlice';
import submissionReducer from './slices/submissionSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    problem: problemReducer,
    canvas: canvasReducer,
    submission: submissionReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: false, // For Date objects
    }),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
```

#### 3.2.2 Canvas Component

```typescript
// components/Canvas.tsx

import React, { useRef, useCallback } from 'react';
import { View, StyleSheet } from 'react-native';
import { Canvas as SkiaCanvas, Path, Stroke } from '@shopify/react-native-skia';
import { useDispatch, useSelector } from 'react-redux';
import { addStroke, undo, redo } from '../store/slices/canvasSlice';

interface Point {
  x: number;
  y: number;
  pressure: number;
  timestamp: number;
}

interface StrokeData {
  id: string;
  points: Point[];
  color: string;
  width: number;
  tool: 'pen' | 'eraser' | 'highlighter';
}

export const Canvas: React.FC = () => {
  const dispatch = useDispatch();
  const { strokes, currentTool, currentColor, currentWidth } = useSelector(
    (state: RootState) => state.canvas
  );

  const currentStroke = useRef<Point[]>([]);

  const handleTouchStart = useCallback((event: TouchEvent) => {
    const { locationX, locationY, force } = event.nativeEvent;
    currentStroke.current = [{
      x: locationX,
      y: locationY,
      pressure: force || 1.0,
      timestamp: Date.now()
    }];
  }, []);

  const handleTouchMove = useCallback((event: TouchEvent) => {
    const { locationX, locationY, force } = event.nativeEvent;
    currentStroke.current.push({
      x: locationX,
      y: locationY,
      pressure: force || 1.0,
      timestamp: Date.now()
    });
  }, []);

  const handleTouchEnd = useCallback(() => {
    if (currentStroke.current.length > 0) {
      const stroke: StrokeData = {
        id: `stroke_${Date.now()}`,
        points: currentStroke.current,
        color: currentColor,
        width: currentWidth,
        tool: currentTool
      };
      dispatch(addStroke(stroke));
      currentStroke.current = [];

      // Trigger auto-save after stroke
      dispatch(triggerAutoSave());
    }
  }, [dispatch, currentTool, currentColor, currentWidth]);

  return (
    <View style={styles.container}>
      <SkiaCanvas
        style={styles.canvas}
        onTouchStart={handleTouchStart}
        onTouchMove={handleTouchMove}
        onTouchEnd={handleTouchEnd}
      >
        {strokes.map((stroke) => (
          <Path
            key={stroke.id}
            path={buildPathFromPoints(stroke.points)}
            color={stroke.color}
            style="stroke"
            strokeWidth={stroke.width}
            strokeCap="round"
            strokeJoin="round"
          />
        ))}
      </SkiaCanvas>
    </View>
  );
};

function buildPathFromPoints(points: Point[]): string {
  if (points.length === 0) return '';

  let path = `M ${points[0].x} ${points[0].y}`;
  for (let i = 1; i < points.length; i++) {
    // Apply pressure to width (optional)
    path += ` L ${points[i].x} ${points[i].y}`;
  }
  return path;
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#FFFFFF',
  },
  canvas: {
    flex: 1,
  },
});
```

---

## 4. Data Flow Design

### 4.1 Solution Submission Flow

```
┌──────────────────────────────────────────────────────────────────┐
│ PHASE 1: Client-side Processing                                 │
└──────────────────────────────────────────────────────────────────┘

[Canvas Component]
    │
    │ 1. User finishes writing
    │ 2. Taps "Submit" button
    │
    ▼
[Submission Handler]
    │
    │ 3. Validate canvas (strokes exist)
    │ 4. Capture canvas as PNG image
    │ 5. Compress image (target: < 2MB)
    │ 6. Convert to Base64
    │
    ▼
[iink SDK Recognition] (if available)
    │
    │ 7. Extract LaTeX from strokes
    │ 8. Get confidence score
    │
    ▼
[Build Submission Payload]
    │
    │ 9. Package data:
    │    - problem_id
    │    - image_base64
    │    - recognized_latex
    │    - stroke_metadata
    │    - device_info
    │
    ▼
[API Client]
    │
    │ 10. POST /api/v1/submissions
    │
    ▼
┌──────────────────────────────────────────────────────────────────┐
│ PHASE 2: Server-side Processing                                 │
└──────────────────────────────────────────────────────────────────┘

[FastAPI Endpoint: POST /submissions]
    │
    │ 11. Validate JWT token
    │ 12. Validate request payload
    │ 13. Generate submission_id
    │ 14. Create Submission record (status="received")
    │ 15. Return 202 Accepted with submission_id
    │
    ▼
[Analysis Service]
    │
    │ 16. Retrieve Problem from database
    │ 17. If LaTeX not provided, skip HTR
    │ 18. Call GPT-4o API with:
    │     - Problem statement
    │     - Student LaTeX
    │     - Student image (Base64)
    │     - Student grade level
    │
    ▼
[GPT-4o Processing]
    │
    │ 19. Analyze solution step-by-step
    │ 20. Classify error type
    │ 21. Generate feedback message
    │ 22. Return structured JSON
    │
    ▼
[Result Processing]
    │
    │ 23. Parse GPT-4o response
    │ 24. Create RecognitionResult record
    │ 25. Update Submission status="completed"
    │ 26. Update ConceptMastery records
    │ 27. Add to UserProblemHistory
    │
    ▼
[Response to Client]
    │
    │ 28. Client polls GET /submissions/{id}/status
    │     OR WebSocket push (Phase 2)
    │ 29. Return analysis result
    │
    ▼
┌──────────────────────────────────────────────────────────────────┐
│ PHASE 3: Client-side Rendering                                  │
└──────────────────────────────────────────────────────────────────┘

[Feedback Screen]
    │
    │ 30. Display is_correct badge
    │ 31. Highlight error region on image
    │ 32. Show feedback message
    │ 33. Render LaTeX explanation
    │ 34. Offer action buttons:
    │     - Try Again
    │     - Similar Problem
    │     - Learn Concept
    │     - Next Problem
```

---

## 5. Algorithm Specifications

### 5.1 Concept Mastery Score Calculation

**Algorithm**: Exponentially Weighted Moving Average (EWMA)

**Formula**:
```
mastery_score = α * current_result + (1 - α) * previous_mastery_score

where:
  α = 0.3 (learning rate)
  current_result = 1.0 if correct, 0.0 if incorrect
  initial mastery_score = 0.5 (unknown)
```

**Implementation**:
```python
def update_concept_mastery(
    user_id: str,
    concept_id: str,
    is_correct: bool,
    db: AsyncSession
):
    """Update concept mastery using EWMA."""
    alpha = 0.3  # Learning rate

    # Get existing mastery record
    stmt = select(ConceptMastery).where(
        ConceptMastery.user_id == user_id,
        ConceptMastery.concept_id == concept_id
    )
    result = await db.execute(stmt)
    mastery = result.scalar_one_or_none()

    if not mastery:
        # Create new record
        mastery = ConceptMastery(
            user_id=user_id,
            concept_id=concept_id,
            mastery_score=0.5,  # Initial
            consecutive_correct=0,
            status="learning"
        )
        db.add(mastery)

    # Update score
    current_result = 1.0 if is_correct else 0.0
    mastery.mastery_score = (
        alpha * current_result + (1 - alpha) * mastery.mastery_score
    )

    # Update consecutive correct count
    if is_correct:
        mastery.consecutive_correct += 1
        if mastery.consecutive_correct >= 3:
            mastery.status = "mastered"
            # Schedule spaced repetition
            mastery.next_review_at = datetime.utcnow() + timedelta(days=1)
    else:
        mastery.consecutive_correct = 0
        mastery.status = "learning"

    await db.commit()
```

---

### 5.2 Problem Difficulty Adjustment Algorithm

**Algorithm**: Adaptive Difficulty with Exponential Moving Average

**Goal**: Keep student in "optimal challenge zone" (60-70% success rate)

**Implementation**:
```python
async def adjust_difficulty(user: User, db: AsyncSession) -> int:
    """
    Adjust problem difficulty based on recent performance.

    Returns:
        New difficulty level (1-5)
    """
    # Get last 10 submissions
    stmt = (
        select(RecognitionResult.is_correct)
        .join(Submission)
        .where(Submission.user_id == user.id)
        .order_by(Submission.submitted_at.desc())
        .limit(10)
    )
    result = await db.execute(stmt)
    recent_results = [row[0] for row in result.all()]

    if len(recent_results) < 3:
        # Not enough data, use medium
        return 3

    # Calculate success rate
    success_rate = sum(recent_results) / len(recent_results)

    # Get current difficulty
    current = user.current_difficulty or 3

    # Adjustment rules
    if success_rate >= 0.8:
        # Too easy → increase
        return min(current + 1, 5)
    elif success_rate <= 0.4:
        # Too hard → decrease
        return max(current - 1, 1)
    elif success_rate >= 0.7:
        # Slightly easy → gentle increase
        if len(recent_results) >= 5 and all(recent_results[:5]):
            return min(current + 1, 5)
    elif success_rate <= 0.5:
        # Slightly hard → gentle decrease
        if len(recent_results) >= 4 and not any(recent_results[:4]):
            return max(current - 1, 1)

    # Optimal zone → maintain
    return current
```

---

### 5.3 LaTeX Equivalence Checking

**Purpose**: Determine if two LaTeX expressions are mathematically equivalent

**Tool**: SymPy symbolic math library

**Implementation**:
```python
from sympy import simplify, sympify
from sympy.parsing.latex import parse_latex

def are_latex_equivalent(latex1: str, latex2: str) -> bool:
    """
    Check if two LaTeX expressions are mathematically equivalent.

    Args:
        latex1: First LaTeX expression
        latex2: Second LaTeX expression

    Returns:
        True if equivalent, False otherwise

    Example:
        are_latex_equivalent("2x + 3", "3 + 2x") → True
        are_latex_equivalent("x^2 - 4", "(x-2)(x+2)") → True
    """
    try:
        # Parse LaTeX to SymPy expressions
        expr1 = parse_latex(latex1)
        expr2 = parse_latex(latex2)

        # Simplify and compare
        diff = simplify(expr1 - expr2)

        return diff == 0

    except Exception as e:
        logger.warning(f"LaTeX comparison failed: {e}")
        # Fallback to string normalization
        return normalize_latex(latex1) == normalize_latex(latex2)

def normalize_latex(latex: str) -> str:
    """Normalize LaTeX string for basic comparison."""
    # Remove whitespace
    latex = latex.replace(" ", "")
    # Normalize cdot vs *
    latex = latex.replace("\\cdot", "*")
    # Normalize fractions
    latex = latex.replace("\\frac", "\\dfrac")
    return latex.lower()
```

---

## 6. API Interface Design

### 6.1 REST API Specifications

#### POST /api/v1/submissions

**Description**: Submit handwritten solution for AI analysis

**Request**:
```http
POST /api/v1/submissions HTTP/1.1
Authorization: Bearer {jwt_token}
Content-Type: application/json

{
  "problem_id": "uuid",
  "image_base64": "iVBORw0KG...",
  "recognized_latex": "2x + 3 = 7 \\\\ 2x = 4 \\\\ x = 2",
  "stroke_metadata": {
    "stroke_count": 42,
    "total_duration_ms": 35000
  },
  "device_info": {
    "platform": "ios",
    "os_version": "17.4"
  }
}
```

**Response** (202 Accepted):
```json
{
  "submission_id": "uuid",
  "status": "received",
  "estimated_time_ms": 5000
}
```

**Error Responses**:
- `400 Bad Request`: Invalid payload
- `401 Unauthorized`: Invalid/missing JWT
- `404 Not Found`: Problem not found
- `413 Payload Too Large`: Image > 2MB
- `429 Too Many Requests`: Rate limit exceeded (60/hour)

---

#### GET /api/v1/submissions/{id}/status

**Description**: Poll submission processing status

**Request**:
```http
GET /api/v1/submissions/{id}/status HTTP/1.1
Authorization: Bearer {jwt_token}
```

**Response** (200 OK):
```json
{
  "submission_id": "uuid",
  "status": "completed",
  "result": {
    "is_correct": false,
    "error_steps": [
      {
        "step_order": 2,
        "error_type": "procedural",
        "error_subtype": "sign_error",
        "description": "이항 시 부호가 바뀌지 않았습니다.",
        "correct_expression": "2x = 7 - 3"
      }
    ],
    "feedback_message": "등식의 성질에서 이항할 때는 부호를 반대로 바꿔야 해요...",
    "recommended_concept_tags": ["일차방정식", "이항"]
  },
  "processing_time_ms": 3245
}
```

**Status Values**:
- `received`: Submission accepted
- `processing`: AI analysis in progress
- `completed`: Analysis finished
- `failed`: Processing error

---

### 6.2 WebSocket Protocol (Future)

**Connection**: `wss://api.mathlens.ai/ws/v1/submissions/{submission_id}`

**Client → Server** (Authentication):
```json
{
  "type": "auth",
  "token": "jwt_access_token"
}
```

**Server → Client** (Status Updates):
```json
{
  "type": "status",
  "submission_id": "uuid",
  "stage": "received",
  "timestamp": "2026-05-22T10:30:00Z"
}
```

```json
{
  "type": "status",
  "submission_id": "uuid",
  "stage": "htr_done",
  "latex_preview": "2x + 3 = 7 \\\\ 2x = 4 \\\\ x = 2",
  "confidence": 0.96,
  "timestamp": "2026-05-22T10:30:02Z"
}
```

```json
{
  "type": "status",
  "submission_id": "uuid",
  "stage": "analysis_done",
  "result_id": "uuid",
  "timestamp": "2026-05-22T10:30:05Z"
}
```

**Server → Client** (Error):
```json
{
  "type": "error",
  "submission_id": "uuid",
  "error_code": "HTR_TIMEOUT",
  "message": "Handwriting recognition timed out",
  "timestamp": "2026-05-22T10:30:10Z"
}
```

---

## 7. Data Storage Design

### 7.1 Database Schema (PostgreSQL)

```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255),
    name VARCHAR(100) NOT NULL,
    grade VARCHAR(20) NOT NULL,
    current_difficulty INT DEFAULT 3,
    daily_goal INT DEFAULT 5,
    notification_enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_active_at TIMESTAMP,
    INDEX idx_users_email (email)
);

-- Problems table
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
    source VARCHAR(50) DEFAULT 'bank',
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_problems_grade_difficulty (grade, difficulty),
    INDEX idx_problems_concept_tags USING GIN (concept_tags),
    INDEX idx_problems_status (status)
);

-- Submissions table
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
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP,
    INDEX idx_submissions_user (user_id, submitted_at DESC),
    INDEX idx_submissions_status (status)
);

-- Recognition Results table
CREATE TABLE recognition_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    submission_id UUID UNIQUE NOT NULL REFERENCES submissions(id) ON DELETE CASCADE,
    is_correct BOOLEAN NOT NULL,
    error_steps JSONB,
    feedback_text TEXT,
    correct_solution_latex TEXT,
    concept_tags_inferred TEXT[],
    llm_model_version VARCHAR(50),
    confidence FLOAT,
    processing_time_ms INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_results_submission (submission_id)
);

-- Concept Mastery table
CREATE TABLE concept_mastery (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    concept_id VARCHAR(100) NOT NULL,
    mastery_score FLOAT DEFAULT 0.5 CHECK (mastery_score BETWEEN 0 AND 1),
    consecutive_correct INT DEFAULT 0,
    status VARCHAR(20) DEFAULT 'learning',
    next_review_at TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_id, concept_id),
    INDEX idx_mastery_user_status (user_id, status, next_review_at)
);

-- User Problem History table
CREATE TABLE user_problem_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    problem_id UUID NOT NULL REFERENCES problems(id),
    submission_id UUID REFERENCES submissions(id),
    is_correct BOOLEAN NOT NULL,
    error_type VARCHAR(50),
    solved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_history_user_problem (user_id, problem_id),
    INDEX idx_history_user_date (user_id, solved_at DESC)
);
```

### 7.2 Indexing Strategy

| Table | Index | Purpose | Type |
|-------|-------|---------|------|
| `users` | `email` | Fast login lookup | B-tree, UNIQUE |
| `problems` | `(grade, difficulty, status)` | Recommendation filtering | Composite B-tree |
| `problems` | `concept_tags` | Tag-based search | GIN (array) |
| `submissions` | `(user_id, submitted_at)` | User history queries | Composite B-tree |
| `recognition_results` | `submission_id` | Join optimization | B-tree, UNIQUE |
| `concept_mastery` | `(user_id, status, next_review_at)` | Review schedule | Composite B-tree |
| `user_problem_history` | `(user_id, solved_at)` | Recent activity | Composite B-tree |

---

## 8. Security Design

### 8.1 Authentication Flow

```
┌─────────────────────────────────────────────────────────────┐
│ JWT Authentication Flow                                     │
└─────────────────────────────────────────────────────────────┘

[Client]
    │
    │ 1. POST /api/v1/auth/token
    │    Body: { email, password }
    │
    ▼
[Backend: /auth/token endpoint]
    │
    │ 2. Query user by email
    │ 3. Verify password (bcrypt)
    │ 4. Generate access token (1h expiry)
    │ 5. Generate refresh token (30d expiry)
    │
    ▼
[Response]
    │
    │ 6. Return tokens:
    │    {
    │      "access_token": "eyJ...",
    │      "refresh_token": "eyJ...",
    │      "token_type": "bearer"
    │    }
    │
    ▼
[Client Stores Tokens]
    │
    │ 7. Save to secure storage:
    │    iOS: Keychain
    │    Android: EncryptedSharedPreferences
    │
    ▼
[Subsequent Requests]
    │
    │ 8. Include header:
    │    Authorization: Bearer {access_token}
    │
    ▼
[Backend: Auth Dependency]
    │
    │ 9. Extract token from header
    │ 10. Decode & verify signature
    │ 11. Check expiry
    │ 12. Load user from database
    │ 13. Inject user into endpoint
    │
    ▼
[If Token Expired]
    │
    │ 14. Return 401 Unauthorized
    │
    ▼
[Client: Refresh Flow]
    │
    │ 15. POST /api/v1/auth/refresh
    │     Body: { refresh_token }
    │
    ▼
[Backend: /auth/refresh endpoint]
    │
    │ 16. Verify refresh token
    │ 17. Generate new access token
    │ 18. Return new access token
```

---

### 8.2 Rate Limiting

**Implementation**: Token bucket algorithm with Redis

**Limits**:
- Submission API: 60 requests per hour per user
- Problem recommendation: 100 requests per hour per user
- Authentication: 5 login attempts per 15 minutes per IP

**Code**:
```python
from fastapi import Request, HTTPException
from redis import Redis
import time

redis_client = Redis(host='localhost', port=6379, db=0)

async def rate_limit_submissions(request: Request, user_id: str):
    """Rate limit submission endpoint."""
    key = f"ratelimit:submission:{user_id}"
    limit = 60  # requests
    window = 3600  # seconds (1 hour)

    # Increment counter
    count = redis_client.incr(key)

    # Set expiry on first request
    if count == 1:
        redis_client.expire(key, window)

    # Check limit
    if count > limit:
        ttl = redis_client.ttl(key)
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Try again in {ttl} seconds."
        )
```

---

### 8.3 Data Encryption

**In Transit**:
- TLS 1.3 for all HTTPS connections
- Certificate from Let's Encrypt or AWS Certificate Manager

**At Rest**:
- Database: PostgreSQL native encryption (LUKS/dm-crypt)
- S3 images: AES-256 server-side encryption (SSE-S3)
- Passwords: bcrypt with salt rounds=12

**PII Handling**:
- Email: Stored in plaintext (required for login)
- Name: Stored in plaintext
- Solution images: Auto-deleted after 30 days (configurable)
- No sensitive financial or health data collected

---

## 9. Performance Optimization

### 9.1 Database Query Optimization

**Problem**: N+1 query problem when loading user's recent submissions with results

**Solution**: Use SQLAlchemy eager loading

```python
# ❌ BAD: N+1 queries
async def get_user_submissions_bad(user_id: str, db: AsyncSession):
    stmt = select(Submission).where(Submission.user_id == user_id)
    submissions = (await db.execute(stmt)).scalars().all()

    # This triggers N additional queries!
    for sub in submissions:
        result = await sub.awaitable_attrs.recognition_result
        # Use result...

# ✅ GOOD: Single query with join
async def get_user_submissions_good(user_id: str, db: AsyncSession):
    stmt = (
        select(Submission)
        .options(selectinload(Submission.recognition_result))
        .where(Submission.user_id == user_id)
        .order_by(Submission.submitted_at.desc())
        .limit(20)
    )
    submissions = (await db.execute(stmt)).scalars().all()

    # All results already loaded!
    for sub in submissions:
        result = sub.recognition_result  # No additional query
        # Use result...
```

---

### 9.2 API Response Caching

**Strategy**: Cache frequently accessed, rarely changing data

**Implementation**: Redis with TTL

```python
from redis import Redis
import json

redis_client = Redis(host='localhost', port=6379, db=0)

async def get_problem(problem_id: str, db: AsyncSession) -> Problem:
    """Get problem with Redis caching."""
    cache_key = f"problem:{problem_id}"

    # Try cache first
    cached = redis_client.get(cache_key)
    if cached:
        data = json.loads(cached)
        return Problem(**data)

    # Cache miss → query database
    problem = await db.get(Problem, problem_id)
    if not problem:
        raise NotFoundError("Problem not found")

    # Cache for 1 hour
    redis_client.setex(
        cache_key,
        3600,
        json.dumps(problem.to_dict())
    )

    return problem
```

**Cached Endpoints**:
- `GET /api/v1/problems/{id}`: 1 hour TTL
- `GET /api/v1/concepts/{id}`: 24 hour TTL
- `GET /api/v1/concepts`: 24 hour TTL

**Cache Invalidation**:
- On `POST /problems` or `PUT /problems/{id}`: Invalidate `problem:{id}`
- On concept updates: Invalidate `concepts` list

---

### 9.3 Image Processing Optimization

**Challenge**: Large canvas images (1080x1440) → slow upload

**Solutions**:

1. **Client-side Compression**:
```typescript
import { Image } from 'react-native';
import { manipulateAsync, SaveFormat } from 'expo-image-manipulator';

async function compressCanvasImage(uri: string): Promise<string> {
  // Resize to max 1024px on long side
  const result = await manipulateAsync(
    uri,
    [{ resize: { width: 1024 } }],
    { compress: 0.85, format: SaveFormat.JPEG }
  );

  // Convert to Base64
  const response = await fetch(result.uri);
  const blob = await response.blob();
  const base64 = await blobToBase64(blob);

  return base64;
}
```

2. **Progressive Upload** (Future):
```typescript
// Upload thumbnail first for quick preview
const thumbnail = await createThumbnail(image, 256);
await api.uploadThumbnail(submissionId, thumbnail);

// Upload full image in background
await api.uploadFullImage(submissionId, image);
```

---

## 10. Error Handling Strategy

### 10.1 Error Taxonomy

| Category | HTTP Status | Action |
|----------|-------------|--------|
| Validation Error | 400 | Show specific field errors |
| Authentication Error | 401 | Redirect to login |
| Authorization Error | 403 | Show "Access denied" message |
| Not Found | 404 | Show "Resource not found" |
| Rate Limit | 429 | Show "Too many requests, retry after X seconds" |
| Internal Server Error | 500 | Log error, show generic message, allow retry |
| Service Unavailable | 503 | Show "Service temporarily down", queue request |

---

### 10.2 Backend Error Handling

```python
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

# Custom exceptions
class MathLensError(Exception):
    """Base exception for MathLens errors."""
    pass

class AnalysisError(MathLensError):
    """AI analysis failed."""
    pass

class NoProblemsError(MathLensError):
    """No suitable problems found."""
    pass

# Global exception handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors."""
    return JSONResponse(
        status_code=400,
        content={
            "error": "validation_error",
            "detail": exc.errors(),
            "message": "Invalid request data"
        }
    )

@app.exception_handler(AnalysisError)
async def analysis_exception_handler(request: Request, exc: AnalysisError):
    """Handle AI analysis errors."""
    logger.error(f"Analysis error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "analysis_error",
            "message": "AI analysis failed. Please try again.",
            "can_retry": True
        }
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Catch-all exception handler."""
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_server_error",
            "message": "An unexpected error occurred.",
            "request_id": request.state.request_id
        }
    )
```

---

### 10.3 Client Error Handling

```typescript
// services/api.ts

import axios, { AxiosError } from 'axios';
import { store } from '../store';
import { logout } from '../store/slices/authSlice';
import { showErrorToast } from '../utils/toast';

export const apiClient = axios.create({
  baseURL: 'https://api.mathlens.ai/api/v1',
  timeout: 30000,
});

// Request interceptor: Add auth token
apiClient.interceptors.request.use((config) => {
  const token = store.getState().auth.accessToken;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor: Handle errors
apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const { response, request, message } = error;

    if (response) {
      // Server responded with error status
      switch (response.status) {
        case 401:
          // Unauthorized → Try refresh token
          const refreshed = await tryRefreshToken();
          if (refreshed) {
            // Retry original request
            return apiClient.request(error.config!);
          } else {
            // Refresh failed → Logout
            store.dispatch(logout());
            showErrorToast('Session expired. Please log in again.');
          }
          break;

        case 429:
          // Rate limit
          const retryAfter = response.headers['retry-after'] || '60';
          showErrorToast(`Too many requests. Try again in ${retryAfter}s.`);
          break;

        case 500:
        case 503:
          // Server error
          showErrorToast('Server error. Please try again later.');
          break;

        default:
          // Other errors
          const errorData = response.data as any;
          showErrorToast(errorData.message || 'An error occurred.');
      }
    } else if (request) {
      // No response received (network error)
      showErrorToast('Network error. Please check your connection.');
    } else {
      // Request setup error
      showErrorToast(message || 'An error occurred.');
    }

    return Promise.reject(error);
  }
);

async function tryRefreshToken(): Promise<boolean> {
  try {
    const refreshToken = store.getState().auth.refreshToken;
    if (!refreshToken) return false;

    const response = await axios.post(
      'https://api.mathlens.ai/api/v1/auth/refresh',
      { refresh_token: refreshToken }
    );

    const { access_token } = response.data;
    store.dispatch(setAccessToken(access_token));

    return true;
  } catch {
    return false;
  }
}
```

---

**Document Revision History:**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| v1.0 | 2026-05-22 | Engineering Team | Initial detailed technical design |

---

*This document is for internal development use.*

*© 2026 MathLens AI Project. All rights reserved.*
