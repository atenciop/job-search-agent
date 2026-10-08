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

# ADR-001: Job Source Integration Evaluation

## Status

Proposed

## Date

2026-10-07

## Context

The Job Search Agent requires access to current job postings from external job sources.

The application is intended to aggregate job opportunities, normalize results, remove duplicates, apply user-defined filters, and eventually use AI to evaluate job/resume fit and explain strengths and gaps.

Before integrating job providers into the main application, standalone proof-of-concept (POC) implementations are being developed.

The purpose of the POCs is to verify actual integration behavior rather than selecting providers based only on documentation.

The initial providers considered were:

- Dice – MCP
- ZipRecruiter – MCP
- Adzuna – REST API
- USAJOBS – REST API

An additional objective is to demonstrate more than one integration pattern in the portfolio. Therefore, a combination of MCP and conventional REST API integration is preferred over multiple providers using the same integration mechanism.

## Decision Drivers

Providers will be evaluated based on:

- Reliability
- Integration complexity
- Search quality
- U.S. job coverage
- Relevance to technology and project/delivery management roles
- Job-description completeness
- Structured metadata
- Job URLs
- Filtering capabilities
- Authentication requirements
- Rate limits
- Terms/access restrictions
- Suitability for AI-based fit analysis
- Local development support
- Future cloud deployment compatibility
- Portfolio and learning value

## ZipRecruiter Evaluation

ZipRecruiter provides an HTTP MCP endpoint at:

`https://api.ziprecruiter.com/mcp`

Its MCP documentation describes a `search_jobs` tool supporting keyword search and filters including location, radius, country, salary, recency, workplace type, employment type, and seniority.

A standalone Python POC was created using the MCP Python SDK.

### Successful Tests

The client was able to:

- Establish communication with the MCP endpoint.
- Successfully initialize MCP sessions during multiple test runs.
- Negotiate MCP protocol version `2025-11-25`.
- Receive server identification:
  - Name: `jobseeker-mcp`
  - Version: `1.0.0`
- Receive server capabilities advertising both Tools and Resources support.

### Problems Observed

The following operations returned MCP error `-32603` ("Server returned an error response"):

- `tools/list`
- `resources/list`
- `tools/call` using `search_jobs`

MCP initialization also intermittently returned `-32603`.

Earlier testing encountered HTTP 409 responses.

To determine whether the problem was specific to the Python MCP implementation, the endpoint was independently tested using MCP Inspector.

The Inspector request returned:

`HTTP 429 – Too Many Requests`

This demonstrated that access/reliability problems were not limited to the Python application.

ZipRecruiter's separate Partner Platform documentation confirms that some ZipRecruiter APIs implement rate limiting and use HTTP 429 responses. However, that documentation describes the Embedded Sponsorship API rather than the Job Search MCP endpoint and therefore does not establish the MCP endpoint's specific rate-limit policy.

### ZipRecruiter Conclusion

The POC did not demonstrate reliable end-to-end retrieval of jobs from ZipRecruiter.

ZipRecruiter will therefore not be included in Job Search Agent V1.

This does not permanently reject ZipRecruiter as a provider. It is deferred for reevaluation in a future version if MCP reliability, access guidance, or rate-limit documentation improves.

## V1 Integration Strategy

V1 should preferably contain:

1. One MCP-based job provider.
2. One conventional REST API job provider.

Dice is currently the preferred MCP provider, subject to completion of its POC evaluation.

Adzuna is a REST API candidate.

However, Adzuna's API documentation indicates that the returned job description can be a snippet rather than a complete job description. This could reduce its usefulness for AI-based resume/job fit analysis.

Adzuna should therefore be compared with other legitimate job APIs before the V1 REST provider is finalized.

## Proposed Architecture

    Job Provider
         |
         +-- Dice MCP -------- DiceAdapter
         |
         +-- REST API -------- RestProviderAdapter
                                  |
                                  v
                           Normalized Job Model
                                  |
                           Deduplication / Filters
                                  |
                              AI Analysis
                                  |
                               Ranking
                                  |
                             HTML Report

Each provider-specific adapter should isolate external integration details from the rest of the application.

This allows providers to be added, removed, or replaced without significantly changing downstream processing.

## Consequences

### Positive

- V1 is not dependent on an integration that could not be demonstrated reliably.
- Provider-specific behavior is isolated behind adapters.
- The portfolio demonstrates both MCP and REST API integration.
- Future providers can be added incrementally.
- Provider reliability is validated before architectural commitment.
- The POC process provides evidence supporting architectural decisions.

### Negative

- ZipRecruiter will not be available in V1 despite being a recognizable job-search platform.
- Another REST API provider must be evaluated.
- Job coverage will initially be narrower than originally envisioned.

## Deferred

- ZipRecruiter MCP integration
- Additional job-board providers
- Provider health/failover logic
- Advanced rate-limit handling
- Scheduled job retrieval
- Automated provider retry/backoff strategies

## Next Steps

1. Complete Dice MCP POC and document results.
2. Evaluate Adzuna REST API.
3. Research at least one alternative REST job API.
4. Compare REST candidates.
5. Select V1 REST provider.
6. Update this ADR from `Proposed` to `Accepted`.
7. Implement provider adapters only after provider selection.
