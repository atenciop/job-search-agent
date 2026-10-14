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

- Reviewed ZipRecruiter Job Search MCP documentation.
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

---

## 2026-10-09 — Adzuna REST API Provider Spike

### Objective

Determine whether the Adzuna REST API can provide reliable job discovery, useful search filtering, structured job metadata, and working application links for Job Search Agent V1.

Evaluate whether Adzuna can complement Dice MCP as a second job-data provider.

### Work Completed

- Registered for Adzuna API access and obtained application credentials.
- Configured credentials using a local `.env` file excluded from Git.
- Installed Python `requests` and `python-dotenv` dependencies using `uv`.
- Created a standalone Python REST API client in `spikes/adzuna/adzuna_poc.py`.
- Successfully authenticated and executed job searches using the US jobs endpoint.
- Retrieved structured JSON responses and saved results locally in `output/`.
- Tested posting recency, geographic location, full-time employment, and salary filtering.
- Inspected job metadata, description completeness, and potential duplicates.
- Manually verified job listing links and navigation to application pages.
- Used Adzuna search results to identify actual job opportunities and submit applications.

### Successful Findings

**API Connectivity and Data Retrieval**

- REST API requests returned HTTP 200.
- Authentication using `app_id` and `app_key` worked.
- The initial Nashville Technical Project Manager search reported 294 matching jobs and returned 10 records.
- JSON responses contained structured fields including job ID, title, company, location, posting date, description, salary information, category, and redirect URL.
- The integration was straightforward using Python `requests`, without MCP session initialization or tool discovery.

**Posting Recency**

- Added `max_days_old=7` and `sort_by=date` parameters.
- The Nashville search reported 58 matching jobs.
- All 10 inspected results had posting dates from the current or previous day.
- The results supported the usefulness of server-side recency filtering.

**Geographic Filtering**

- Changed the search location from Nashville to Atlanta.
- Adzuna reported 111 matching jobs.
- Inspected results were geographically relevant to the Atlanta area.
- Some geographically associated jobs included remote-work options.
- Geographic location and work arrangement should be treated as separate attributes.

**Full-Time Employment Filtering**

- Tested the `full_time=1` parameter.
- Spot checks showed full-time positions in the filtered results.
- An Atlanta listing that did not indicate full-time employment was no longer returned.
- Filtering appeared effective, although complete employment-type field coverage was not established.

**Salary Filtering**

- Tested `salary_min=120000`.
- The Nashville matching-job count decreased from 57 to 27.
- Some returned positions had salary ranges with lower bounds below $120,000.
- One example had a salary range of $91,400–$187,000.
- This suggests the provider may include positions whose salary ranges overlap the requested threshold.
- The exact filtering semantics were not independently established.
- Salary values may be predicted or employer-provided, as indicated by `salary_is_predicted`.

**Job Links and Application Navigation**

- Verified that Adzuna job links opened successfully.
- Some pages presented an optional email-alert signup prompt that could be dismissed.
- Adzuna displayed complete job descriptions on its website.
- The Apply button led to the employer's or recruiter’s application page.
- Technical Project Manager job links were also successfully verified.
- The POC produced practical value: results were used to identify jobs and submit applications.

### Key Limitations

**Incomplete API Descriptions**

- All 10 descriptions in the initial sample were truncated to approximately 500 characters.
- Complete descriptions were visible on Adzuna's website but were not supplied in the tested API responses.
- These snippets can support preliminary relevance analysis but are insufficient for comprehensive resume-to-job qualification matching.
- The V1 application should not assume it can automatically retrieve full descriptions from Adzuna's website.

**Search Relevance**

- Some results were not closely related to Technical Project Management.
- An Instructional Designer position appeared in the Technical Project Manager search.
- Provider search results require additional relevance filtering before being presented to users.

**Salary Interpretation**

- Salary filtering does not necessarily mean that every returned job's minimum salary meets the requested threshold.
- Predicted salary values must be distinguished from employer-provided compensation.
- The application should display available salary ranges and avoid overstating salary certainty.

**Potential Duplicates**

- Two Eliassen Group listings had the same job title but different job IDs, descriptions, and reference numbers.
- Similar titles and companies are not sufficient evidence that listings are duplicates.
- Duplicate detection should consider multiple attributes.

**Posting Dates and Work Arrangement**

- API posting dates may reflect when jobs were indexed or added to Adzuna rather than the employer's original publication date.
- Remote, hybrid, and on-site arrangements may require additional classification because geographic location alone is insufficient.

### Architecture Implications

- Adzuna can complement Dice by expanding job discovery coverage.
- Dice remains preferable for detailed AI matching because it provides fuller job descriptions and structured skills.
- Adzuna results should support preliminary matching based on available metadata and snippets.
- Provider-specific results should be normalized into a common `Job` model.
- The normalized model should preserve provider name, provider job ID, source URL, description completeness, salary prediction status, and other available metadata.
- Deterministic filtering should remove obviously irrelevant results before AI analysis.
- Match explanations should distinguish preliminary assessments from those based on full job descriptions.
- The application should provide working source links so users can review complete postings and apply.
- The adapter architecture should isolate differences between MCP and REST integrations.

### Technical Lessons

- A successful HTTP response confirms connectivity but does not establish that the provider satisfies application requirements.
- REST APIs can be evaluated incrementally by changing one query parameter at a time.
- Saving JSON responses makes it easier to inspect data structures and identify limitations.
- API filtering semantics must be validated against actual returned data.
- Manual navigation testing is useful when an API supplies redirect URLs but incomplete descriptions.
- Technical POCs should evaluate business usefulness as well as integration feasibility.

### Decision

**Select Adzuna REST as the secondary job-discovery provider for Job Search Agent V1.**

Use Dice MCP as the preferred source for detailed job information and AI-assisted matching.

Use Adzuna REST for additional discovery coverage, search filtering, preliminary relevance assessment, and navigation to complete job postings.

This decision is based on demonstrated local API functionality, usable structured data, effective search filtering, working application links, and practical usefulness during the job search.

Adzuna's limited API descriptions must be explicitly accommodated in the application design.

### Result

**Local technical feasibility: PASS**

**V1 provider suitability: ACCEPTED, with documented limitations**

Cloud deployment, API quotas, production reliability, and applicable usage requirements remain to be validated.

### V1 Provider Direction

- **Dice MCP:** Selected for rich job data and detailed matching.
- **Adzuna REST:** Selected for complementary job discovery.
- **ZipRecruiter MCP:** Deferred because reliable end-to-end job retrieval was not demonstrated.
- **Indeed integrations:** Deferred pending a suitable officially supported integration path.

### Next

1. Update the Adzuna spike README with test results and limitations.
2. Update ADR-001 to document the V1 provider selection.
3. Complete the provider-evaluation Jira work.
4. Define a common normalized `Job` data model.
5. Implement separate Dice MCP and Adzuna REST provider adapters.
6. Begin integrating provider results into the Job Search Agent application.
