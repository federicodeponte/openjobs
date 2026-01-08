"""
OpenJobs Multi-Company Scraper Test

Tests the openjobs scraper on multiple company career pages
and saves results for browser-use verification.
"""

import json
import os
from datetime import datetime

# Set API keys
os.environ["GOOGLE_API_KEY"] = "AIzaSyA2AICFwi_pD0wsSaLoRnkeuvJl3lFPxu4"
os.environ["FIRECRAWL_URL"] = "https://api-production-8df3.up.railway.app"

from openjobs import scrape_careers_page, process_jobs

# Companies to test
COMPANIES = [
    ("https://linear.app/careers", "Linear"),
    ("https://www.raycast.com/careers", "Raycast"),
    ("https://posthog.com/careers", "PostHog"),
    ("https://www.notion.so/careers", "Notion"),
    ("https://cal.com/careers", "Cal.com"),
]

def test_company(url, name):
    """Test scraping a single company"""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"URL: {url}")
    print("="*60)

    try:
        jobs = scrape_careers_page(url, company_name=name)
        print(f"✅ Found {len(jobs)} jobs")

        if jobs:
            print("\nSample jobs:")
            for job in jobs[:3]:
                print(f"  - {job.get('title', 'N/A')} @ {job.get('location', 'N/A')}")

        return {
            "company": name,
            "url": url,
            "status": "success",
            "job_count": len(jobs),
            "jobs": jobs,
            "sample": jobs[:3] if jobs else []
        }
    except Exception as e:
        print(f"❌ Error: {e}")
        return {
            "company": name,
            "url": url,
            "status": "error",
            "error": str(e),
            "job_count": 0,
            "jobs": []
        }

def main():
    print("="*60)
    print("OPENJOBS MULTI-COMPANY SCRAPER TEST")
    print(f"Date: {datetime.now().isoformat()}")
    print("="*60)

    results = []
    total_jobs = 0
    successful = 0

    for url, name in COMPANIES:
        result = test_company(url, name)
        results.append(result)

        if result["status"] == "success":
            successful += 1
            total_jobs += result["job_count"]

    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Companies tested: {len(COMPANIES)}")
    print(f"Successful: {successful}/{len(COMPANIES)}")
    print(f"Total jobs found: {total_jobs}")
    print()

    for r in results:
        status = "✅" if r["status"] == "success" else "❌"
        print(f"{status} {r['company']}: {r['job_count']} jobs")

    # Save results
    output = {
        "test_date": datetime.now().isoformat(),
        "summary": {
            "companies_tested": len(COMPANIES),
            "successful": successful,
            "total_jobs": total_jobs
        },
        "results": results
    }

    with open("test_results.json", "w") as f:
        json.dump(output, f, indent=2)

    print(f"\n📁 Results saved to test_results.json")

    return results

if __name__ == "__main__":
    main()
