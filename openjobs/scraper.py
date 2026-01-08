"""
OpenJobs Scraper - Scrape job listings from any careers page

Uses Firecrawl for JavaScript rendering and Gemini AI for job extraction.
"""

import os
import json
import time
import threading
import ipaddress
import socket
import requests
from urllib.parse import urlparse
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional

from .logger import logger
from .utils import create_slug
from .http_utils import post_json_with_retry

# Configuration
FIRECRAWL_URL = os.getenv("FIRECRAWL_URL", "https://api.firecrawl.dev")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"

# Firecrawl wait time configuration
DEFAULT_WAIT_MS = 5000  # Default wait for JS rendering
SLOW_SPA_WAIT_MS = 8000  # Extra time for heavy JS sites

# Patterns that need extra wait time (heavy JS career sites)
SLOW_SITE_PATTERNS = [
    'workday', 'lever.co', 'greenhouse.io', 'bamboohr',
    'careers.', 'jobs.', 'apply.', 'hire.'
]


class RateLimiter:
    """Rate limiter to prevent overwhelming APIs."""

    def __init__(self, requests_per_minute: int = 30):
        self.requests_per_minute = requests_per_minute
        self.requests = []
        self.lock = threading.Lock()

    def wait(self):
        """Wait if necessary to stay within rate limit."""
        with self.lock:
            now = datetime.now()
            minute_ago = now - timedelta(minutes=1)

            # Remove old requests outside the window
            self.requests = [t for t in self.requests if t > minute_ago]

            # If at limit, wait for oldest request to expire
            if len(self.requests) >= self.requests_per_minute:
                oldest = min(self.requests)
                sleep_time = (oldest + timedelta(minutes=1) - now).total_seconds()
                if sleep_time > 0:
                    logger.debug(f"Rate limit reached, waiting {sleep_time:.1f}s")
                    time.sleep(sleep_time)

            # Record this request
            self.requests.append(datetime.now())


# Global rate limiter instance
firecrawl_rate_limiter = RateLimiter(requests_per_minute=30)

# URLs that cannot be scraped or are not career pages
SKIP_URL_PATTERNS = [
    # File extensions (not pages)
    '.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.pdf', '.zip',
    # Social media / login pages (can't scrape)
    'linkedin.com', 'twitter.com', 'facebook.com', 'instagram.com',
    # Generic job boards (not company-specific)
    'indeed.com', 'glassdoor.com', 'monster.com', 'ziprecruiter.com',
    # Workday (has its own ATS - too complex to scrape)
    '.myworkdayjobs.com',
]


def _is_private_ip(ip_str: str) -> bool:
    """Check if an IP address is private, loopback, or otherwise internal."""
    try:
        ip = ipaddress.ip_address(ip_str)
        return (
            ip.is_private or
            ip.is_loopback or
            ip.is_reserved or
            ip.is_link_local or
            ip.is_multicast or
            ip.is_unspecified
        )
    except ValueError:
        return False


def is_valid_url(url: str) -> Tuple[bool, str]:
    """
    Check if a URL is valid for scraping.

    Security: Blocks SSRF attacks by validating:
    - URL scheme (only http/https)
    - No internal/private IP addresses
    - No localhost or loopback addresses

    Returns:
        (is_valid, reason) - True if valid, False with reason if not
    """
    if not url:
        return False, "Empty URL"

    url_lower = url.lower()

    # Parse URL for security checks
    try:
        parsed = urlparse(url)
    except Exception:
        return False, "Invalid URL format"

    # Security: Only allow http/https schemes
    if parsed.scheme not in ('http', 'https'):
        return False, f"Invalid URL scheme: {parsed.scheme} (only http/https allowed)"

    # Security: Block localhost and loopback variations
    hostname = parsed.hostname or ''
    hostname_lower = hostname.lower()

    blocked_hosts = [
        'localhost', '127.0.0.1', '::1', '0.0.0.0',
        'localhost.localdomain', 'local', 'internal',
        'metadata.google.internal',  # GCP metadata
        '169.254.169.254',  # AWS/GCP/Azure metadata endpoint
    ]

    if hostname_lower in blocked_hosts:
        return False, f"Blocked hostname: {hostname}"

    # Security: Check if hostname resolves to private/internal IP
    try:
        if _is_private_ip(hostname):
            return False, f"Private/internal IP not allowed: {hostname}"

        # For hostnames, resolve and check the IP
        try:
            ipaddress.ip_address(hostname)
        except ValueError:
            # It's a hostname, resolve it
            try:
                resolved_ip = socket.gethostbyname(hostname)
                if _is_private_ip(resolved_ip):
                    return False, f"Hostname resolves to private IP: {hostname} -> {resolved_ip}"
            except socket.gaierror:
                pass  # DNS resolution failed - allow through
    except Exception:
        pass

    # Check for skip patterns
    for pattern in SKIP_URL_PATTERNS:
        if pattern in url_lower:
            return False, f"Skipped pattern: {pattern}"

    return True, "OK"


