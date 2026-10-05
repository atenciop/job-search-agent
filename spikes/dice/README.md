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
