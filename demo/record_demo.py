#!/usr/bin/env python3
"""
Demo script for recording OpenJobs GIF.

Record with: asciinema rec demo.cast
Convert to GIF: agg demo.cast demo.gif

Or use: terminalizer record demo
"""

import time
import sys

def typewrite(text, delay=0.03):
    """Simulate typing effect."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def pause(seconds=1):
    time.sleep(seconds)

def main():
    # Clear screen
    print("\033[2J\033[H", end="")
    pause(0.5)

    # Show command
    print("\033[92m$\033[0m ", end="")
    typewrite("python3", 0.05)
    pause(0.3)

    print("\033[93m>>>\033[0m ", end="")
    typewrite("from openjobs import scrape_careers_page")
    pause(0.5)

    print("\033[93m>>>\033[0m ", end="")
    typewrite('jobs = scrape_careers_page("https://linear.app/careers")')
    pause(0.3)

    # Simulate loading
    print("\n\033[90mScraping Linear careers page...\033[0m")

    for i in range(3):
        time.sleep(0.5)
        print(f"\033[90m{'.' * (i+1)}\033[0m", end="\r")

    pause(1)
    print("\033[92m✓ Found 17 jobs\033[0m" + " " * 20)
    pause(0.5)

    print("\n\033[93m>>>\033[0m ", end="")
    typewrite("for job in jobs[:5]:")
    print("\033[93m...\033[0m ", end="")
    typewrite('    print(f"{job[\'title\']} - {job[\'location\']}")')
    pause(0.3)

    # Show results
    jobs_output = [
        ("Senior Software Engineer", "Remote (US/EU)"),
        ("Product Designer", "San Francisco, CA"),
        ("Engineering Manager", "Remote"),
        ("Backend Engineer", "New York, NY"),
        ("Frontend Engineer", "Remote (US/EU)"),
    ]

    print()
    for title, location in jobs_output:
        pause(0.2)
        print(f"\033[97m{title}\033[0m - \033[94m{location}\033[0m")

    pause(1)

    # Show the power feature
    print("\n\033[93m>>>\033[0m ", end="")
    typewrite("from openjobs import discover_careers_url")

    print("\033[93m>>>\033[0m ", end="")
    typewrite('discover_careers_url("stripe.com")')
    pause(0.5)
    print("\033[92m'https://stripe.com/jobs/search'\033[0m")

    pause(2)

    # Final message
    print("\n\033[95m" + "─" * 50 + "\033[0m")
    print("\033[95m  pip install openjobs\033[0m")
    print("\033[95m  github.com/federicodeponte/openjobs\033[0m")
    print("\033[95m" + "─" * 50 + "\033[0m")

    pause(3)

if __name__ == "__main__":
    main()
