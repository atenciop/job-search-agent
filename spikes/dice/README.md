## Initial Findings

- Successfully connected directly to Dice remote MCP server from Python.
- No LLM required to invoke the MCP server.
- Server currently exposes three tools:
  - search_jobs
  - get_job_details
  - get_company
- search_jobs provides structured job-search results.
- get_job_details provides full job description and skills for a selected job.
- Dice requires AI-assistance disclosure when presenting search results to users.

## Final Findings

Dice MCP Local POC — PASS

Validated:

- Remote MCP connectivity
- MCP tool discovery
- Job search
- Server-side search filters
- Recency filtering
- Workplace filtering
- Employment-type filtering
- Newest-first sorting
- Structured job metadata
- Direct job URLs
- Full job-description retrieval
- Structured skill retrieval
- JSON output

Findings:

- Search results are relevant but include adjacent job titles.
- Workplace filtering appears to use membership/OR semantics.
- Remote jobs may be returned independently of physical search location.
- Salary data is not consistently normalized.
- Full descriptions contain HTML and require cleanup.
- Structured skills could support deterministic preliminary matching.
- Search results can contain potential duplicate/closely related postings.
- Dice requires an AI-assistance disclosure when results are presented.
- Basic MCP access does not require authentication.

Status:
Local technical feasibility: PASS
Cloud feasibility: Not yet tested
Final provider selection: Pending comparison with other providers
