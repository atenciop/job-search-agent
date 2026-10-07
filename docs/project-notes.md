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
