# JobFit AI Architecture

This document tracks the intended architecture for the JobFit AI portfolio project.

## Design Principles

- Recommendation first, LLM second: ranking quality should not depend entirely on a chat model.
- Human-in-the-loop: the system recommends and explains, but does not submit applications.
- Measured claims only: resume and README metrics should come from reproducible eval scripts.
- State over one-off prompts: recommendation runs should be persisted and comparable.

## Planned Data Model

- `users`: candidate profile, target roles, location preferences, seniority, and skill graph.
- `items`: jobs, courses, projects, or learning resources.
- `events`: saves, clicks, skips, applications, interviews, and feedback.
- `recommendation_runs`: model version, input snapshot, candidates, scores, and explanations.

## Pipeline

1. Ingest and normalize items.
2. Extract structured features and embeddings.
3. Generate candidates from multiple retrieval strategies.
4. Rank candidates with structured features.
5. Generate explanations and skill-gap analysis.
6. Persist run state for review and iteration.

## Open Questions

- Which public or synthetic dataset should be used for the first measurable benchmark?
- Should the first UI be a landing page only, or a small review dashboard?
- Which features belong in the LightGBM ranker versus the LLM explanation layer?
