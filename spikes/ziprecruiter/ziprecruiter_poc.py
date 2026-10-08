import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
from mcp.shared.exceptions import MCPError

ZIPRECRUITER_MCP_URL = "https://api.ziprecruiter.com/mcp"


async def main():
    print("Connecting to ZipRecruiter MCP...")

    async with (
        streamable_http_client(ZIPRECRUITER_MCP_URL) as (read_stream, write_stream),
        ClientSession(read_stream, write_stream) as session,
    ):
        # Initialize the client session before interacting with the MCP

        init_result = await session.initialize()

        print("Connected successfully.")
        print(f"Protocol version: {init_result.protocol_version}")
        print(f"Server info: {init_result.server_info}")
        print(f"Capabilities: {init_result.capabilities}")
        print()

        # try:
        #     await session.initialize()
        # except MCPError as e:
        #     print("\nMCP INITIALIZATION FAILED")
        #     print(f"Code: {e.code}")
        #     print(f"Message: {e.message}")
        #     print(f"Data: {e.data}")
        #     return

        print("Connected successfully.")
        print("Retrieving available tools...\n")

        # List all available tools from the MCP session
        try:
            tools = await session.list_tools()
        except Exception as e:
            print("list_tools failed")
            print(f"Exception type: {type(e)}")
            print(f"Exception: {repr(e)}")
            raise

        print("Available tools retrieved successfully.\n")

        # Print the details of each available tool
        for tool in tools.tools:
            print(f"Tool: {tool.name}")
            print(f"Description: {tool.description}")
            print()


if __name__ == "__main__":
    asyncio.run(main())
