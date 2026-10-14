# to run in terminal:
# uv run python spikes/adzuna/adzuna_poc.py
import os
import requests
from dotenv import load_dotenv
import json
from pathlib import Path

load_dotenv()

app_id = os.getenv("ADZUNA_APP_ID")
app_key = os.getenv("ADZUNA_APP_KEY")
print(app_id)
print(app_key)


if not app_id or not app_key:
    raise RuntimeError("Missing Adzuna API credentials")

url = "https://api.adzuna.com/v1/api/jobs/us/search/1"


params = {
    "app_id": app_id,
    "app_key": app_key,
    "what": "Technical Project Manager",
    "where": "Nashville",
    "results_per_page": 10,
    "max_days_old": 7,
    "sort_by": "date",
    "salary_min": 120000,
}

response = requests.get(url, params=params, timeout=30)

print(f"HTTP status: {response.status_code}")

response.raise_for_status()

data = response.json()

print(f"Total matching jobs: {data.get('count', 'Unknown')}")
print(f"Jobs returned: {len(data.get('results', []))}")

for job in data.get("results", []):
    print(f"Title: {job.get('title')}")
    print(f"Posted: {job.get('created')}")
    print(f"Company: {job.get('company', {}).get('display_name')}")
    print(f"Location: {job.get('location', {}).get('display_name')}")
    print(f"Salary Min: {job.get('salary_min')}")
    print(f"Salary Max: {job.get('salary_max')}")
    print(f"Salary Predicted: {job.get('salary_is_predicted')}")
    print("-" * 50)

# Save the complete response for later analysis.
output_path = Path("output/adzuna_results.json")
output_path.parent.mkdir(parents=True, exist_ok=True)

with output_path.open("w", encoding="utf-8") as file:
    json.dump(data, file, indent=2, ensure_ascii=False)

print(f"\nResults saved to: {output_path}")

# To visually inspect description completeness and potential duplicates.
for index, job in enumerate(data.get("results", []), start=1):
    description = job.get("description") or ""

    print(f"\nJob {index}: {job.get('title')}")
    print(f"Job ID: {job.get('id')}")
    print(f"Posted: {job.get('created')}")
    print(f"Location: {job.get('location', {}).get('display_name')}")
    print(f"Description length: {len(description)} characters")
    print(f"Description: {description[:500]}")
    print(f"Salary Min: {job.get('salary_min')}")
    print(f"Salary Max: {job.get('salary_max')}")
    print(f"Salary Predicted: {job.get('salary_is_predicted')}")
    print("-" * 60)
