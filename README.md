# JobFit AI

Career intelligence and recommendation pipeline for matching candidates with high-fit jobs and learning content.

## Business Problem

Job seekers often collect many job posts, courses, resume versions, and application notes, but the hard part is deciding where to focus. JobFit AI treats career search as a recommendation problem: given a candidate profile, behavior history, target roles, and a catalog of jobs or learning resources, the system retrieves, ranks, and explains the best next opportunities.

The goal is not to auto-apply. The goal is to help a human make better decisions with transparent recommendation evidence.

## Product Loop

1. Ingest jobs and learning content.
2. Build candidate and item features from resumes, skills, behavior signals, and metadata.
3. Generate candidate recommendations with retrieval models.
4. Rank recommendations with structured features and behavioral signals.
5. Use an LLM reasoning layer to explain fit, skill gaps, and resume focus.
6. Save recommendation state so results can be reviewed, compared, and improved over time.

## System Design

```text
job/content sources
        |
        v
ingestion pipeline
        |
        v
PostgreSQL metadata + Redis cache
        |
        v
candidate generation
  - popularity
  - item-based collaborative filtering
  - two-tower neural retrieval
  - FAISS ANN search
        |
        v
ranking layer
  - LightGBM
  - user-item match features
  - behavior signals
  - recency
  - embedding similarity
        |
        v
LLM reasoning layer
  - recommendation explanation
  - skill-gap analysis
  - resume/project focus suggestions
        |
        v
human review dashboard / report
```

## Agentic Pipeline Design

JobFit AI is designed as a multi-stage, human-in-the-loop pipeline. Each stage has a narrow responsibility and writes state that later stages can reuse.

| Stage | Responsibility |
| --- | --- |
| Ingestion worker | Normalize jobs, learning resources, and profile inputs. |
| Feature worker | Extract skills, seniority, domain, location, recency, and behavior features. |
| Retrieval worker | Generate candidates with popularity, ItemCF, two-tower embeddings, and FAISS. |
| Ranker worker | Score candidates with LightGBM and structured user-item features. |
| Explanation agent | Produce fit explanations, missing skills, and next learning steps. |
| Tracker worker | Persist recommendation state and avoid duplicate scoring. |

The model can recommend and explain, but final application decisions stay with the user.

## Core Features

- Local deterministic recommendation smoke test for validating profile-job scoring behavior.
- Personalized job recommendation from a job/content catalog.
- Learning-content recommendation for skill gaps.
- Multi-stage candidate generation.
- Two-tower neural retrieval with negative sampling and contrastive learning.
- FAISS approximate nearest-neighbor search for low-latency retrieval.
- LightGBM ranking with profile, behavior, recency, and embedding similarity features.
- LLM-based explanation and skill-gap analysis.
- Redis caching for expensive recommendation and LLM reasoning contexts.

## Tech Stack

- Python
- PyTorch
- FastAPI
- PostgreSQL
- Redis
- FAISS
- LightGBM
- Docker
- OpenAI API

## Evaluation Plan

The project should report only measured metrics. Planned evaluation includes:

- Recall@50 for retrieval quality.
- NDCG@10 for ranking quality.
- AUC for ranker discrimination.
- p50 / p95 retrieval latency with and without FAISS.
- Redis cache hit rate for repeated recommendation sessions.
- LLM explanation quality checks against unsupported-claim rules.

## Repository Map

```text
jobfit-ai/
├── backend/      # Recommendation primitives and future FastAPI services
├── docs/         # Architecture, data contract, and design notes
├── evals/        # Offline metrics, benchmark scripts, and smoke checks
├── landing/      # Portfolio landing page
└── README.md
```

## Local Smoke Test

The current runnable slice is a deterministic profile-job recommender. It does
not require external services or API keys:

```sh
python3 evals/smoke_recommendations.py
```

The script prints ranked jobs, matched skills, missing skills, and short reasons
for each score. It is intentionally small so later FAISS, LightGBM, and LLM
layers can be compared against a stable baseline.

## MVP Roadmap

### Phase 1: Recommendation Core

- Define job, learning item, and user profile schemas.
- Build synthetic or public sample data for local development.
- Implement popularity and ItemCF baselines.
- Add FAISS retrieval over item embeddings.
- Expose recommendation API with FastAPI.

### Phase 2: Ranking and Metrics

- Add two-tower retrieval training.
- Add LightGBM ranker features.
- Report Recall@50, NDCG@10, AUC, and latency.
- Persist recommendation runs in PostgreSQL.

### Phase 3: LLM Reasoning Layer

- Generate recommendation explanations.
- Generate skill-gap and learning-plan summaries.
- Cache LLM reasoning contexts with Redis.
- Add guardrails to avoid unsupported resume or project claims.

### Phase 4: Portfolio Polish

- Build landing page.
- Add architecture diagram.
- Add demo screenshots or a short walkthrough video.
- Publish measured results and trade-off notes.

## Interview Narrative

JobFit AI demonstrates search and recommendation engineering beyond a toy model. It combines retrieval, ranking, feature design, backend APIs, caching, and LLM reasoning into a product-shaped system where the user stays in control of final career decisions.
