# ADR-001: Job Source Integration Evaluation

- Status: Proposed

## Context

The Job Search Agent requires reliable programmatic access to current job postings. Candidate providers include Dice, ZipRecruiter, and Adzuna.

## Decision

Build small provider spikes before selecting the initial production source:

- Dice — MCP
- ZipRecruiter — MCP
- Adzuna — REST API
  Evaluate each for:
- integration complexity
- search quality
- description completeness
- metadata quality
- URLs
- filtering
- reliability
- cloud compatibility

## Decision outcome

### Dice POC Findings

Dice MCP provides structured skills for individual job postings in addition
to the full job description.

This enables a two-stage matching approach:

1. Use deterministic Python logic for preliminary filtering and skills matching.
2. Use the AI model only for shortlisted jobs requiring semantic analysis,
   match rationale, gap analysis, and final ranking.

This approach may reduce LLM calls, token consumption, latency, and operating
cost while keeping deterministic filtering explainable and testable.

Final matching architecture remains pending evaluation of the other job providers.
