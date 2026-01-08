"""
OpenJobs - Open source job scraper using Firecrawl + Gemini AI

Scrape job listings from any careers page using:
- Firecrawl for JavaScript rendering
- Gemini AI for intelligent job extraction
"""

__version__ = "0.1.0"

from .scraper import scrape_careers_page, scrape_with_firecrawl, extract_jobs_from_markdown
from .processor import process_job, enhance_job_output
from .utils import create_slug

__all__ = [
    "scrape_careers_page",
    "scrape_with_firecrawl",
    "extract_jobs_from_markdown",
    "process_job",
    "enhance_job_output",
    "create_slug",
]
