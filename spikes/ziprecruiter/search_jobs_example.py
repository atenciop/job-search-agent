# run using this command from the terminal:
# uv run python -u spikes/ziprecruiter/search_jobs_example.py
import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
from mcp.shared.exceptions import MCPError

ZIPRECRUITER_MCP_URL = "https://api.ziprecruiter.com/mcp"


async def main():
    # Define your search arguments directly
    job_filters = {"search": "Python Developer", "location": "New York, NY"}

    print("Connecting to ZipRecruiter MCP and searching for jobs...")

    async with (
        streamable_http_client(ZIPRECRUITER_MCP_URL) as (read_stream, write_stream),
        ClientSession(read_stream, write_stream) as session,
    ):
        print("Initializing MCP session...")
        try:
            await session.initialize()
        except MCPError as e:
            print("\nMCP INITIALIZATION FAILED")
            print(f"Code: {e.code}")
            print(f"Message: {e.message}")
            print(f"Data: {e.data}")
            raise

        print("test of list_resources before calling list_resources tool")

        try:
            resources = await session.list_resources()
        except MCPError as e:
            print("\nLIST_RESOURCES FAILED")
            print(f"Code: {e.code}")
            print(f"Message: {e.message}")
            print(f"Data: {e.data}")
            return

        for resource in resources.resources:
            print(f"Resource: {resource.uri}")
            print(f"Name: {resource.name}")
            print()

        print("Executing search_jobs tool with filters " + str(job_filters))
        try:
            result = await session.call_tool("search_jobs", job_filters)
        except Exception as e:
            print("search_jobs failed")
            print(f"Exception type: {type(e)}")
            print(f"Exception: {repr(e)}")
            raise

        print("\n--- Search Results ---")
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
