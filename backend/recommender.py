from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from math import log1p


@dataclass(frozen=True)
class CandidateProfile:
    target_titles: tuple[str, ...]
    skills: tuple[str, ...]
    preferred_locations: tuple[str, ...] = ()
    remote_ok: bool = True


@dataclass(frozen=True)
class JobItem:
    id: str
    title: str
    company: str
    location: str
    skills: tuple[str, ...]
    posted_days_ago: int
    description: str


@dataclass(frozen=True)
class Recommendation:
    job: JobItem
    score: float
    matched_skills: tuple[str, ...]
    missing_skills: tuple[str, ...]
    reasons: tuple[str, ...]


def _tokens(values: tuple[str, ...] | list[str]) -> set[str]:
    return {value.strip().lower() for value in values if value.strip()}


def _title_score(profile: CandidateProfile, job: JobItem) -> float:
    title = job.title.lower()
    matches = sum(1 for target in profile.target_titles if target.lower() in title)
    return min(matches / max(len(profile.target_titles), 1), 1.0)


def _location_score(profile: CandidateProfile, job: JobItem) -> float:
    job_location = job.location.lower()
    if profile.remote_ok and "remote" in job_location:
        return 1.0
    if not profile.preferred_locations:
        return 0.5
    return 1.0 if any(location.lower() in job_location for location in profile.preferred_locations) else 0.0


def score_job(profile: CandidateProfile, job: JobItem) -> Recommendation:
    profile_skills = _tokens(profile.skills)
    job_skills = _tokens(job.skills)
    matched = tuple(sorted(profile_skills & job_skills))
    missing = tuple(sorted(job_skills - profile_skills))

    skill_score = len(matched) / max(len(job_skills), 1)
    title_score = _title_score(profile, job)
    location_score = _location_score(profile, job)
    recency_score = 1 / log1p(max(job.posted_days_ago, 1) + 1)

    score = (
        0.55 * skill_score
        + 0.20 * title_score
        + 0.15 * location_score
        + 0.10 * recency_score
    )

    reasons = [
        f"matched {len(matched)} of {len(job_skills)} target skills",
        f"title alignment {title_score:.0%}",
        f"location alignment {location_score:.0%}",
        f"posted {job.posted_days_ago} days ago",
    ]

    return Recommendation(
        job=job,
        score=round(score, 4),
        matched_skills=matched,
        missing_skills=missing,
        reasons=tuple(reasons),
    )


def recommend(profile: CandidateProfile, jobs: list[JobItem], limit: int = 5) -> list[Recommendation]:
    scored = [score_job(profile, job) for job in jobs]
    return sorted(scored, key=lambda item: item.score, reverse=True)[:limit]


def sample_jobs(today: date | None = None) -> list[JobItem]:
    _ = today or date.today()
    return [
        JobItem(
            id="backend-ai-intern",
            title="Backend AI Engineering Intern",
            company="Northstar Labs",
            location="Remote US",
            skills=("Python", "FastAPI", "Redis", "RAG", "PostgreSQL"),
            posted_days_ago=3,
            description="Build retrieval-backed AI services and evaluation workflows.",
        ),
        JobItem(
            id="mobile-ai-intern",
            title="iOS AI Product Engineer Intern",
            company="FocusWorks",
            location="San Jose, CA",
            skills=("SwiftUI", "DeviceActivity", "LLM", "Privacy"),
            posted_days_ago=6,
            description="Prototype privacy-aware AI companion features for mobile users.",
        ),
        JobItem(
            id="data-platform-intern",
            title="Data Platform Intern",
            company="LedgerFrame",
            location="New York, NY",
            skills=("Python", "SQL", "Airflow", "dbt"),
            posted_days_ago=12,
            description="Improve financial data pipelines and reporting reliability.",
        ),
    ]

