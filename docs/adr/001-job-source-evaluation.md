# ADR-001: Job Source Integration Evaluation

- **Status:** Accepted
- **Date:** 2026-10-09
- **Project:** Job Search Agent
- **Decision:** Select Dice MCP and Adzuna REST API as the initial job-data providers for V1.

## 1. Context

The Job Search Agent requires reliable programmatic access to current job postings from external providers.

The application is intended to:

- Retrieve job opportunities from multiple sources.
- Normalize provider-specific data into a common job model.
- Identify and remove duplicate listings.
- Apply user-defined search and relevance filters.
- Evaluate job/resume fit using deterministic logic and AI.
- Explain candidate strengths, qualification gaps, and match rationale.
- Generate an HTML report containing ranked opportunities and application links.

Before incorporating providers into the application, standalone proof-of-concept (POC) implementations were developed to validate actual integration behavior.

The initial providers evaluated were:

- Dice — Model Context Protocol (MCP)
- ZipRecruiter — MCP
- Adzuna — REST API

USAJOBS and other job APIs were identified as possible alternatives but were not evaluated through completed POCs.

An additional project objective is to demonstrate both MCP and conventional REST API integration in a professional portfolio application.

## 2. Decision Drivers

Providers were evaluated against the following criteria:

- Reliability and successful job retrieval
- Integration complexity
- Search quality and relevance
- Coverage of U.S. technology and project/delivery management positions
- Job-description completeness
- Availability of structured job metadata
- Job URLs and application navigation
- Search filtering capabilities
- Authentication requirements
- Rate limits and usage restrictions
- Suitability for AI-based job/resume matching
- Local development feasibility
- Future cloud deployment compatibility
- Portfolio demonstration and learning value

Actual POC results were prioritized over documented capabilities alone.

## 3. Provider Evaluation

### 3.1 Dice MCP

**POC Result: PASS**

Dice provides an MCP endpoint accessible through the Python MCP SDK.

The POC successfully demonstrated:

- MCP session initialization and tool discovery.
- Job searches using `search_jobs`.
- Retrieval of full job details using `get_job_details`.
- Access to company information through `get_company`.
- Server-side search filtering and sorting.
- Structured job metadata and job URLs.
- Structured skills associated with individual job postings.

**Strengths**

- Full job descriptions support detailed AI-assisted qualification analysis.
- Structured skills support deterministic preliminary matching.
- MCP integration provides a useful example of an emerging integration architecture.
- Full details can be retrieved selectively for shortlisted jobs, potentially reducing API calls and AI token consumption.

**Limitations**

- Full descriptions contain HTML and require appropriate text processing.
- Salary information is not consistently normalized.
- Results can contain adjacent roles and potential duplicates.
- Remote positions may appear in geographically constrained searches.
- Dice requires disclosure of AI assistance when presenting results.
- Cloud deployment feasibility has not yet been established.

**Conclusion**

Dice is the preferred V1 provider for detailed job information and AI-assisted resume matching.

### 3.2 ZipRecruiter MCP

**POC Result: DEFER**

ZipRecruiter provides an MCP endpoint at:

`https://api.ziprecruiter.com/mcp`

Its documentation describes a `search_jobs` tool supporting keywords, location, radius, country, salary, recency, workplace type, employment type, and seniority filters.

A standalone Python MCP client was implemented.

**Successful Tests**

- Communication with the endpoint was established.
- MCP sessions initialized successfully during multiple test runs.
- Protocol version `2025-11-25` was negotiated.
- Server identification was returned:
  - Name: `jobseeker-mcp`
  - Version: `1.0.0`
- The server advertised Tools and Resources capabilities.

**Problems Observed**

Reliable job retrieval could not be demonstrated.

Observed failures included:

- `tools/list` returning MCP error `-32603`.
- `resources/list` returning MCP error `-32603`.
- Direct `tools/call` of `search_jobs` returning MCP error `-32603`.
- Intermittent MCP initialization failures.
- Earlier HTTP 409 responses.
- HTTP 429 Too Many Requests when testing independently with MCP Inspector.

The independent Inspector test provided additional evidence that the problems were not limited to the Python implementation.

