import asyncio
import json

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

DICE_MCP_URL = "https://mcp.dice.com/mcp"


async def main():
    print("Connecting to Dice MCP...")

    async with (
        streamable_http_client(DICE_MCP_URL) as (read_stream, write_stream),
        ClientSession(read_stream, write_stream) as session,
    ):
        await session.initialize()

        print("Connected successfully.")
        print("Searching Dice...\n")

        result = await session.call_tool(
            "search_jobs",
            arguments={
                "keyword": "Technical Project Manager",
                "location": "Nashville, TN",
                "jobs_per_page": 5,
            },
        )

        #  print(result.structured_content)

        jobs = result.structured_content["data"]

        print(f"\nDice returned {len(jobs)} jobs:\n")

        for job in jobs:
            print(f"Title: {job['title']}")
            print(f"Company: {job['companyName']}")
            print(f"Salary: {job['salary']}")
            print(f"Employment Type: {job['employmentType']}")
            print(f"Workplace Type: {job['workplaceTypes']}")
            print(f"Posted: {job['postedDate']}")
            print(f"URL: {job['detailsPageUrl']}")
            print("-" * 80)

        output_file = "output/dice_jobs_raw.json"

        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(
                result.structured_content,
                file,
                indent=2,
                ensure_ascii=False,
            )

        print(f"\nResults saved to {output_file}")


if __name__ == "__main__":
    asyncio.run(main())
