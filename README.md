# Job Search Agent

**An AI-assisted job discovery and qualification-matching application**

**Status:** In Development — Provider Evaluation Completed

## Overview

Job Search Agent is a Python-based application designed to help job seekers discover relevant employment opportunities, compare job requirements against their qualifications, and prioritize promising positions.

The application will combine structured job data from multiple providers with deterministic filtering and selective AI-assisted analysis.

The goal is to produce an actionable HTML report that helps job seekers focus their time on opportunities that best align with their experience and career objectives.

This project is also a portfolio demonstration of modern software development, API integration, AI-assisted analysis, solution architecture, and technical delivery practices.

## Project Objectives

- Aggregate job opportunities from multiple providers.
- Normalize different provider data formats into a consistent structure.
- Support searches based on role, location, compensation, and employment preferences.
- Identify duplicate and irrelevant postings.
- Evaluate candidate qualifications against job requirements.
- Explain relevant strengths and potential qualification gaps.
- Generate an actionable report with links to original job postings.
- Demonstrate a modular architecture suitable for future expansion.
- Control AI usage and operating costs through selective analysis.

## Planned V1 Workflow

1. Upload a resume in PDF or DOCX format.
2. Enter job search preferences.
3. Retrieve job postings from supported providers.
4. Normalize results into a common Job model.
5. Deduplicate and filter results.
6. Perform preliminary relevance matching.
7. Apply AI analysis to selected opportunities when appropriate.
8. Generate an HTML report containing job recommendations, match explanations, and application links.

**Note:** This workflow describes the intended V1 functionality. The complete application has not yet been implemented.

## Architecture

The application uses a provider-adapter architecture to isolate external job-source integrations from downstream processing.

```text
                  Job Search Request
                          |
                +---------+---------+
                |                   |
             Dice MCP          Adzuna REST
                |                   |
            DiceAdapter        AdzunaAdapter
                |                   |
                +---------+---------+
                          |
                  Normalized Job Model
                          |
                 Deduplication / Filters
                          |
                Preliminary Job Matching
                          |
                 Selective AI Analysis
                          |
                      Ranking
                          |
                     HTML Report
```

This architecture is intended to support independent provider integrations, consistent data validation, reusable matching logic, and future provider expansion.

## Job Data Providers

Three provider integrations were evaluated through standalone proofs of concept.

| Provider     | Integration | Evaluation                                                      | V1 Decision |
| ------------ | ----------- | --------------------------------------------------------------- | ----------- |
| Dice         | MCP         | Successful job search, full descriptions, structured skills     | Selected    |
| Adzuna       | REST API    | Successful job discovery, filtering, and application navigation | Selected    |
| ZipRecruiter | MCP         | Session initialization succeeded; reliable job retrieval failed | Deferred    |

### Dice MCP

Dice provides job search functionality, detailed job descriptions, structured skills, and additional job metadata.

It is the preferred V1 provider for detailed AI-assisted qualification matching.

### Adzuna REST API

Adzuna provides structured job listings, geographic and recency filters, salary information, and application links.

It will complement Dice by expanding job discovery coverage.

**Known limitation:** The tested API responses provided approximately 500-character description snippets, restricting comprehensive qualification analysis.

### ZipRecruiter MCP

ZipRecruiter was evaluated but deferred because the integration could not reliably retrieve job listings.

The evaluation included independent testing with MCP Inspector.

## Technology Stack

| Area                       | Technology                    |
| -------------------------- | ----------------------------- |
| Programming language       | Python                        |
| Development environment    | VS Code, PowerShell           |
| Dependency management      | uv                            |
| MCP integration            | Python MCP SDK                |
| REST integration           | requests                      |
| Local configuration        | python-dotenv                 |
| Data modeling (planned)    | Pydantic V2                   |
| Unit testing (planned)     | pytest                        |
| AI analysis (planned)      | LLM integration, provider TBD |
| Reporting (planned)        | HTML                          |
| Cloud deployment (planned) | AWS                           |
| Version control            | Git and GitHub                |
| Project management         | Jira                          |

## Current Development Status

### Completed