Separate ZipRecruiter documentation confirms rate limiting for its Embedded Sponsorship API, but those limits cannot be assumed to apply to the Job Search MCP endpoint.

**Conclusion**

ZipRecruiter is deferred from V1 because the POC did not establish sufficiently reliable end-to-end job retrieval.

It may be reevaluated if endpoint reliability, access requirements, or integration documentation improves.

### 3.3 Adzuna REST API

**POC Result: PASS — With Limitations**

Adzuna provides a conventional REST API for job discovery.

The POC used:

`GET https://api.adzuna.com/v1/api/jobs/us/search/1`

Authentication was implemented using `app_id` and `app_key`, stored locally in environment configuration excluded from Git.

Python `requests` was used to make HTTP requests and process JSON responses.

**Successful Tests**

- API authentication and connectivity returned HTTP 200.
- The initial Nashville Technical Project Manager search reported 294 matching jobs.
- Structured JSON responses included job IDs, titles, companies, locations, posting dates, description snippets, salary fields, categories, and redirect URLs.
- Seven-day recency filtering returned 58 matches, with all 10 inspected postings dated today or yesterday.
- An Atlanta geographic search returned 111 matches, with inspected jobs located in the Atlanta area.
- Full-time filtering produced results consistent with the requested employment type during spot checks.
- A $120,000 salary filter reduced the Nashville result count from 57 to 27.
- Job listing URLs opened successfully.
- Complete job descriptions were available on Adzuna's website.
- Apply buttons navigated to employer or recruiter application pages.

The POC also demonstrated practical usefulness: retrieved listings were used to identify job opportunities and submit actual applications.

**Strengths**

- Straightforward REST integration using standard Python libraries.
- Useful structured metadata.
- Effective recency and geographic filtering.
- Support for employment-type and salary search criteria.
- Working links to complete job listings and application pages.
- Complementary job discovery coverage.

**Limitations**

- All ten initial API description samples were truncated to approximately 500 characters.
- Complete descriptions were not available through the tested API response.
- Some search results were not closely relevant to Technical Project Management.
- Salary filters may include jobs whose ranges overlap the requested threshold rather than requiring the lower bound to meet it.
- Salary information may be predicted and must be labeled appropriately.
- Similar listings may represent either duplicates or distinct openings.
- Geographic location alone does not reliably identify remote, hybrid, or on-site work.
- Adzuna pages may present optional email-alert signup prompts before displaying listings.

**Conclusion**

Adzuna is suitable as a complementary V1 job-discovery provider.

Its description limitations make it less suitable than Dice for comprehensive AI-based resume/job matching.

Adzuna results should therefore support preliminary relevance assessment and navigation to complete job postings.

## 4. Decision

**Select Dice MCP and Adzuna REST API as the initial Job Search Agent V1 providers.**

The providers will have complementary responsibilities:

| Provider         | V1 Responsibility                                                                               |
| ---------------- | ----------------------------------------------------------------------------------------------- |
| Dice MCP         | Rich job data, structured skills, detailed AI-assisted matching                                 |
| Adzuna REST      | Additional job discovery, search filtering, preliminary relevance assessment, application links |
| ZipRecruiter MCP | Deferred from V1                                                                                |

The application will distinguish between assessments based on full job descriptions and assessments based only on limited description snippets.

ZipRecruiter will not be a required dependency for V1.

## 5. Proposed Integration Architecture

The application will use provider-specific adapters that normalize external data into a common job representation.

```text
                 Job Search Agent
                         |
                  Job Search Request
                         |
             +-----------+-----------+
             |                       |
         Dice MCP                Adzuna REST
             |                       |
        DiceAdapter             AdzunaAdapter
             |                       |
             +-----------+-----------+
                         |
                 Normalized Job Model
                         |
                Deduplication / Filters
                         |
              Preliminary Relevance Match
                         |
                 AI Analysis (as needed)
                         |
                    Job Ranking
                         |
                    HTML Report
```

The normalized job model should preserve, where available:

- Provider name and provider-specific job ID
- Job title and company
- Location and work arrangement
- Posting date
- Job description and completeness indicator
- Structured skills
- Salary range and prediction indicator
- Source URL
- Employment type
- Relevant job categories

Provider-specific adapters will isolate integration details from downstream application logic.

