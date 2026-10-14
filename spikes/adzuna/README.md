# Adzuna REST API — Provider Spike

**Project:** Job Search Agent  
**Provider:** Adzuna  
**Integration:** REST API  
**Status:** PASS — Selected for V1 with limitations  
**Evaluation completed:** October 9, 2026

## 1. Objective

Evaluate whether the Adzuna REST API can serve as a reliable job-discovery provider for Job Search Agent V1.

The POC focuses on API connectivity, structured job data, search filtering, description completeness, and navigation to application pages.

Adzuna is evaluated as a complementary provider to Dice MCP.

## 2. Environment and Dependencies

- Python managed through `uv`
- `requests` — HTTP client
- `python-dotenv` — local credential configuration
- VS Code with integrated PowerShell terminal
- Adzuna Developer API credentials

API endpoint:

`GET https://api.adzuna.com/v1/api/jobs/us/search/1`

Documentation: https://developer.adzuna.com/

## 3. Setup and Execution

From the Job Search Agent project root, install dependencies:

```powershell
uv add requests python-dotenv
```

Create a `.env` file in the project root containing:

```dotenv
ADZUNA_APP_ID=your_app_id
ADZUNA_APP_KEY=your_app_key
```

Do not commit credentials to source control.

The project's `.gitignore` excludes `.env` and the `output/` directory.

Run the POC:

```powershell
uv run python spikes/adzuna/adzuna_poc.py
```

The script authenticates with Adzuna, executes a job search, prints selected job information, and saves the JSON response to:

`output/adzuna_results.json`

The saved output is excluded from Git.

## 4. Test Coverage and Results

| Test                            | Observation                                                           | Result                |
| ------------------------------- | --------------------------------------------------------------------- | --------------------- |
| Authentication and connectivity | HTTP 200; valid JSON response                                         | PASS                  |
| Initial Nashville search        | 294 matches reported; 10 retrieved                                    | PASS                  |
| Recency filtering               | 58 matches; 10 inspected jobs posted today or yesterday               | PASS                  |
| Geographic filtering            | Atlanta search returned 111 matches in the area                       | PASS                  |
| Full-time filtering             | Spot checks supported correct filtering                               | Preliminary PASS      |
| Salary filtering                | Match count reduced from 57 to 27                                     | PASS with limitations |
| Description completeness        | Initial sample descriptions truncated at approximately 500 characters | LIMITATION            |
| Job links                       | Listings opened successfully                                          | PASS                  |
| Application navigation          | Adzuna Apply links led to application pages                           | PASS                  |

### Search Parameters Tested

- `what` — job search keywords
- `where` — geographic location
- `results_per_page` — number of returned records
- `max_days_old` — posting recency
- `sort_by` — result ordering
- `full_time` — employment type
- `salary_min` — salary threshold

Tests were performed incrementally to isolate the effects of individual filters.

## 5. Data Available

The API response includes useful structured job metadata:

- Job ID, title, and company
- Geographic location
- Posting date
- Job description snippet
- Salary minimum and maximum, when available
- Salary prediction indicator
- Job category
- Redirect URL

These fields support job discovery, deterministic filtering, basic relevance assessment, and source attribution.

## 6. Limitations and Risks

### Description completeness

The ten descriptions inspected in the initial sample were truncated at approximately 500 characters.

Full descriptions were available through Adzuna's website, but not through the tested API response.

**Implication:** Adzuna results can support preliminary matching but should not be treated as sufficient for comprehensive AI resume-to-job qualification analysis.

### Salary filtering

A search with `salary_min=120000` returned a job with a stated salary range of $91,400–$187,000.

This suggests that Adzuna may include jobs whose ranges overlap the requested threshold. The exact filter semantics were not established.

Salary prediction indicators must be preserved, and estimated salaries should not be presented as confirmed employer compensation.

### Search relevance

Some results were only loosely related to the requested Technical Project Manager role.

The application will need additional relevance filtering.

### Potential duplicates

Multiple postings may share a company and job title while representing distinct openings.

Deduplication should use more than company and title alone.

### Location and work arrangement

Geographic search results can include remote positions.

Location and remote/hybrid/on-site classification should be handled separately.

### Application navigation

Some Adzuna pages display an optional email-alert signup prompt before the job description.

The prompt can be dismissed. Verified listings provided access to application pages.

## 7. Architecture Recommendation

**Select Adzuna REST as a secondary job-discovery provider for V1.**

Proposed provider responsibilities:

| Provider    | Primary use                                                                              |
| ----------- | ---------------------------------------------------------------------------------------- |
| Dice MCP    | Detailed job descriptions, structured skills, AI-assisted matching                       |
| Adzuna REST | Additional discovery coverage, search filtering, preliminary matching, application links |

Both providers should eventually return results normalized into a common `Job` model.

The application should:

- Preserve source attribution and provider job IDs.
- Distinguish full descriptions from truncated snippets.
- Apply deterministic relevance filtering before AI analysis.
- Preserve salary ranges and prediction indicators.
- Detect potential duplicates across providers.
- Provide links to original job listings.
- Avoid presenting snippet-based fit assessments as comprehensive evaluations.

## 8. Outstanding Validation

The local POC demonstrated technical feasibility, but the following remain outside its scope:

- Cloud deployment and connectivity
- API quotas and production reliability
- Applicable API usage, attribution, and redistribution requirements
- Larger-volume searches and pagination
- Cross-provider duplicate detection
- Normalized job data model implementation
- Production error handling, retries, and logging

## 9. Final Decision

**Local technical feasibility: PASS**

**V1 integration decision: ACCEPTED — with documented limitations**

Adzuna successfully returned structured job listings, supported useful search filters, and provided working links to complete postings and application pages.

The POC also produced practical value: retrieved listings were used to identify job opportunities and submit applications.

Adzuna is suitable for V1 job discovery, while Dice remains the preferred provider for detailed AI matching.

## 10. Related Documentation

- `project-notes.md` — chronological spike findings and technical lessons
- `docs/adr/ADR-001.md` — job-source integration evaluation and architectural decision (confirm the actual filename)
- `spikes/adzuna/adzuna_poc.py` — executable proof of concept
- `spikes/dice/README.md` — Dice MCP provider evaluation
- `spikes/ziprecruiter/README.md` — deferred ZipRecruiter MCP evaluation
