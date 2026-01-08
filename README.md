# OpenJobs - AI-Powered Job Scraper for Any Career Page

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**OpenJobs** is an open-source Python library that scrapes job listings from any company careers page using [Firecrawl](https://firecrawl.dev) for JavaScript rendering and [Google Gemini AI](https://ai.google.dev/) for intelligent job extraction.

No more writing custom scrapers for each company - OpenJobs works universally on any careers page.

## Quick Start (3 Steps)

### 1. Clone & Install

```bash
git clone https://github.com/yourusername/openjobs.git
cd openjobs
pip install -e .
```

### 2. Start Firecrawl (Local)

```bash
./start.sh
```

This starts Firecrawl locally using Docker. That's it - no API keys needed for Firecrawl!

> **Don't have Docker?** Install it from [docker.com](https://docs.docker.com/get-docker/)

### 3. Scrape Jobs

```bash
export GOOGLE_API_KEY=your_key  # Get free at https://aistudio.google.com/apikey

python -c "
from openjobs import scrape_careers_page
jobs = scrape_careers_page('https://linear.app/careers')
for job in jobs:
    print(f\"- {job['title']} ({job['location']})\")
"
```

**Output:**
```
- Account Executive (Enterprise) (North America)
- Senior Software Engineer (Europe)
- Product Designer (Remote)
...
```

## Why OpenJobs?

Traditional job scrapers break when websites change. They require constant maintenance and only work with specific ATS platforms. **OpenJobs takes a different approach**:

1. **Firecrawl** renders the page (including JavaScript-heavy SPAs)
2. **Gemini AI** intelligently extracts job listings from the rendered content
3. **Works on ANY careers page** - no custom code needed per company

### Key Features

- **Universal Job Scraping** - Works on any careers page, not just ATS platforms
- **JavaScript Support** - Handles React, Vue, Angular, and other JS frameworks
- **AI-Powered Extraction** - Gemini AI extracts jobs intelligently
- **Job Classification** - Automatically categorize jobs (Engineering, Product, Design, etc.)
- **Job Enrichment** - Extract salary, tech stack, requirements, remote status
- **Self-Hosted** - Run Firecrawl locally with Docker (free, unlimited)
- **Production Ready** - Rate limiting, retry logic, SSRF protection

## Installation Options

### Option A: Self-Hosted Firecrawl (Recommended - Free & Unlimited)

```bash
# Clone repo
git clone https://github.com/yourusername/openjobs.git
cd openjobs
pip install -e .

# Start Firecrawl locally
./start.sh

# Set only Google API key (Firecrawl runs locally)
export GOOGLE_API_KEY=your_key
```

### Option B: Firecrawl Cloud (No Docker Required)

```bash
pip install openjobs

# Set both API keys
export GOOGLE_API_KEY=your_google_key
export FIRECRAWL_API_KEY=your_firecrawl_key  # Get at https://firecrawl.dev
```

## Usage Examples

### Basic Scraping

```python
from openjobs import scrape_careers_page

# Scrape any careers page
jobs = scrape_careers_page("https://stripe.com/jobs")

for job in jobs:
    print(f"- {job['title']}")
    print(f"  Location: {job['location']}")
    print(f"  URL: {job['job_url']}")
```

### With AI Enrichment

```python
from openjobs import scrape_careers_page, process_jobs

# Scrape jobs
jobs = scrape_careers_page("https://figma.com/careers")

# Enrich with AI (extracts salary, tech stack, requirements)
enriched = process_jobs(jobs, enrich=True)

for job in enriched:
    print(f"Title: {job['title_original']}")
    print(f"Category: {job['category']} > {job['subcategory']}")
    print(f"Tech Stack: {', '.join(job.get('tech_stack', []))}")
```

### Filter by Category

```python
from openjobs import scrape_careers_page, process_jobs

jobs = scrape_careers_page("https://notion.so/careers")

# Only get engineering jobs
engineering = process_jobs(
    jobs,
    filter_categories=["Software Engineering", "Data"]
)
```

### Scrape Multiple Companies

```python
from openjobs import scrape_careers_page

companies = [
    ("https://linear.app/careers", "Linear"),
    ("https://figma.com/careers", "Figma"),
    ("https://notion.so/careers", "Notion"),
]

all_jobs = []
for url, name in companies:
    jobs = scrape_careers_page(url, company_name=name)
    all_jobs.extend(jobs)
    print(f"{name}: {len(jobs)} jobs")

print(f"\nTotal: {len(all_jobs)} jobs")
```

### Command Line

```bash
python -m openjobs.scraper https://linear.app/careers Linear
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GOOGLE_API_KEY` | Google API key for Gemini | **Required** |
| `FIRECRAWL_API_KEY` | Firecrawl cloud API key | Optional |
| `FIRECRAWL_URL` | Firecrawl URL | `localhost:3002` (self-hosted) |
| `GEMINI_MODEL` | Gemini model | `gemini-2.0-flash` |

### Getting API Keys

**Google API Key (Required):**
1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Click "Create API Key"
3. Copy and set as `GOOGLE_API_KEY`

**Firecrawl API Key (Optional - only for cloud):**
1. Go to [firecrawl.dev](https://firecrawl.dev)
2. Sign up (free tier: 500 credits/month)
3. Copy and set as `FIRECRAWL_API_KEY`

## API Reference

### `scrape_careers_page(url, company_name=None)`

Scrape job listings from any careers page.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `url` | str | Careers page URL |
| `company_name` | str | Company name (auto-detected if not provided) |

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

### `process_jobs(jobs, enrich=True, filter_categories=None)`

Process and enrich jobs with AI.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `jobs` | list | Jobs from `scrape_careers_page()` |
| `enrich` | bool | Enable AI enrichment (default: True) |
| `filter_categories` | list | Filter to specific categories |

**Returns:** Enriched job dictionaries with additional fields:

```python
{
    "category": "Software Engineering",
    "subcategory": "Backend Engineer",
    "tech_stack": ["Python", "PostgreSQL", "AWS"],
    "salary_range": "$150,000 - $200,000 per year",
    "remote_type": "Hybrid",
    "experience_required": "5+ years",
    ...
}
```

## Job Categories

OpenJobs classifies jobs into 10 categories:

| Category | Examples |
|----------|----------|
| **Software Engineering** | Backend, Frontend, Full-stack, DevOps, Mobile |
| **Data** | Data Science, ML Engineering, Data Analysis |
| **Product** | Product Management, User Research |
| **Design** | UI/UX, Brand Design, Graphic Design |
| **Operations & Strategy** | Business Ops, Project Management |
| **Sales & Account Management** | Sales, Account Executive, Customer Success |
| **Marketing** | Growth, Content, Product Marketing |
| **People/HR/Recruitment** | HR, Recruiting |
| **Finance/Legal & Compliance** | Finance, Legal |
| **Other Engineering** | Hardware, IT Support |

## Docker Commands

```bash
# Start Firecrawl
./start.sh
# or
docker compose up -d

# Stop Firecrawl
docker compose down

# View logs
docker compose logs -f

# Restart
docker compose restart
```

## Supported Websites

OpenJobs works with virtually any careers page:

- **Direct career pages**: company.com/careers, company.com/jobs
- **ATS platforms**: Greenhouse, Lever, Workable, BambooHR, Ashby
- **Custom sites**: React, Vue, Angular SPAs
- **International sites**: Any language (extracted in English)

## Security

Built-in SSRF protection:
- Only allows `http`/`https` schemes
- Blocks private IP ranges
- Blocks localhost and metadata endpoints
- DNS rebinding protection

## Limitations

- Cannot bypass CAPTCHA
- Cannot scrape login-required pages
- Respect rate limits

## Contributing

1. Fork the repo
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add feature'`)
4. Push (`git push origin feature/amazing`)
5. Open Pull Request

## License

MIT License - see [LICENSE](LICENSE)

---

**Built with [Firecrawl](https://firecrawl.dev) and [Google Gemini](https://ai.google.dev/)**
