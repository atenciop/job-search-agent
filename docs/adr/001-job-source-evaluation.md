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

Pending POC results.