# Default extraction prompt for Gemini
EXTRACTION_PROMPT = """Extract all job listings from this careers page content.

IMPORTANT:
- ONLY extract jobs that are explicitly listed on the page
- Do NOT invent or assume job titles that aren't clearly stated
- If unsure whether something is a job listing, skip it
- If no jobs are clearly listed, return an empty array

For each job, return a JSON object with:
- title: job title exactly as written on the page (required)
- department: department or team name if stated (optional)
- location: job location if stated (optional)
- url: direct link to job posting if available (optional)

Return ONLY a valid JSON array. No explanation, no markdown.
If no jobs found, return: []

Example output:
[{"title": "Software Engineer", "department": "Engineering", "location": "Remote", "url": "https://..."}]"""


def scrape_with_firecrawl(url: str, api_key: Optional[str] = None) -> str:
    """
    Scrape a URL using Firecrawl and return markdown content.

    Args:
        url: The URL to scrape
        api_key: Optional Firecrawl API key (uses FIRECRAWL_API_KEY env var if not provided)

    Returns:
        Markdown content of the page, or empty string on failure
    """
    # Apply rate limiting before making request
    firecrawl_rate_limiter.wait()

    # Determine wait time based on URL patterns
    url_lower = url.lower()
    wait_time = DEFAULT_WAIT_MS
    if any(pattern in url_lower for pattern in SLOW_SITE_PATTERNS):
        wait_time = SLOW_SPA_WAIT_MS
        logger.debug(f"Using extended wait time ({wait_time}ms) for slow site: {url}")

    try:
        headers = {}
        firecrawl_api_key = api_key or os.getenv("FIRECRAWL_API_KEY", "")
        if firecrawl_api_key:
            headers["Authorization"] = f"Bearer {firecrawl_api_key}"

        data = post_json_with_retry(
            f"{FIRECRAWL_URL}/v1/scrape",
            json_body={
                "url": url,
                "formats": ["markdown"],
                "waitFor": wait_time
            },
            headers=headers if headers else None,
            timeout=60
        )

        if not data:
            logger.error(f"Firecrawl returned empty response for {url}")
            return ""

        return data.get('data', {}).get('markdown', '')

    except Exception as e:
        logger.error(f"Firecrawl request failed: {e}")
        return ""


def extract_jobs_from_markdown(
    markdown: str,
    prompt: Optional[str] = None,
    api_key: Optional[str] = None
) -> List[Dict]:
    """
    Use Gemini to extract job listings from markdown content.

    Args:
        markdown: Page content as markdown
        prompt: Custom extraction prompt (uses default if not provided)
        api_key: Google API key (uses GOOGLE_API_KEY env var if not provided)

    Returns:
        List of job dicts with title, department, location, url
    """
    if not markdown or len(markdown) < 50:
        return []

    google_api_key = api_key or GOOGLE_API_KEY
    if not google_api_key:
        logger.error("GOOGLE_API_KEY not set")
        return []

    extraction_prompt = prompt or EXTRACTION_PROMPT
    start_time = time.time()

    try:
        payload = {
            "contents": [{"parts": [{"text": f"{extraction_prompt}\n\nPage content:\n{markdown[:25000]}"}]}],
            "generationConfig": {
                "temperature": 0.1,
                "maxOutputTokens": 8192
            }
        }

        response = requests.post(
            f"{GEMINI_URL}?key={google_api_key}",
            json=payload,
            timeout=30
        )
        duration_ms = int((time.time() - start_time) * 1000)

        if response.status_code != 200:
            logger.error(f"Gemini error {response.status_code}: {response.text[:200]}")
            return []

        result = response.json()

        # Extract text from response
        text = ""
        if 'candidates' in result and result['candidates']:
            parts = result['candidates'][0].get('content', {}).get('parts', [])
            for part in parts:
                if 'text' in part:
                    text += part['text']

        if not text:
            return []

        # Parse JSON from response
        text = text.strip()
        if text.startswith('```'):
            lines = text.split('\n')
            text = '\n'.join(lines[1:-1] if lines[-1] == '```' else lines[1:])

        start = text.find('[')
        end = text.rfind(']') + 1

        if start == -1 or end == 0:
            return []

        jobs = json.loads(text[start:end])
        logger.debug(f"Extracted {len(jobs)} jobs in {duration_ms}ms")
        return [j for j in jobs if isinstance(j, dict) and j.get('title')]

    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse Gemini response: {e}")
        return []
    except Exception as e:
        logger.error(f"Gemini extraction failed: {e}")
        return []


