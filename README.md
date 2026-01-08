# OpenJobs - AI-Powered Job Scraper for Any Career Page

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/openjobs.svg)](https://badge.fury.io/py/openjobs)

**OpenJobs** is an open-source Python library that scrapes job listings from any company careers page using [Firecrawl](https://firecrawl.dev) for JavaScript rendering and [Google Gemini AI](https://ai.google.dev/) for intelligent job extraction. No more writing custom scrapers for each company - OpenJobs works universally.

## Why OpenJobs?

Traditional job scrapers break when websites change. They require constant maintenance and only work with specific ATS platforms like Greenhouse or Lever. **OpenJobs takes a different approach**:

1. **Firecrawl** renders the page (including JavaScript-heavy SPAs)
2. **Gemini AI** intelligently extracts job listings from the rendered content
3. **Works on ANY careers page** - no custom code needed per company

### Key Features

- **Universal Job Scraping** - Works on any careers page, not just ATS platforms
- **JavaScript Support** - Handles React, Vue, Angular, and other JS frameworks via Firecrawl
- **AI-Powered Extraction** - Gemini AI extracts jobs intelligently, adapting to any page structure
- **Job Enrichment** - Optional AI enrichment for salary, tech stack, requirements, remote status
- **Job Classification** - Automatically categorize jobs (Engineering, Product, Design, Data, etc.)
- **Production Ready** - Rate limiting, retry logic, SSRF protection built-in
- **Minimal Dependencies** - Just `requests` and `tenacity`

## Installation

### From PyPI

```bash
pip install openjobs
```

### From Source

```bash
git clone https://github.com/yourusername/openjobs.git
cd openjobs
pip install -e .
```

## Quick Start

### Prerequisites

You need a **Google API key** for Gemini AI. Get one free at [Google AI Studio](https://aistudio.google.com/apikey).

For Firecrawl, you can either:
- Use the [Firecrawl cloud API](https://firecrawl.dev) (requires API key)
- Self-host Firecrawl (free, no API key needed)

### Basic Job Scraping

```python
import os
from openjobs import scrape_careers_page

# Set your API key
os.environ["GOOGLE_API_KEY"] = "your_google_api_key"
os.environ["FIRECRAWL_URL"] = "https://api.firecrawl.dev"  # or self-hosted URL
os.environ["FIRECRAWL_API_KEY"] = "your_firecrawl_key"  # if using cloud

# Scrape jobs from any careers page
jobs = scrape_careers_page(
    url="https://linear.app/careers",
    company_name="Linear"
)

# Print results
for job in jobs:
    print(f"- {job['title']} ({job['location']})")
```

**Output:**
```
- Account Executive (Enterprise) (North America)
- Senior Software Engineer (San Francisco)
- Product Designer (Remote)
...
```

### Job Scraping with AI Enrichment

Extract additional structured data like salary, tech stack, and requirements:

```python
from openjobs import scrape_careers_page, process_jobs

# Scrape jobs
jobs = scrape_careers_page("https://figma.com/careers", company_name="Figma")

# Enrich with AI (extracts salary, tech stack, requirements)
enriched_jobs = process_jobs(jobs, enrich=True)

for job in enriched_jobs:
    print(f"Title: {job['title_original']}")
    print(f"Category: {job['category']} > {job['subcategory']}")
    print(f"Tech Stack: {', '.join(job.get('tech_stack', []))}")
    print(f"Salary: {job.get('salary_range', 'Not specified')}")
    print(f"Remote: {job.get('remote_type', 'Not specified')}")
    print()
```

### Filter Jobs by Category

Only get specific job types:

```python
from openjobs import scrape_careers_page, process_jobs

jobs = scrape_careers_page("https://stripe.com/jobs")

# Only Software Engineering and Data jobs
tech_jobs = process_jobs(
    jobs,
    enrich=True,
    filter_categories=["Software Engineering", "Data"]
)

print(f"Found {len(tech_jobs)} tech jobs")
```

### Command Line Usage

```bash
# Set environment variables
export GOOGLE_API_KEY=your_key
export FIRECRAWL_URL=https://api.firecrawl.dev
export FIRECRAWL_API_KEY=your_key

# Scrape jobs
python -m openjobs.scraper https://linear.app/careers Linear
```

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Google API key for Gemini AI | **Yes** |
| `FIRECRAWL_URL` | Firecrawl API URL | No (defaults to api.firecrawl.dev) |
| `FIRECRAWL_API_KEY` | Firecrawl API key | Only for cloud API |
| `GEMINI_MODEL` | Gemini model to use | No (defaults to gemini-2.0-flash) |
| `OPENJOBS_LOG_DIR` | Directory for log files | No |

### Example `.env` File

```env
# Required
GOOGLE_API_KEY=your_google_api_key

# Firecrawl (choose one)
# Option 1: Firecrawl Cloud
FIRECRAWL_URL=https://api.firecrawl.dev
FIRECRAWL_API_KEY=your_firecrawl_api_key

# Option 2: Self-hosted Firecrawl (no API key needed)
# FIRECRAWL_URL=http://localhost:3002

# Optional
# GEMINI_MODEL=gemini-2.0-flash
# OPENJOBS_LOG_DIR=logs
```

## API Reference

### `scrape_careers_page(url, company_name=None, ...)`

Scrape job listings from any careers page.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `url` | str | The careers page URL to scrape |
| `company_name` | str | Company name (auto-extracted from URL if not provided) |
| `firecrawl_api_key` | str | Firecrawl API key (optional) |
| `google_api_key` | str | Google API key (optional, uses env var) |
| `extraction_prompt` | str | Custom prompt for job extraction (optional) |

**Returns:** List of job dictionaries:

```python
{
    "company": "Linear",
    "title": "Senior Software Engineer",
    "department": "Engineering",
    "location": "San Francisco",
    "job_url": "https://linear.app/careers/...",
    "slug": "linear-senior-software-engineer",
    "date_scraped": "2025-01-08T10:30:00",
    "source_url": "https://linear.app/careers"
}
```

### `process_jobs(jobs, enrich=True, filter_categories=None, ...)`

Process and optionally enrich jobs with AI.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `jobs` | list | List of job dicts from `scrape_careers_page()` |
| `enrich` | bool | Enable AI enrichment (default: True) |
| `filter_categories` | list | Only return jobs in these categories |
| `api_key` | str | Google API key (optional) |

**Returns:** List of enriched job dictionaries with additional fields:

```python
{
    # Original fields...
    "category": "Software Engineering",
    "subcategory": "Backend Engineer",
    "tech_stack": ["Python", "PostgreSQL", "AWS"],
    "salary_range": "$150,000 - $200,000 per year",
    "remote_type": "Hybrid",
    "experience_required": "5+ years",
    "education_level": "Bachelor's Degree",
    "contract_type": "Full-Time",
    "benefits": ["Health Insurance", "Stock Options", "401k"],
    "requirements": ["Python experience", "System design skills"]
}
```

### `classify_job(job_title, api_key=None)`

Classify a job title into category and subcategory.

```python
from openjobs.processor import classify_job

result = classify_job("Senior Machine Learning Engineer")
# {
#     "category": "Data",
#     "subcategory": "Machine Learning Engineer",
#     "similar_job_title": "ML Engineer"
# }
```

## Job Categories

OpenJobs classifies jobs into 10 main categories:

| Category | Subcategories |
|----------|---------------|
| **Software Engineering** | Backend, Frontend, Full-stack, DevOps, Mobile, QA, Security, etc. |
| **Data** | Data Science, ML Engineering, Data Analysis, Data Engineering |
| **Product** | Product Management, User Research, Technical PM |
| **Design** | UI/UX, Brand Design, Graphic Design, Industrial Design |
| **Operations & Strategy** | Business Ops, Project Management, Customer Support |
| **Sales & Account Management** | Sales, Account Executive, Customer Success, Partnerships |
| **Marketing** | Growth, Content, Product Marketing, SEO, Social Media |
| **People/HR/Recruitment** | HR, Recruiting, People Operations |
| **Finance/Legal & Compliance** | Finance, Accounting, Legal, Compliance |
| **Other Engineering** | Hardware, IT Support, Technical Writing |

## Self-Hosting Firecrawl

For unlimited scraping without API costs, self-host Firecrawl:

```bash
# Using Docker
docker run -p 3002:3002 mendableai/firecrawl

# Then set the URL
export FIRECRAWL_URL=http://localhost:3002
```

See [Firecrawl documentation](https://docs.firecrawl.dev/self-host) for more options.

## Security Features

OpenJobs includes built-in SSRF (Server-Side Request Forgery) protection:

- Only allows `http` and `https` URL schemes
- Blocks private/internal IP ranges (10.x.x.x, 192.168.x.x, 172.16.x.x)
- Blocks localhost and loopback addresses
- Blocks cloud metadata endpoints (169.254.169.254)
- DNS rebinding protection

## Use Cases

### Job Aggregators

Build a job board that aggregates listings from multiple companies:

```python
companies = [
    ("https://linear.app/careers", "Linear"),
    ("https://figma.com/careers", "Figma"),
    ("https://notion.so/careers", "Notion"),
]

all_jobs = []
for url, name in companies:
    jobs = scrape_careers_page(url, company_name=name)
    all_jobs.extend(jobs)

print(f"Aggregated {len(all_jobs)} jobs from {len(companies)} companies")
```

### Job Matching Systems

Match candidates to relevant jobs:

```python
# Get only engineering jobs
jobs = scrape_careers_page("https://stripe.com/jobs")
engineering_jobs = process_jobs(
    jobs,
    filter_categories=["Software Engineering", "Data"]
)

# Filter by tech stack
python_jobs = [j for j in engineering_jobs if "Python" in j.get("tech_stack", [])]
```

### Salary Research

Collect salary data across companies:

```python
jobs = scrape_careers_page("https://company.com/careers")
enriched = process_jobs(jobs, enrich=True)

for job in enriched:
    if job.get("salary_range") != "Not Specified":
        print(f"{job['title_original']}: {job['salary_range']}")
```

## Supported Websites

OpenJobs works with virtually any careers page, including:

- **Direct career pages**: company.com/careers, company.com/jobs
- **ATS platforms**: Greenhouse, Lever, Workable, BambooHR, Ashby
- **Custom career sites**: React/Vue/Angular SPAs, static sites
- **International sites**: Works with any language (extraction in English)

## Limitations

- **Rate limits**: Respect API rate limits (Firecrawl, Gemini)
- **Dynamic content**: Some highly dynamic sites may need longer wait times
- **CAPTCHA**: Cannot bypass CAPTCHA-protected pages
- **Login-required**: Cannot scrape pages requiring authentication

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Firecrawl](https://firecrawl.dev) - JavaScript rendering and web scraping
- [Google Gemini](https://ai.google.dev/) - AI-powered content extraction
- Inspired by the need for universal job scraping without per-company maintenance

---

**Keywords**: job scraper, careers page scraper, job board scraper, web scraping, AI job extraction, Firecrawl, Gemini AI, Python job scraper, open source job scraper, universal job scraper, job aggregator, recruitment automation, HR tech, talent acquisition tools
