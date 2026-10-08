# Job Search Agent — Project Notes

## 2026-10-04 — Dice MCP Provider Spike

### Objective

Determine whether Dice MCP can provide usable job data for the
Job Search Agent.

### Work Completed

- Installed the Python MCP SDK.
- Connected Python client to the Dice remote MCP server.
- Used MCP tool discovery to identify available tools.
- Executed job searches with search_jobs.
- Retrieved full job details using get_job_details.
- Tested server-side filtering and sorting.
- Saved structured results as JSON.

### Key Findings

- Dice exposes search_jobs, get_job_details, and get_company.
- Basic MCP access does not require authentication.
- Search results contain structured job metadata and direct URLs.
- Full descriptions are available but contain HTML.
- Dice provides a structured skills list.
- Salary data is not consistently normalized.
- Search results may contain adjacent roles and potential duplicates.
- Remote jobs can be returned when searching a geographic location.
- Dice requires AI-assistance disclosure when presenting results.

### Architecture Implications

- Structured skills could support deterministic Python-based
  preliminary matching before invoking an LLM.
- Full descriptions could be retrieved only for shortlisted jobs,
  reducing MCP calls and AI token usage.
- Provider-specific results should eventually be normalized into
  a common Job model.
- Duplicate detection will be needed when aggregating providers.

### Decisions / Decision Candidates

- Candidate: Use deterministic filtering before AI semantic analysis.
  Final decision deferred until other providers are evaluated.
- Candidate: Use a provider adapter architecture.
  Final decision deferred until provider comparison is complete.

### Issues / Technical Lessons

- Installed MCP SDK version returns two values from
  streamable_http_client(), not three.
- Ruff SIM117 recommended combining nested async context managers.
- MCP structured_content can be consumed directly rather than
  parsing the text representation.

### Result

**Local technical feasibility: PASS**

Cloud feasibility remains to be tested.

### Next

Evaluate ZipRecruiter MCP using the same general criteria.

---

## 2026-10-07 — ZipRecruiter MCP Provider Spike

### Objective

Determine whether ZipRecruiter MCP can reliably provide usable job data
for the Job Search Agent.

The POC was intentionally implemented independently of the main application
so that provider feasibility could be established before creating an
architectural dependency.

### Work Completed

- Reviewed ZipRecruititer Job Search MCP documentation.
- Created a standalone Python MCP client.
- Connected to the ZipRecruiter MCP endpoint.
- Successfully initialized MCP sessions during multiple test runs.
- Inspected negotiated MCP protocol and advertised server capabilities.
- Attempted MCP tool discovery using tools/list.
- Attempted resource discovery using resources/list.
- Attempted direct invocation of search_jobs.
- Tested the same endpoint independently using MCP Inspector.
- Reviewed additional ZipRecruiter documentation related to API rate limiting.

### Successful Findings

During successful initialization, the ZipRecruiter MCP server returned:

- MCP protocol version: 2025-11-25
- Server name: jobseeker-mcp
- Server version: 1.0.0
- Tools capability
- Resources capability

This demonstrated that the Python MCP client could establish and negotiate
an MCP session with the ZipRecruiter server.

ZipRecruiter's MCP documentation identifies search_jobs as the job-search
tool and describes filters including keyword, location, radius, country,
salary, recency, workplace type, employment type, and seniority.

### Reliability / Integration Issues

Reliable job retrieval could not be demonstrated.

Observed behavior included:

- tools/list returned MCP error -32603.
- resources/list returned MCP error -32603.
- Direct tools/call of search_jobs returned MCP error -32603.
- MCP initialization intermittently returned -32603.
- Earlier testing encountered HTTP 409 responses.
- MCP error responses generally contained no additional diagnostic data.
- MCP Inspector independently returned HTTP 429 Too Many Requests.

A controlled test was also performed after leaving the endpoint idle for
several hours. MCP initialization succeeded, but the immediately following
resources/list operation returned -32603.

This reduced confidence that the earlier failures were caused only by
repeated rapid testing.

### Rate-Limit Research

Additional ZipRecruiter Partner Platform documentation confirms that the
Embedded Sponsorship API uses rate limiting and HTTP 429 responses.

However, that documentation applies to the Sponsorship API rather than the
Job Search MCP endpoint.

Therefore, it provides evidence that ZipRecruiter uses rate limiting in
other API products, but it should not be treated as documentation of the
MCP endpoint's specific limits or cooldown behavior.

### Architecture Implications

- External providers should be validated through isolated POCs before being
  incorporated into the main application.
- Successful MCP initialization alone is not sufficient evidence that a
  provider is production-usable.
- Provider selection must consider reliability in addition to documented
  capabilities.
- Provider-specific failures should eventually be isolated behind adapters
  so that failure of one job source does not necessarily prevent searches
  against other providers.
- Retry, backoff, and rate-limit handling should be considered when the
  production provider architecture is implemented.
- The application should avoid unnecessary provider calls where possible.

### Technical Lessons

- MCP protocol negotiation can succeed even when subsequent MCP operations
  fail.
- Advertised server capabilities do not by themselves prove that the
  advertised operations work reliably.
- MCP error -32603 provides limited diagnostic value when the server returns
  no additional error data.
- Testing the same endpoint with an independent MCP client is useful for
  separating application-specific problems from provider or interoperability
  problems.
- Controlled tests are more useful than repeatedly changing multiple
  variables during troubleshooting.
- A POC can be successful even when the resulting decision is not to adopt
  the technology being evaluated.

### Decision

Defer ZipRecruiter from Job Search Agent V1.

The POC did not demonstrate sufficiently reliable end-to-end job retrieval
to justify making V1 dependent on the ZipRecruiter MCP endpoint.

ZipRecruiter may be reevaluated in a future version if:

- MCP reliability improves,
- rate-limit behavior becomes better documented,
- additional integration guidance becomes available, or
- another supported ZipRecruiter integration becomes appropriate.

### Result

**Local technical feasibility for V1: DEFER**

The endpoint can negotiate an MCP session, but reliable job retrieval was
not demonstrated.

### V1 Provider Direction

Prefer two complementary provider integration styles:

1. One MCP-based provider.
2. One conventional REST API provider.

Dice is currently the preferred MCP provider based on its successful local
POC.

A REST API provider still needs to be selected.

Adzuna remains a candidate, but its description completeness and suitability
for AI-based job/resume matching must be validated.

At least one additional legitimate REST job API should be researched before
making the final selection.

### Next

Evaluate REST API provider candidates and select the provider to pair with
Dice for V1.
