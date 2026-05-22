# MathLens AI — Functional Design Document (기능 설계서)

**Document Version:** v1.0
**Date:** 2026-05-22
**Document Type:** Functional Design Document
**Author:** MathLens AI Development Team
**Status:** Draft

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Functional Requirements Overview](#2-functional-requirements-overview)
3. [Feature Specifications](#3-feature-specifications)
4. [User Workflows](#4-user-workflows)
5. [Functional Dependencies](#5-functional-dependencies)
6. [Acceptance Criteria](#6-acceptance-criteria)
7. [Traceability Matrix](#7-traceability-matrix)

---

## 1. Introduction

### 1.1 Purpose

This Functional Design Document (FDD) specifies the detailed functional requirements and behavioral specifications for the MathLens AI mobile application and backend system. It serves as a blueprint for developers, QA engineers, and stakeholders to understand how each feature should operate.

### 1.2 Scope

This document covers:
- Detailed functional specifications for all Phase 1 features
- User interaction workflows
- Input/output specifications
- Business logic and validation rules
- Integration points between components

### 1.3 Document Conventions

- **FR-XXX-YY**: Functional Requirement ID
- **UC-XX**: Use Case ID
- **BL-XX**: Business Logic Rule ID

---

## 2. Functional Requirements Overview

### 2.1 Feature Hierarchy

```
MathLens AI Application
│
├── Authentication & User Management
│   ├── Social Login (Apple, Google, Kakao)
│   ├── User Profile Management
│   └── Session Management
│
├── Pen Input Canvas
│   ├── Stylus Input Capture
│   ├── Real-time Stroke Rendering
│   ├── Tool Selection (Pen, Eraser, Highlighter)
│   ├── Canvas Manipulation (Zoom, Pan)
│   └── Auto-save & Recovery
│
├── Handwriting Recognition
│   ├── Real-time Math Expression Recognition (iink SDK)
│   ├── LaTeX Conversion
│   ├── Fallback Recognition (MathPix API)
│   └── Manual Correction Interface
│
├── AI Solution Analysis
│   ├── Step-by-step Solution Parsing
│   ├── Error Type Classification
│   ├── Misconception Inference
│   └── Personalized Feedback Generation
│
├── Problem Bank & Recommendation
│   ├── Problem Repository Management
│   ├── Personalized Problem Recommendation
│   ├── AI-powered Similar Problem Generation
│   └── Camera-based Problem Input
│
├── Learning Management
│   ├── Spaced Repetition Scheduling
│   ├── Concept Mastery Tracking
│   ├── Automatic Wrong Answer Notebook
│   └── Learning Progress Dashboard
│
└── Reporting & Analytics
    ├── Student Dashboard
    ├── Weekly/Monthly Reports
    ├── Error Type Distribution
    └── Concept Mastery Heat Map
```

---

## 3. Feature Specifications

### 3.1 Authentication & User Management

#### FR-AUTH-001: Social Login

**Description:** Users can authenticate using Apple, Google, or Kakao accounts.

**Functional Behavior:**
1. User taps "Sign in with [Provider]" button
2. System redirects to provider's authentication page
3. User authorizes the application
4. System receives authorization token
5. System creates or updates user profile
6. System generates JWT access token (1 hour) and refresh token (30 days)
7. System stores tokens securely in device keychain
8. User is redirected to home dashboard

**Input:**
- Provider authorization response (OAuth token, user email, name, profile image)

**Output:**
- JWT access token
- User profile data (id, email, name, grade, avatar_url)

**Business Rules:**
- BL-001: For users under 14, legal guardian consent is required
- BL-002: Email must be unique across all authentication providers
- BL-003: Account linking is allowed if email matches

**Error Handling:**
- E-001: Provider authentication failed → Show error message, allow retry
- E-002: Network timeout → Queue request for retry when connection restored
- E-003: Duplicate email → Prompt user to link accounts

**Acceptance Criteria:**
- ✓ User can sign in with Apple, Google, and Kakao
- ✓ JWT token expires after 1 hour
- ✓ Refresh token successfully extends session
- ✓ User profile is correctly populated
- ✓ Authentication state persists across app restarts

---

#### FR-AUTH-002: User Profile Management

**Description:** Users can view and update their profile settings.

**Functional Behavior:**
1. User navigates to profile screen
2. System displays current profile information
3. User modifies fields (grade, daily goal, notification preferences)
4. User taps "Save" button
5. System validates input
6. System updates user record in database
7. System shows success confirmation

**Editable Fields:**
- Grade level (middle_1 ~ high_3, reexaminee, other)
- Daily problem-solving goal (1-50 problems)
- Notification preferences (push enabled, quiet hours)
- Feedback tone (formal/informal Korean)

**Validation Rules:**
- Daily goal: Integer between 1-50
- Grade level: Must be one of predefined values
- Notification quiet hours: Valid time range (HH:MM format)

**Acceptance Criteria:**
- ✓ Profile changes are saved successfully
- ✓ Invalid input shows appropriate error messages
- ✓ Changes reflect immediately in the UI
- ✓ API call succeeds within 2 seconds (P95)

---

### 3.2 Pen Input Canvas

#### FR-CANVAS-001: Stylus Input Capture

**Description:** Capture smooth, pressure-sensitive pen strokes from Apple Pencil, S-Pen, or generic stylus.

**Functional Behavior:**
1. User touches screen with stylus or finger
2. System detects touch event (ACTION_DOWN)
3. System captures touch coordinates, pressure, timestamp
4. As user moves stylus, system captures stroke path (ACTION_MOVE)
5. System renders stroke in real-time on canvas
6. When user lifts stylus, system finalizes stroke (ACTION_UP)
7. System stores stroke metadata (coordinates, pressure, tool type)

**Input:**
- Touch events (x, y, pressure, timestamp, tool type)

**Output:**
- Visual stroke rendered on canvas
- Stroke data object (path points, style, timestamp)

**Performance Requirements:**
- Rendering latency: ≤ 16ms per frame (60 FPS)
- Touch-to-display lag: ≤ 10ms
- Pressure sensitivity: 256 levels minimum
- Palm rejection: Enabled when stylus is detected

**Acceptance Criteria:**
- ✓ Strokes render smoothly at 60 FPS
- ✓ Pressure affects stroke width visibly
- ✓ No jitter or lag in stroke rendering
- ✓ Palm rejection works correctly
- ✓ Works with Apple Pencil (1st/2nd gen), S-Pen, and finger

---

#### FR-CANVAS-002: Tool Selection

**Description:** Users can select different drawing tools (pen, eraser, highlighter, lasso).

**Functional Behavior:**
1. User taps tool button in toolbar
2. System highlights selected tool
3. System changes cursor/tool mode
4. User draws with selected tool
5. Stroke behavior matches tool characteristics

**Tool Specifications:**

| Tool | Options | Behavior |
|------|---------|----------|
| Pen | 3 widths (1px, 2px, 4px), 5 colors | Opaque stroke |
| Highlighter | 1 width (8px), semi-transparent | Overlay mode, 40% opacity |
| Eraser | Stroke-based, Point-based | Removes intersecting strokes or points |
| Lasso | Selection tool | Selects area, allows move/delete |

**Acceptance Criteria:**
- ✓ Tool selection changes immediately
- ✓ Selected tool persists until changed
- ✓ Tool characteristics (color, width) apply correctly
- ✓ Eraser removes strokes accurately
- ✓ Lasso selection works for move and delete operations

---

#### FR-CANVAS-003: Undo/Redo

**Description:** Users can undo and redo up to 50 actions.

**Functional Behavior:**
1. User draws strokes or performs actions
2. System stores action history (stack, max 50 items)
3. User taps "Undo" button
4. System pops last action from history
5. System removes corresponding stroke(s) from canvas
6. Action is pushed to redo stack
7. User taps "Redo" button
8. System restores action from redo stack

**Undoable Actions:**
- Add stroke
- Erase stroke(s)
- Move selection
- Delete selection
- Clear all

**Business Rules:**
- BL-010: History limited to 50 actions
- BL-011: Redo stack cleared on new action
- BL-012: History cleared on problem submission

**Acceptance Criteria:**
- ✓ Undo removes last action
- ✓ Redo restores undone action
- ✓ Undo/Redo buttons disabled appropriately
- ✓ History persists across canvas zoom/pan

---

#### FR-CANVAS-004: Auto-save & Recovery

**Description:** System automatically saves canvas state every 30 seconds to prevent data loss.

**Functional Behavior:**
1. User draws on canvas
2. Every 30 seconds, system triggers auto-save
3. System serializes current strokes to JSON
4. System stores data in local storage (UserDefaults/SharedPreferences)
5. On app restart, system checks for unsaved work
6. If found, system shows "Restore previous work?" dialog
7. User chooses to restore or discard
8. If restored, canvas loads previous state

**Auto-save Data:**
```json
{
  "problem_id": "uuid",
  "session_id": "uuid",
  "timestamp": "ISO8601",
  "strokes": [
    {
      "id": "stroke_001",
      "tool": "pen",
      "color": "#000000",
      "width": 2,
      "points": [[x1, y1, p1, t1], [x2, y2, p2, t2], ...]
    }
  ],
  "canvas_size": {"width": 1080, "height": 1440}
}
```

**Business Rules:**
- BL-020: Auto-save only if strokes exist
- BL-021: Auto-save data expires after 7 days
- BL-022: Submitted work auto-save is deleted

**Acceptance Criteria:**
- ✓ Auto-save triggers every 30 seconds
- ✓ Recovery dialog appears on app restart
- ✓ Restored canvas matches saved state
- ✓ Old auto-saves are cleaned up

---

### 3.3 Handwriting Recognition

#### FR-HTR-001: Real-time Math Expression Recognition

**Description:** As user writes, system recognizes math expressions in real-time using iink SDK.

**Functional Behavior:**
1. User writes math expression on canvas
2. After 200ms of no input, system triggers recognition
3. System passes stroke data to iink SDK
4. iink SDK returns LaTeX string and confidence score
5. System renders LaTeX preview using KaTeX
6. Preview updates in real-time as user continues writing

**Input:**
- Stroke collection (from canvas)

**Output:**
- LaTeX string (e.g., `2x + 3 = 7`)
- Confidence score (0.0 - 1.0)
- Bounding box coordinates for recognized symbols

**Performance Requirements:**
- Recognition latency: ≤ 200ms (P95)
- Accuracy: ≥ 95% for middle/high school level expressions
- Supported symbols: Numbers, operators (+, -, ×, ÷), variables, exponents, fractions, roots, parentheses

**Error Handling:**
- E-010: Low confidence (< 0.7) → Highlight uncertain symbols in yellow
- E-011: Recognition failure → Show "Recognition failed" message, allow manual correction
- E-012: Unsupported symbol → Flag symbol, suggest manual input

**Acceptance Criteria:**
- ✓ LaTeX preview updates within 200ms
- ✓ Recognized expressions match user intent (95% accuracy)
- ✓ Preview rendering is mathematically correct
- ✓ Works offline (on-device iink SDK)

---

#### FR-HTR-002: Manual Correction Interface

**Description:** Users can manually correct misrecognized expressions.

**Functional Behavior:**
1. User taps on LaTeX preview
2. System shows correction dialog
3. User sees list of alternative symbol interpretations
4. User selects correct interpretation or enters custom LaTeX
5. System updates LaTeX string
6. Preview re-renders with corrected expression

**Correction Options:**
- Symbol alternatives (from iink SDK candidates)
- Custom LaTeX input field
- Delete symbol
- Re-recognize region

**Acceptance Criteria:**
- ✓ Correction dialog appears on tap
- ✓ Alternative symbols are relevant
- ✓ Custom LaTeX input validates and renders correctly
- ✓ Corrections are immediately reflected

---

### 3.4 AI Solution Analysis

#### FR-AI-001: Asynchronous Solution Submission

**Description:** User submits handwritten solution for AI analysis.

**Functional Behavior:**
1. User completes solution on canvas
2. User taps "Submit" button
3. System validates canvas (strokes exist)
4. System captures canvas as image (PNG, max 2MB)
5. System packages submission data (image, LaTeX, metadata)
6. System sends POST request to `/api/v1/submissions`
7. Server responds with 202 Accepted and submission_id
8. Client establishes WebSocket connection for real-time updates
9. System shows "Analyzing..." loading screen with progress indicators
10. Client receives status updates via WebSocket
11. When complete, system navigates to feedback screen

**Submission Payload:**
```json
{
  "user_id": "uuid",
  "problem_id": "uuid",
  "session_id": "uuid",
  "image_base64": "...",
  "recognized_latex": "2x + 3 = 7 \\\\ 2x = 4 \\\\ x = 3",
  "stroke_metadata": {
    "stroke_count": 42,
    "total_duration_ms": 35000,
    "canvas_size": {"width": 1080, "height": 1440}
  },
  "device_info": {
    "platform": "ios",
    "os_version": "17.4",
    "app_version": "1.0.0"
  }
}
```

**WebSocket Status Messages:**
```json
{"stage": "received", "timestamp": "..."}
{"stage": "preprocessed", "timestamp": "..."}
{"stage": "htr_done", "latex_preview": "...", "confidence": 0.96}
{"stage": "analysis_done", "result_id": "uuid"}
```

**Business Rules:**
- BL-030: Submission requires minimum 3 strokes
- BL-031: Image size must be ≤ 2MB
- BL-032: User can submit maximum 60 times per hour

**Error Handling:**
- E-020: Empty canvas → Show "Please write your solution" alert
- E-021: Image too large → Auto-compress, retry
- E-022: Network timeout → Save locally, retry when connected
- E-023: Server error (5xx) → Show error, allow retry

**Acceptance Criteria:**
- ✓ Submission accepted within 500ms (P99)
- ✓ WebSocket connection established successfully
- ✓ Status updates received in real-time
- ✓ Network errors handled gracefully
- ✓ Submission data is validated

---

#### FR-AI-002: Error Classification

**Description:** AI analyzes solution and classifies error type.

**Functional Behavior:**
1. Backend receives submission
2. Worker extracts LaTeX and image
3. Worker calls GPT-4o with problem + solution + image
4. GPT-4o analyzes each step
5. GPT-4o identifies error step and error type
6. GPT-4o returns structured analysis
7. System stores analysis in database
8. System sends result via WebSocket

**Error Classification Taxonomy:**

| Type | Subtype | Description | Example |
|------|---------|-------------|---------|
| Conceptual | Formula confusion | Wrong formula applied | Using area formula for perimeter |
| Conceptual | Rule misunderstanding | Incorrect rule application | Sign error in transposition |
| Procedural | Step omission | Missing step in procedure | Skipping factorization |
| Procedural | Incorrect sequence | Steps in wrong order | Solving before simplifying |
| Computational | Arithmetic error | Calculation mistake | 7 - 3 = 5 |
| Computational | Sign error | Wrong sign in calculation | -(-3) = -3 |
| Comprehension | Problem misinterpretation | Misunderstood question | Finding x instead of 2x |
| Comprehension | Variable confusion | Wrong variable used | Using a instead of b |

**Analysis Output Schema:**
```json
{
  "is_correct": false,
  "error_steps": [
    {
      "step_order": 2,
      "error_type": "procedural",
      "error_subtype": "sign_error",
      "description": "부호 변환이 올바르지 않습니다.",
      "correct_expression": "2x = 7 - 3"
    }
  ],
  "concept_understanding_summary": "일차방정식 이항 개념이 불명확합니다.",
  "feedback_message": "이항할 때는 부호를 바꿔야 해요...",
  "recommended_concept_tags": ["일차방정식", "이항"]
}
```

**Business Rules:**
- BL-040: Analysis timeout: 30 seconds max
- BL-041: Confidence threshold: ≥ 0.7 for classification
- BL-042: If ambiguous, mark for manual review

**Acceptance Criteria:**
- ✓ Error classification accuracy ≥ 90% vs teacher labels
- ✓ Analysis completes within 5 seconds (P95)
- ✓ Feedback message is grade-appropriate
- ✓ Analysis considers student's grade level

---

#### FR-AI-003: Personalized Feedback Generation

**Description:** Generate customized concept explanation based on error type and student level.

**Functional Behavior:**
1. System receives error classification
2. System retrieves student profile (grade, error history)
3. System queries misconception pattern database
4. If pattern match found (similarity > 0.7), use template
5. Else, invoke GPT-4o for custom explanation
6. System formats feedback with LaTeX rendering
7. System includes related concept links

**Feedback Components:**
- Error badge (color-coded by type)
- Explanation text (Korean, 300-500 characters)
- Related formula (LaTeX rendered)
- Example problem (similar but simpler)
- Action buttons (Try Again, Similar Problem, Learn More)

**Tone Adaptation:**
- Middle school: 친근한 반말 (informal, friendly)
- High school: 존댓말 (polite)
- User preference override available

**Acceptance Criteria:**
- ✓ Feedback is relevant to identified error
- ✓ Explanation matches student's grade level
- ✓ LaTeX formulas render correctly
- ✓ Tone is consistent with user preference

---

### 3.5 Problem Bank & Recommendation

#### FR-PROB-001: Personalized Problem Recommendation

**Description:** System recommends problems based on student's weak concepts and difficulty level.

**Functional Behavior:**
1. User opens app or navigates to "Problems" tab
2. System retrieves user's error history (last 30 days)
3. System calculates concept mastery scores
4. System identifies weak concepts (mastery < 0.6)
5. System queries problem bank with filters:
   - Grade level
   - Weak concepts (70% weight)
   - Strong concepts (30% weight for review)
   - Exclude recently solved (last 7 days)
6. System applies difficulty scaffolding:
   - If last 3 problems correct: increase difficulty
   - If last 2 problems incorrect: decrease difficulty
7. System returns recommended problem
8. User can tap "Next Problem" for alternatives

**Recommendation Algorithm:**
```python
def recommend_problem(user):
    weak_concepts = get_weak_concepts(user, threshold=0.6)
    strong_concepts = get_strong_concepts(user, threshold=0.8)

    # 70-30 mix
    concept_pool = (
        weighted_sample(weak_concepts, weight=0.7) +
        weighted_sample(strong_concepts, weight=0.3)
    )

    # Difficulty adjustment
    difficulty = adjust_difficulty(user.recent_performance)

    # Query problems
    candidates = Problem.query.filter(
        Problem.grade == user.grade,
        Problem.concept_tags.overlap(concept_pool),
        Problem.difficulty == difficulty,
        Problem.id.not_in(user.recent_problems)
    ).limit(10)

    # Re-rank by predicted success rate (0.5-0.7 zone)
    return rank_by_optimal_difficulty(candidates, user)
```

**Business Rules:**
- BL-050: Recommended difficulty targets 60-70% success rate
- BL-051: No problem repeats within 7 days
- BL-052: New users start at medium difficulty

**Acceptance Criteria:**
- ✓ Recommended problems match user's grade
- ✓ Weak concepts are prioritized
- ✓ Difficulty adapts to performance
- ✓ No duplicate problems in short term
- ✓ API responds within 1 second (P99)

---

#### FR-PROB-002: AI Similar Problem Generation

**Description:** Generate similar problem with same concept but different numbers.

**Functional Behavior:**
1. User completes a problem incorrectly
2. User taps "Similar Problem" button
3. System retrieves original problem data
4. System calls GPT-4o with generation prompt:
   ```
   Generate a similar problem to the following,
   keeping the same concept and difficulty but
   changing numbers and context:

   Original: {problem_text}
   Concept: {concept_tags}
   Grade: {grade}
   ```
5. GPT-4o returns new problem (text + LaTeX)
6. System validates problem (LaTeX parsable)
7. System generates correct answer using SymPy
8. System saves generated problem to database
9. System navigates user to new problem

**Generation Validation:**
- LaTeX syntax check
- SymPy symbolic parsing
- Solution existence check
- Concept tag consistency

**Business Rules:**
- BL-060: Generated problems marked as `source: llm_generated`
- BL-061: Generation fails after 3 retries → Show fallback problem
- BL-062: Generated problems reviewed periodically

**Acceptance Criteria:**
- ✓ Generated problem has same concept
- ✓ Numbers/context are different
- ✓ Difficulty level is consistent
- ✓ Problem is mathematically valid
- ✓ Generation completes within 5 seconds (P95)

---

### 3.6 Learning Management

#### FR-LEARN-001: Concept Mastery Tracking

**Description:** Track student's mastery of each concept based on repeated success.

**Functional Behavior:**
1. Student completes a problem correctly
2. System extracts concept tags from problem
3. For each concept:
   - Increment consecutive_correct count
   - Update mastery status
4. If consecutive_correct >= 3:
   - Set status to "mastered"
   - Schedule spaced repetition review
   - Show mastery badge animation
5. If student gets concept wrong:
   - Reset consecutive_correct to 0
   - Set status to "learning"

**Mastery States:**
- `learning`: 0-2 consecutive correct
- `mastered`: 3+ consecutive correct
- `review_due`: Mastered but review scheduled

**Spaced Repetition Schedule:**
| Review # | Interval |
|----------|----------|
| 1 | 1 day |
| 2 | 3 days |
| 3 | 7 days |
| 4 | 14 days |
| 5 | 30 days |

**Acceptance Criteria:**
- ✓ Mastery status updates correctly
- ✓ Badge animation shows on mastery
- ✓ Review schedule follows spaced repetition
- ✓ Wrong answer resets consecutive count

---

#### FR-LEARN-002: Automatic Wrong Answer Notebook

**Description:** Automatically collect and organize wrong answers for review.

**Functional Behavior:**
1. Student submits incorrect solution
2. System creates wrong answer entry:
   - Problem snapshot
   - Student's solution image
   - Error analysis
   - AI feedback
   - Timestamp
3. System tags entry with error type and concepts
4. User can access "Wrong Answer Notebook" from menu
5. User can filter by:
   - Date range
   - Error type
   - Concept
6. User can export as PDF or images

**Wrong Answer Entry Schema:**
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "problem": {
    "id": "uuid",
    "text": "...",
    "answer": "..."
  },
  "solution_image_url": "...",
  "error_analysis": {
    "error_type": "procedural",
    "error_subtype": "sign_error",
    "feedback": "..."
  },
  "solved_at": "ISO8601",
  "tags": ["일차방정식", "이항"]
}
```

**Acceptance Criteria:**
- ✓ Wrong answers are saved automatically
- ✓ Filtering works correctly
- ✓ Images display properly
- ✓ PDF export includes all relevant data

---

## 4. User Workflows

### 4.1 Core Learning Workflow

```
┌─────────────────────────────────────────────────────────┐
│ START: User opens app                                   │
└─────────┬───────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────┐
│ Home Dashboard                                          │
│ - Today's recommended problem                           │
│ - Learning streak                                       │
│ - Quick actions (Camera, Manual, Review)                │
└─────────┬───────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────┐
│ User selects "Today's Problem"                          │
└─────────┬───────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────┐
│ Problem Screen                                          │
│ - Problem statement (LaTeX rendered)                    │
│ - "Start Solving" button                                │
└─────────┬───────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────┐
│ Canvas Screen                                           │
│ - Pen input canvas (real-time recognition)             │
│ - LaTeX preview panel                                   │
│ - Toolbar (pen, eraser, undo/redo)                     │
│ - "Submit" button                                       │
└─────────┬───────────────────────────────────────────────┘
          │
          │ User writes solution
          │
          ▼
┌─────────────────────────────────────────────────────────┐
│ User taps "Submit"                                      │
└─────────┬───────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────┐
│ Analysis Loading Screen                                 │
│ - "Analyzing your solution..." message                  │
│ - Progress indicators (received, processing, done)      │
│ - WebSocket status updates                              │
└─────────┬───────────────────────────────────────────────┘
          │
          │ AI analysis completes (3-5 seconds)
          │
          ▼
┌─────────────────────────────────────────────────────────┐
│ Feedback Screen                                         │
│ - Correct/Incorrect badge                               │
│ - If incorrect:                                         │
│   - Error highlighting on solution image                │
│   - Error type badge                                    │
│   - Concept explanation card                            │
│   - TTS playback button                                 │
│   - Related formula display                             │
│ - Action buttons:                                       │
│   - "Try Again" (same problem)                          │
│   - "Similar Problem" (AI generated)                    │
│   - "Learn Concept" (detailed explanation)              │
│   - "Next Problem" (continue)                           │
└─────────┬───────────────────────────────────────────────┘
          │
          ├──► User taps "Similar Problem"
          │    │
          │    ▼
          │    Generate AI problem → Back to Canvas Screen
          │
          ├──► User taps "Learn Concept"
          │    │
          │    ▼
          │    Concept Detail Screen → Back to Feedback
          │
          └──► User taps "Next Problem"
               │
               ▼
               Return to Home Dashboard
```

---

## 5. Functional Dependencies

### 5.1 Feature Dependency Graph

```
Authentication (FR-AUTH)
    │
    ├──► User Profile (FR-AUTH-002)
    │       │
    │       └──► Grade-based Filtering (FR-PROB-001)
    │
    └──► Session Management
            │
            └──► All Authenticated Features

Canvas Input (FR-CANVAS)
    │
    ├──► Handwriting Recognition (FR-HTR)
    │       │
    │       └──► AI Analysis (FR-AI)
    │
    └──► Auto-save (FR-CANVAS-004)

Problem Bank (FR-PROB)
    │
    ├──► Recommendation Engine (FR-PROB-001)
    │       │
    │       └──► Concept Mastery (FR-LEARN-001)
    │
    └──► AI Generation (FR-PROB-002)
            │
            └──► GPT-4o API

AI Analysis (FR-AI)
    │
    ├──► Error Classification (FR-AI-002)
    │       │
    │       └──► Misconception Database
    │
    ├──► Feedback Generation (FR-AI-003)
    │       │
    │       └──► Learning History
    │
    └──► Concept Mastery Update (FR-LEARN-001)
```

---

## 6. Acceptance Criteria

### 6.1 Phase 1 Functional Completeness Checklist

#### Authentication & User Management
- [ ] User can register via Apple, Google, Kakao
- [ ] JWT tokens issued correctly (1h access, 30d refresh)
- [ ] User profile displays and updates correctly
- [ ] Session persists across app restarts

#### Pen Input Canvas
- [ ] Canvas renders at 60 FPS minimum
- [ ] Stylus and finger input both work
- [ ] Pressure sensitivity visible on compatible devices
- [ ] Undo/Redo works for 50 actions
- [ ] Auto-save triggers every 30 seconds
- [ ] Recovery prompt shows on app restart

#### Handwriting Recognition
- [ ] Real-time recognition within 200ms
- [ ] LaTeX preview renders correctly
- [ ] Recognition accuracy ≥ 95% on test set
- [ ] Manual correction interface works
- [ ] Fallback to MathPix on iink failure

#### AI Solution Analysis
- [ ] Submission accepted within 500ms (P99)
- [ ] WebSocket connection established
- [ ] Analysis completes within 5 seconds (P95)
- [ ] Error classification accuracy ≥ 90%
- [ ] Feedback is grade-appropriate

#### Problem Recommendation
- [ ] Recommended problems match user grade
- [ ] Weak concepts prioritized (70% weight)
- [ ] Difficulty adapts based on performance
- [ ] No duplicates within 7 days
- [ ] API responds within 1 second (P99)

#### Learning Management
- [ ] Concept mastery updates correctly
- [ ] Spaced repetition schedule accurate
- [ ] Wrong answer notebook saves entries
- [ ] Mastery badge shows on achievement

---

## 7. Traceability Matrix

| Requirement ID | Feature Name | PRD Section | Test Case ID | Implementation Status |
|---------------|--------------|-------------|--------------|----------------------|
| FR-AUTH-001 | Social Login | 4.8 | TC-AUTH-001 | ✅ Complete |
| FR-AUTH-002 | Profile Management | 4.8 | TC-AUTH-002 | ✅ Complete |
| FR-CANVAS-001 | Stylus Input | 4.1 | TC-CANVAS-001 | 🟡 In Progress |
| FR-CANVAS-002 | Tool Selection | 4.1 | TC-CANVAS-002 | 🟡 In Progress |
| FR-CANVAS-003 | Undo/Redo | 4.1 | TC-CANVAS-003 | 🟡 In Progress |
| FR-CANVAS-004 | Auto-save | 4.1 | TC-CANVAS-004 | 🟡 In Progress |
| FR-HTR-001 | Real-time Recognition | 4.2 | TC-HTR-001 | ⏳ Pending |
| FR-HTR-002 | Manual Correction | 4.2 | TC-HTR-002 | ⏳ Pending |
| FR-AI-001 | Async Submission | 4.3 | TC-AI-001 | ✅ Complete |
| FR-AI-002 | Error Classification | 4.3 | TC-AI-002 | ✅ Complete |
| FR-AI-003 | Feedback Generation | 4.3 | TC-AI-003 | ✅ Complete |
| FR-PROB-001 | Recommendation | 4.6 | TC-PROB-001 | ✅ Complete |
| FR-PROB-002 | AI Generation | 4.6 | TC-PROB-002 | ✅ Complete |
| FR-LEARN-001 | Concept Mastery | 4.5 | TC-LEARN-001 | ✅ Complete |
| FR-LEARN-002 | Wrong Answer Notebook | 4.5 | TC-LEARN-002 | ✅ Complete |

---

**Document Revision History:**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| v1.0 | 2026-05-22 | Dev Team | Initial functional design document |

---

*This document is for internal development use.*

*© 2026 MathLens AI Project. All rights reserved.*