- [x] Initial project scope and V1 workflow defined.
- [x] Local Python development environment configured.
- [x] Dice MCP proof of concept completed.
- [x] ZipRecruiter MCP proof of concept completed and deferred.
- [x] Adzuna REST API proof of concept completed.
- [x] Provider filtering and job metadata evaluated.
- [x] Adzuna application links manually validated.
- [x] Provider selection documented in ADR-001.
- [x] Initial project notes and spike documentation created.

### Planned / In Progress

- [ ] Define normalized Job data model.
- [ ] Implement Pydantic validation and unit tests.
- [ ] Implement Dice and Adzuna provider adapters.
- [ ] Implement duplicate detection and relevance filtering.
- [ ] Implement resume ingestion.
- [ ] Implement deterministic and AI-assisted qualification matching.
- [ ] Generate HTML reports.
- [ ] Validate production usage requirements.
- [ ] Deploy a working V1 application to AWS.

## Repository Structure

Current and planned directories:

```text
job-search-agent/
├── docs/
│   └── adr/
│       └── 001-job-source-evaluation.md
├── spikes/
│   ├── adzuna/
│   ├── dice/
│   ├── ziprecruiter/
├── src/                       # Planned application code
├── tests/                     # Planned unit tests
├── output/                    # Local output, Git-ignored
├── .env                       # Local credentials, Git-ignored
├── .gitignore
├── pyproject.toml
├── project-notes.md
└── README.md
```

The repository structure will evolve as implementation progresses.

## Local Development

### Prerequisites

- Python
- uv
- Git
- Valid credentials for providers that require authentication

### Install Dependencies

From the repository root:

```powershell
uv sync
```

### Configure Adzuna

Create a `.env` file in the repository root:

```dotenv
ADZUNA_APP_ID=your_app_id
ADZUNA_APP_KEY=your_app_key
```

Never commit API credentials to Git.

### Run Provider Proofs of Concept

Dice:

```powershell
uv run python spikes/dice/dice_poc.py
```

Adzuna:

```powershell
uv run python spikes/adzuna/adzuna_poc.py
```

Refer to each spike's README for additional requirements, instructions, and limitations.

The full application does not yet have a production entry point.

## Architecture Decisions and Documentation

- [ADR-001 — Job Source Integration Evaluation](docs/adr/001-job-source-evaluation.md)
- [Project Notes](project-notes.md)
- [Dice MCP Spike](spikes/dice/README.md)
- [ZipRecruiter MCP Spike](spikes/ziprecruiter/README.md)
- [Adzuna REST Spike](spikes/adzuna/README.md)

These documents provide additional information about technical experiments, architectural trade-offs, and implementation decisions.

## Design Principles

**Modularity:** External provider logic should remain separate from business logic.

**Data quality:** Provider data should be normalized and validated before downstream processing.

**Explainability:** Matching results should provide understandable reasoning rather than unexplained scores.

**Cost awareness:** Deterministic filtering should reduce unnecessary AI processing.

**Graceful handling of incomplete data:** Missing fields and truncated descriptions should not be treated as complete information.

**Security:** API credentials must not be committed to source control.

**Incremental delivery:** Features should be implemented and tested in manageable increments.

## Known Limitations

- Only provider-level POCs have been completed.
- The complete job-search and matching workflow is not yet operational.
- Adzuna API descriptions may be truncated.
- Job-provider results can contain irrelevant or duplicate listings.
- Salary information may be incomplete or predicted.
- Provider rate limits, production usage terms, and cloud deployment compatibility require additional validation.
- Automated AI matching has not yet been implemented.

## Roadmap

**Phase 1 — Provider Feasibility:** Completed

Evaluate job data providers and select viable V1 integrations.

**Phase 2 — Core Data Architecture:** Next

Implement the normalized Job model, validation, and provider adapters.

**Phase 3 — Job Processing**

Implement deduplication, filtering, and preliminary matching.

**Phase 4 — AI and Reporting**

Implement resume processing, selective AI-assisted analysis, and HTML reporting.

**Phase 5 — Deployment**

Validate the end-to-end workflow, complete security and provider compliance checks, and deploy the application to AWS.

## Project Approach

Development follows an iterative approach supported by Jira, technical spikes, Architecture Decision Records, unit testing, and Git version control.

The project emphasizes validating integration feasibility before making architectural commitments.

It is being developed as both a functional application and a demonstration of technical project delivery, software architecture, and applied AI capabilities.

---

**Project status:** Active development  
**Last updated:** October 13, 2026
