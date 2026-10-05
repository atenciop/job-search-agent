import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

DICE_MCP_URL = "https://mcp.dice.com/mcp"


async def main():
    print("Connecting to Dice MCP...")

    async with streamable_http_client(DICE_MCP_URL) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            print("Connected successfully.")
            print("Retrieving available tools...\n")

            tools = await session.list_tools()

            for tool in tools.tools:
                print(f"Tool: {tool.name}")
                print(f"Description: {tool.description}")
                print()


if __name__ == "__main__":
    asyncio.run(main())
