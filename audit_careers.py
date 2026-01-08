"""
OpenJobs Product Audit - Test on Linear Careers Page
"""

import asyncio
from browser_use import Agent
from browser_use.llm import ChatGoogle

API_KEY = "AIzaSyA2AICFwi_pD0wsSaLoRnkeuvJl3lFPxu4"

async def main():
    print("=" * 60)
    print("OPENJOBS - Careers Page Audit (Linear)")
    print("=" * 60)

    llm = ChatGoogle(model="gemini-2.0-flash", api_key=API_KEY)

    agent = Agent(
        task="""
        Go to https://linear.app/careers

        Audit the careers page for job scraping compatibility:
        1. How many job listings are visible?
        2. What departments/categories do you see?
        3. Are individual job URLs accessible?
        4. Is the page a SPA (JavaScript-heavy) or static HTML?
        5. Would a tool like Firecrawl + Gemini AI be able to extract jobs from this page?

        Provide a structured report.
        """,
        llm=llm,
    )

    try:
        result = await agent.run()
        print(f"\nCareers Page Audit Result:\n{result}")
    except Exception as e:
        print(f"Audit error: {e}")

    print("\n" + "=" * 60)
    print("AUDIT COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
