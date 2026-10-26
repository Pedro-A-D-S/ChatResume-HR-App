"""Domain entities, value objects, and repository interfaces for HR Multi-Agent Platform."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum


class CandidateStatus(str, Enum):
    NEW = "NEW"
    SCREENED = "SCREENED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    FLAGGED_SECURITY = "FLAGGED_SECURITY"


@dataclass(frozen=True)
class PIIEntity:
    entity_type: str
    original_value: str
    redacted_placeholder: str


@dataclass
class CandidateResume:
    candidate_id: str
    raw_text: str
    sanitized_text: str
    detected_pii: list[PIIEntity] = field(default_factory=list)
    has_injection_risk: bool = False
    security_flags: list[str] = field(default_factory=list)
    uploaded_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass
class EvaluationRubric:
    role_title: str
    seniority: str
    required_skills: list[str]
    nice_to_have_skills: list[str]
    min_years_experience: int
    rubric_id: str = "MLOPS-SR-2026"


@dataclass
class JudgeVerdict:
    is_faithful_to_resume: bool
    hallucination_detected: bool
    hallucination_details: str | None
    bias_score: float  # 0.0 to 1.0 (0 = clean, 1 = biased)
    confidence: float
    verdict_summary: str
    audited_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass
class CandidateEvaluation:
    candidate_id: str
    rubric_id: str
    matched_skills: list[str]
    missing_skills: list[str]
    years_experience_detected: float
    fit_score: float  # 0.0 to 100.0
    synthesis: str
    judge_verdict: JudgeVerdict | None = None
    evaluated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
