import json
import anyio
from mcp import ClientSession
from mcp.client.sse import sse_client

ZIPRECRUITER_MCP_URL = "https://api.ziprecruiter.com/mcp"


async def inspect_ziprecruiter_tools():
    print(f"Connecting to ZipRecruiter MCP at {ZIPRECRUITER_MCP_URL}")

    # 1. Define custom headers to bypass gateway filtering
    custom_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/event-stream",
        # If ZipRecruiter provided an API/Bearer Token, add it below:
        # "Authorization": "Bearer YOUR_ZIPRECRUITER_API_KEY"
    }

    try:
        # 2. Inject headers into the SSE transport layer
        async with sse_client(ZIPRECRUITER_MCP_URL, headers=custom_headers) as (
            read_stream,
            write_stream,
        ):
            print("Network connection established. Creating protocol session...")

            async with ClientSession(read_stream, write_stream) as session:
                print("About to wait for session initialization...")
                await session.initialize()
                print("Connected successfully.\n")

                print("Retrieving available tools...\n")
                result = await session.list_tools()
                print("Available tools retrieved successfully.\n")

                print(
                    f"\nFound {len(result.tools)} tool(s) registered on this server:\n"
                )

                for tool in result.tools:
                    print(f"Tool Name:  {tool.name}")
                    print(f"Description: {tool.description}")
                    print("Arguments Schema:")
                    print(json.dumps(tool.input_schema, indent=2))
                    print("-" * 60)

    except Exception as e:
        print(f"\nConnection failed: {e}")


if __name__ == "__main__":
    anyio.run(inspect_ziprecruiter_tools)