def scrape_careers_page(
    url: str,
    company_name: Optional[str] = None,
    firecrawl_api_key: Optional[str] = None,
    google_api_key: Optional[str] = None,
    extraction_prompt: Optional[str] = None
) -> List[Dict]:
    """
    Scrape job postings from a careers page using Firecrawl + Gemini.

    This is the main entry point for scraping jobs from any careers page.

    Args:
        url: The careers page URL to scrape
        company_name: Optional company name (extracted from URL if not provided)
        firecrawl_api_key: Optional Firecrawl API key
        google_api_key: Optional Google API key for Gemini
        extraction_prompt: Optional custom prompt for job extraction

    Returns:
        List of job entries with: company, job_url, slug, title, department, location, date_scraped
    """
    if not url:
        return []

    # Ensure URL has protocol
    if not url.startswith('http'):
        url = f'https://{url}'

    # Validate URL before scraping
    is_valid, reason = is_valid_url(url)
    if not is_valid:
        logger.info(f"Skipping invalid URL: {url} ({reason})")
        return []

    # Extract company name from URL if not provided
    if not company_name:
        try:
            parsed = urlparse(url)
            company_name = parsed.netloc.replace('www.', '').split('.')[0]
        except Exception:
            company_name = "unknown"

    logger.info(f"Scraping {company_name} careers page: {url}")

    # Step 1: Scrape page with Firecrawl
    markdown = scrape_with_firecrawl(url, api_key=firecrawl_api_key)
    if not markdown:
        logger.warning(f"No content from Firecrawl for {url}")
        return []

    # Step 2: Extract jobs with Gemini
    jobs = extract_jobs_from_markdown(
        markdown,
        prompt=extraction_prompt,
        api_key=google_api_key
    )
    if not jobs:
        logger.info(f"No jobs extracted from {url}")
        return []

    logger.info(f"Extracted {len(jobs)} jobs from {company_name}")

    # Step 3: Format output
    jobs_data = []
    now = datetime.now().isoformat()

    for idx, job in enumerate(jobs):
        title = job.get('title', '')
        job_url = job.get('url') or f"{url}#job-{idx}"

        job_entry = {
            "company": company_name,
            "title": title,
            "department": job.get('department'),
            "location": job.get('location'),
            "job_url": job_url,
            "slug": create_slug(company_name, title),
            "date_scraped": now,
            "source_url": url
        }

        jobs_data.append(job_entry)

    return jobs_data


# CLI interface
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m openjobs.scraper <careers_url> [company_name]")
        print("\nExample:")
        print("  python -m openjobs.scraper https://linear.app/careers Linear")
        sys.exit(1)

    url = sys.argv[1]
    company = sys.argv[2] if len(sys.argv) > 2 else None

    print(f"\nScraping: {url}")
    print("-" * 50)

    jobs = scrape_careers_page(url, company)

    if jobs:
        print(f"\nFound {len(jobs)} jobs:\n")
        for job in jobs:
            print(f"  - {job['title']}")
            if job.get('department'):
                print(f"    Department: {job['department']}")
            if job.get('location'):
                print(f"    Location: {job['location']}")
            print()
    else:
        print("\nNo jobs found.")
