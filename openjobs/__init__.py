"""
OpenJobs - Open source job scraper using Firecrawl + Gemini AI

Scrape job listings from any careers page using:
- Firecrawl for JavaScript rendering
- Gemini AI for intelligent job extraction
"""

__version__ = "0.1.0"

from .processor import enhance_job_output, process_job, process_jobs
from .scraper import extract_jobs_from_markdown, scrape_careers_page, scrape_with_firecrawl
from .utils import create_slug

__all__ = [
    "scrape_careers_page",
    "scrape_with_firecrawl",
    "extract_jobs_from_markdown",
    "process_job",
    "process_jobs",
    "enhance_job_output",
    "create_slug",
]
