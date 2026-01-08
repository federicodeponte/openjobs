"""
OpenJobs Product Audit using browser-use

This script uses browser-use to:
1. Visit the GitHub repo and verify README renders correctly
2. Check the careers page that openjobs targets
"""

import asyncio
from browser_use import Agent
from browser_use.llm import ChatGoogle

# API key
API_KEY = "AIzaSyA2AICFwi_pD0wsSaLoRnkeuvJl3lFPxu4"

async def main():
    print("=" * 60)
    print("OPENJOBS PRODUCT AUDIT - Using browser-use")
    print("=" * 60)

    llm = ChatGoogle(model="gemini-2.0-flash", api_key=API_KEY)

    # Audit 1: GitHub Repository
    print("\n--- Audit 1: GitHub Repository ---\n")

    agent = Agent(
        task="""
        Go to https://github.com/federicodeponte/openjobs

        Perform a product audit and report:
        1. Is the README visible? What's the main description?
        2. How many files/folders are in the root?
        3. What's the latest commit message?
        4. Is there a docker-compose.yml file?
        5. Are there tests (look for tests/ folder)?
        6. Overall: Does this look like a production-ready open source project?

        Provide a structured report.
        """,
        llm=llm,
    )

    try:
        result = await agent.run()
        print(f"GitHub Audit Result:\n{result}")
    except Exception as e:
        print(f"GitHub audit error: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 60)
    print("AUDIT COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
