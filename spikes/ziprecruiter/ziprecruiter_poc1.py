import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

ZIPRECRUITER_MCP_URL = "https://api.ziprecruiter.com/mcp"


async def main():
    print("Connecting to ZipRecruiter MCP...")

    async with (
        streamable_http_client(ZIPRECRUITER_MCP_URL) as (read_stream, write_stream),
        ClientSession(read_stream, write_stream) as session,
    ):
        # Initialize the client session before interacting with the MCP
        print("Initializing client session...")
        await session.initialize()

        print("Connected successfully.")
        print("Retrieving available tools...\n")

        # List all available tools from the MCP session
        tools = await session.list_tools()
        print("Available tools retrieved successfully.\n")

        # Print the details of each available tool
        for tool in tools.tools:
            print(f"Tool: {tool.name}")
            print(f"Description: {tool.description}")
            print()


if __name__ == "__main__":
    asyncio.run(main())
