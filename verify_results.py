"""
Verify openjobs scraper results using browser-use

Compare what openjobs found vs what's actually on the page
"""

import asyncio
import json
from browser_use import Agent
from browser_use.llm import ChatGoogle

API_KEY = "AIzaSyA2AICFwi_pD0wsSaLoRnkeuvJl3lFPxu4"

# Load openjobs results
with open("test_results.json") as f:
    openjobs_results = json.load(f)

async def verify_company(company_name, url, claimed_count, sample_jobs):
    """Verify a single company's results"""
    print(f"\n{'='*60}")
    print(f"Verifying: {company_name}")
    print(f"OpenJobs claimed: {claimed_count} jobs")
    print("="*60)

    llm = ChatGoogle(model="gemini-2.0-flash", api_key=API_KEY)

    sample_titles = [j.get('title', 'Unknown') for j in sample_jobs[:3]]

    agent = Agent(
        task=f"""
        Go to {url}

        Count the job listings on this careers page and verify:
        1. How many total job listings are visible?
        2. Can you find these specific jobs that openjobs claimed to find: {sample_titles}?
        3. Does the count match {claimed_count} (openjobs result)?

        Provide verification result: MATCH, CLOSE (within 20%), or MISMATCH
        """,
        llm=llm,
    )

    try:
        result = await agent.run()
        return {
            "company": company_name,
            "openjobs_count": claimed_count,
            "verification": "completed",
            "details": str(result)[:500]
        }
    except Exception as e:
        return {
            "company": company_name,
            "openjobs_count": claimed_count,
            "verification": "error",
            "error": str(e)
        }

async def main():
    print("="*60)
    print("OPENJOBS OUTPUT VERIFICATION")
    print("Using browser-use to verify scraper accuracy")
    print("="*60)

    # Only verify companies with jobs found
    to_verify = [
        r for r in openjobs_results["results"]
        if r["job_count"] > 0
    ][:3]  # Limit to 3 for speed

    verifications = []
    for r in to_verify:
        result = await verify_company(
            r["company"],
            r["url"],
            r["job_count"],
            r.get("sample", [])
        )
        verifications.append(result)
        print(f"\n{r['company']}: {result['verification']}")

    # Save verification results
    with open("verification_results.json", "w") as f:
        json.dump(verifications, f, indent=2)

    print("\n" + "="*60)
    print("VERIFICATION COMPLETE")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(main())
