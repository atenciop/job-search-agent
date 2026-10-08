# ZipRecruiter MCP Integration Spike

## Purpose

This spike evaluates whether ZipRecruiter's Job Search MCP server is suitable as a job-data provider for the Job Search Agent.

The goal was not to build production integration code.

The goal was to answer a simpler question:

> Can a standalone application reliably connect to ZipRecruiter's MCP server and retrieve structured job listings?

The provider would only be incorporated into the main application after this capability was demonstrated.

## Endpoint

ZipRecruiter MCP endpoint:

`https://api.ziprecruiter.com/mcp`

ZipRecruiter's MCP documentation describes a `search_jobs` tool supporting job search and filters.

## Technology

The spike uses:

- Python
- uv
- MCP Python SDK
- Streamable HTTP MCP transport

MCP Inspector was also used as an independent client for diagnostic testing.

## Tests Performed

The spike tested:

1. MCP connection.
2. MCP session initialization.
3. Protocol negotiation.
4. Server capability discovery.
5. `tools/list`.
6. `resources/list`.
7. Direct `search_jobs` tool invocation.
8. Independent endpoint testing using MCP Inspector.

## Successful Results

MCP initialization succeeded during multiple test runs.

One diagnostic run returned:

- MCP protocol: `2025-11-25`
- Server: `jobseeker-mcp`
- Server version: `1.0.0`
- Tools capability advertised
- Resources capability advertised

This demonstrated that the endpoint could establish and negotiate an MCP session with the Python client.

## Issues Observed

Subsequent MCP operations were not reliable.

Observed failures included:

| Operation                  | Result                              |
| -------------------------- | ----------------------------------- |
| `initialize`               | Intermittently succeeded / `-32603` |
| `tools/list`               | MCP `-32603`                        |
| `resources/list`           | MCP `-32603`                        |
| `tools/call search_jobs`   | MCP `-32603`                        |
| MCP Inspector `tools/list` | HTTP `429 Too Many Requests`        |

Earlier testing also encountered HTTP 409 responses.

The MCP `-32603` responses contained the message:

`Server returned an error response`

No additional error data was returned.

## Independent Validation

The MCP endpoint was also tested using MCP Inspector to determine whether the failures were specific to the Python implementation.

Example:

    npx @modelcontextprotocol/inspector --cli \
      https://api.ziprecruiter.com/mcp \
      --transport http \
      --method tools/list

The independent test returned:

`HTTP 429 – Too Many Requests`

This indicated that endpoint/access behavior was not limited to the Python POC.

## Decision

**ZipRecruiter is deferred from Job Search Agent V1.**

The POC did not demonstrate reliable end-to-end retrieval of job postings.

The integration may be reevaluated in a future release if:

- MCP endpoint reliability improves,
- rate-limit behavior becomes better documented,
- additional integration guidance becomes available, or
- a supported alternative ZipRecruiter integration becomes appropriate.

## Why the Spike Is Retained

The spike remains in the repository because it documents an architectural evaluation and demonstrates the process used to validate external dependencies before incorporating them into the application.

A POC that identifies an unsuitable dependency is still a successful engineering outcome.

## V1 Direction

Job Search Agent V1 will preferably use:

- one MCP-based job provider, and
- one conventional REST API job provider.

This provides both useful job-source coverage and demonstrates multiple integration approaches.

See:

`docs/adr/001-job-source-integration-evaluation.md`

for the overall provider-selection decision.
