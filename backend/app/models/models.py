import uuid
from datetime import datetime
from typing import Optional, List
from sqlalchemy import (
    String, Integer, Float, Boolean, Text, DateTime,
    ForeignKey, SmallInteger, JSON
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


def new_uuid() -> str:
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    email: Mapped[Optional[str]] = mapped_column(String(255), unique=True, nullable=True)
    hashed_password: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    display_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    grade: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    daily_goal: Mapped[int] = mapped_column(Integer, default=5)
    auth_provider: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # local|google|apple|kakao
    social_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_active_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    submissions: Mapped[List["Submission"]] = relationship("Submission", back_populates="user")
    problem_history: Mapped[List["UserProblemHistory"]] = relationship("UserProblemHistory", back_populates="user")
    mastery: Mapped[List["ConceptMastery"]] = relationship("ConceptMastery", back_populates="user")


class Concept(Base):
    __tablename__ = "concepts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    name: Mapped[str] = mapped_column(String(200))
    subject: Mapped[str] = mapped_column(String(50))   # algebra|geometry|calculus|statistics
    grade: Mapped[str] = mapped_column(String(20))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    formula: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    prerequisites: Mapped[Optional[dict]] = mapped_column(JSON, default=list)
    related_concepts: Mapped[Optional[dict]] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Problem(Base):
    __tablename__ = "problems"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    title: Mapped[str] = mapped_column(String(500))
    content_text: Mapped[str] = mapped_column(Text)
    content_image_key: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    answer_latex: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    solution_steps: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    subject: Mapped[str] = mapped_column(String(50))
    grade: Mapped[str] = mapped_column(String(20))
    difficulty: Mapped[int] = mapped_column(SmallInteger, default=3)  # 1~5
    concept_tags: Mapped[Optional[dict]] = mapped_column(JSON, default=list)
    error_type_tags: Mapped[Optional[dict]] = mapped_column(JSON, default=list)
    curriculum_code: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    source: Mapped[str] = mapped_column(String(20), default="bank")  # bank|llm_generated|textbook
    status: Mapped[str] = mapped_column(String(20), default="active")  # draft|review|active|archived
    estimated_solve_time_min: Mapped[int] = mapped_column(Integer, default=5)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    submissions: Mapped[List["Submission"]] = relationship("Submission", back_populates="problem")


class Submission(Base):
    __tablename__ = "submissions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))
    problem_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("problems.id"), nullable=True)
    session_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    image_s3_key: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    stroke_metadata: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    device_info: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="received")  # received|processing|completed|failed
    submitted_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    processed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="submissions")
    problem: Mapped[Optional["Problem"]] = relationship("Problem", back_populates="submissions")
    recognition_result: Mapped[Optional["RecognitionResult"]] = relationship(
        "RecognitionResult", back_populates="submission", uselist=False
    )


class RecognitionResult(Base):
    __tablename__ = "recognition_results"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    submission_id: Mapped[str] = mapped_column(String(36), ForeignKey("submissions.id"), unique=True)
    htr_raw_latex: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    htr_steps: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    htr_confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    is_correct: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    error_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # conceptual|procedural|computational|comprehension
    error_subtype: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    error_step: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    error_steps: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    feedback_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    concept_explanation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    correct_solution_latex: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    concept_tags_inferred: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    llm_model_version: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    processing_time_ms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    submission: Mapped["Submission"] = relationship("Submission", back_populates="recognition_result")


class ConceptMastery(Base):
    __tablename__ = "concept_mastery"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))
    concept_id: Mapped[str] = mapped_column(String(36))
    status: Mapped[str] = mapped_column(String(20), default="learning")  # learning|mastered|review_due
    consecutive_correct: Mapped[int] = mapped_column(SmallInteger, default=0)
    correct_count: Mapped[int] = mapped_column(Integer, default=0)
    total_count: Mapped[int] = mapped_column(Integer, default=0)
    next_review_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user: Mapped["User"] = relationship("User", back_populates="mastery")


class UserProblemHistory(Base):
    __tablename__ = "user_problem_history"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))
    problem_id: Mapped[str] = mapped_column(String(36), ForeignKey("problems.id"))
    submission_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("submissions.id"), nullable=True)
    is_correct: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    error_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    solved_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship("User", back_populates="problem_history")
