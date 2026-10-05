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
                "jobs_per_page": 10,
                "sort": "datePosted",
                "posted_date": "SEVEN",
                "workplace_types": ["Remote", "Hybrid"],
                "employment_types": ["FULLTIME", "CONTRACTS"],
            },
        )

        print(result.structured_content)

        metadata = result.structured_content["metadata"]

        print("\nSearch Metadata:")
        print(f"Matching jobs: {metadata['total']}")
        print(f"Sort: {metadata['sortBy']}")
        print(f"Selected filters: {metadata['selectedFilters']}")

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

        # selected_job = jobs[3]  #  we will be pulling the details for the 4th job

        # print("\nSelected job for detail retrieval:")
        # print(f"Title: {selected_job['title']}")
        # print(f"Company: {selected_job['companyName']}")
        # print(f"GUID: {selected_job['guid']}")

        # print("\nRetrieving full job details...")

        # details_result = await session.call_tool(
        #     "get_job_details",
        #     arguments={
        #         "job_id": selected_job["guid"],
        #     },
        # )

        # print("\nFull job details:\n")
        # print(details_result.structured_content)

        # details = details_result.structured_content

        # print("\nFull Description:\n")
        # print(details["description"])

        # print("\nSkills:\n")

        # for skill in details["skills"]:
        #     print(f"- {skill['name']}")


if __name__ == "__main__":
    asyncio.run(main())
