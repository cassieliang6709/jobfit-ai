from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from backend.recommender import CandidateProfile, recommend, sample_jobs


def main() -> None:
    profile = CandidateProfile(
        target_titles=("Backend", "AI", "Recommendation"),
        skills=("Python", "FastAPI", "Redis", "RAG", "PostgreSQL", "SwiftUI"),
        preferred_locations=("San Jose",),
        remote_ok=True,
    )

    results = recommend(profile, sample_jobs(), limit=3)

    print("JobFit AI smoke recommendations")
    for rank, rec in enumerate(results, start=1):
        matched = ", ".join(rec.matched_skills) or "none"
        missing = ", ".join(rec.missing_skills) or "none"
        print(f"{rank}. {rec.job.title} @ {rec.job.company} — score={rec.score:.4f}")
        print(f"   matched: {matched}")
        print(f"   missing: {missing}")
        print(f"   why: {'; '.join(rec.reasons)}")


if __name__ == "__main__":
    main()