The detailed adapter interface and data-model design will be addressed during implementation and may be documented in a separate ADR if architectural trade-offs require it.

## 6. Matching Strategy

A two-stage matching approach is preferred.

**Stage 1 — Deterministic Filtering**

Use Python logic to:

- Apply user-defined search constraints.
- Remove obviously irrelevant positions.
- Identify potential duplicates.
- Compare available structured skills and metadata.
- Shortlist promising opportunities.

**Stage 2 — AI-Assisted Analysis**

Use AI selectively for shortlisted jobs to:

- Evaluate semantic alignment between the resume and job requirements.
- Explain strengths and qualification gaps.
- Produce a match rationale.
- Support final ranking.

Detailed AI matching should use complete job descriptions when available.

For Adzuna listings with truncated descriptions, the application should identify the assessment as preliminary rather than presenting it as comprehensive.

This approach is intended to control LLM token consumption, latency, and operating cost while maintaining explainability.

The precise matching algorithm and scoring methodology remain implementation decisions.

## 7. Consequences

### Positive

- V1 has two providers with demonstrated local job retrieval.
- The portfolio demonstrates both MCP and REST API integration.
- Dice provides richer data for detailed AI matching.
- Adzuna expands job discovery coverage.
- Provider-specific integration logic can be isolated behind adapters.
- Additional providers can be introduced incrementally.
- The application avoids depending on an MCP endpoint that could not reliably retrieve jobs.
- The decision is supported by reproducible POCs and observed results.
- Adzuna has already demonstrated practical value through actual job applications.

### Negative / Trade-offs

- Two integration mechanisms increase implementation and testing complexity.
- Provider responses differ in completeness and metadata quality.
- Adzuna's truncated descriptions limit automated fit analysis.
- Duplicate detection across providers will require additional logic.
- Salary and work-arrangement information may require normalization and qualification.
- Provider availability and reliability may vary independently.
- The application must communicate different levels of match confidence.
- V1 job coverage will not include ZipRecruiter.

## 8. Risks and Outstanding Validation

The POCs establish local technical feasibility, not production readiness.

The following require further validation:

- Cloud connectivity and deployment compatibility
- Provider API quotas and usage limits
- Authentication and secret management in production
- Applicable API terms, attribution, and redistribution requirements
- Reliability under repeated searches
- Pagination and larger result sets
- Cross-provider duplicate detection
- Error handling, timeouts, retries, and backoff
- Data normalization and validation
- AI matching quality and operating cost
- User-facing disclosure of AI-assisted analysis

These concerns should be addressed before public production deployment.

## 9. Deferred Work

- ZipRecruiter MCP integration
- Indeed integration pending a suitable officially supported access path
- Additional REST API providers, including USAJOBS
- Provider health monitoring and failover
- Advanced retry and rate-limit management
- Scheduled job retrieval
- Automated full-description acquisition from other sources unless an authorized integration method is established
- Advanced semantic matching and ranking optimization

## 10. Implementation Next Steps

1. Complete provider spike documentation and close the evaluation work in Jira.
2. Define the normalized `Job` model.
3. Implement `DiceAdapter` and `AdzunaAdapter`.
4. Normalize job search results from both providers.
5. Implement preliminary relevance filtering and duplicate detection.
6. Add selective AI-assisted matching and explanations.
7. Generate an HTML report containing ranked jobs and application links.
8. Validate provider usage requirements and cloud deployment before public release.

## 11. Decision Summary

**Accepted: October 9, 2026**

Job Search Agent V1 will integrate Dice MCP and Adzuna REST API.

Dice will provide the primary source of detailed job information for AI-assisted matching. Adzuna will provide complementary discovery coverage and preliminary relevance analysis.

ZipRecruiter is deferred because reliable job retrieval was not demonstrated during its POC.

The selected architecture balances demonstrated feasibility, useful job coverage, implementation simplicity, and portfolio learning value.

## 12. Supporting Evidence

- `spikes/dice/README.md` — Dice MCP evaluation
- `spikes/ziprecruiter/README.md` — ZipRecruiter MCP evaluation
- `spikes/adzuna/README.md` — Adzuna REST evaluation
- `project-notes.md` — chronological test results, decisions, and technical lessons
