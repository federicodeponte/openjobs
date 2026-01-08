# OpenJobs

Open source job scraper that extracts job listings from any careers page using **Firecrawl** for JavaScript rendering and **Gemini AI** for intelligent job extraction.

## Features

- **Universal Scraping**: Works on any careers page, not just ATS platforms
- **JavaScript Rendering**: Uses Firecrawl to render JavaScript-heavy career sites
- **AI Extraction**: Gemini AI intelligently extracts job listings from page content
- **Job Enrichment**: Optional AI-powered enrichment to extract salary, tech stack, requirements, etc.
- **Job Classification**: Categorize jobs into standard categories and subcategories
- **Rate Limiting**: Built-in rate limiting to respect API limits
- **SSRF Protection**: Security measures to prevent server-side request forgery

## Installation

```bash
pip install openjobs
```

Or install from source:

```bash
git clone https://github.com/yourusername/openjobs.git
cd openjobs
pip install -e .
```

## Quick Start

### Basic Usage

```python
from openjobs import scrape_careers_page

# Scrape jobs from any careers page
jobs = scrape_careers_page("https://linear.app/careers", company_name="Linear")

for job in jobs:
    print(f"- {job['title']} ({job['location']})")
```

### With AI Enrichment

```python
from openjobs import scrape_careers_page, process_jobs

# Scrape jobs
jobs = scrape_careers_page("https://figma.com/careers", company_name="Figma")

# Enrich with AI (extracts salary, tech stack, requirements, etc.)
enriched_jobs = process_jobs(jobs, enrich=True)

for job in enriched_jobs:
    print(f"- {job['title_original']}")
    print(f"  Category: {job['category']}")
    print(f"  Tech Stack: {', '.join(job.get('tech_stack', []))}")
    print(f"  Salary: {job.get('salary_range', 'Not specified')}")
```

### CLI Usage

```bash
# Basic scraping
python -m openjobs.scraper https://linear.app/careers Linear

# With environment variables
export GOOGLE_API_KEY=your_key
export FIRECRAWL_API_KEY=your_key
python -m openjobs.scraper https://stripe.com/careers Stripe
```

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Google API key for Gemini | Yes |
| `FIRECRAWL_API_KEY` | Firecrawl API key | Yes (for Firecrawl cloud) |
| `FIRECRAWL_URL` | Custom Firecrawl URL | No (defaults to api.firecrawl.dev) |
| `GEMINI_MODEL` | Gemini model to use | No (defaults to gemini-2.0-flash) |
| `OPENJOBS_LOG_DIR` | Directory for log files | No |

### Example `.env` file

```env
GOOGLE_API_KEY=your_google_api_key
FIRECRAWL_API_KEY=your_firecrawl_api_key
# Optional: Use self-hosted Firecrawl
# FIRECRAWL_URL=http://localhost:3002
```

## API Reference

### `scrape_careers_page(url, company_name=None, ...)`

Scrape job listings from a careers page.

**Parameters:**
- `url` (str): The careers page URL to scrape
- `company_name` (str, optional): Company name (extracted from URL if not provided)
- `firecrawl_api_key` (str, optional): Firecrawl API key
- `google_api_key` (str, optional): Google API key for Gemini
- `extraction_prompt` (str, optional): Custom prompt for job extraction

**Returns:** List of job dicts with `title`, `department`, `location`, `job_url`, `slug`, `date_scraped`

### `process_job(job, enrich=True, api_key=None)`

Process a single job with optional AI enrichment.

**Parameters:**
- `job` (dict): Raw job dict from scraper
- `enrich` (bool): Whether to use AI enrichment (default: True)
- `api_key` (str, optional): Google API key

**Returns:** Processed job dict with enriched fields

### `process_jobs(jobs, enrich=True, filter_categories=None, ...)`

Process multiple jobs with optional filtering.

**Parameters:**
- `jobs` (list): List of raw job dicts
- `enrich` (bool): Whether to use AI enrichment
- `filter_categories` (list, optional): Only return jobs in these categories
- `api_key` (str, optional): Google API key

**Returns:** List of processed job dicts

## Job Categories

Jobs are classified into these categories:

- **Software Engineering**: Backend, Frontend, Full-stack, DevOps, Mobile, etc.
- **Data**: Data Science, ML Engineering, Data Analysis, etc.
- **Product**: Product Management, User Research, etc.
- **Design**: UI/UX, Brand Design, etc.
- **Operations & Strategy**: Business Operations, Project Management, etc.
- **Sales & Account Management**: Sales, Customer Success, etc.
- **Marketing**: Growth, Content, Product Marketing, etc.
- **People/HR/Recruitment**: HR, Recruiting, etc.
- **Finance/Legal & Compliance**: Finance, Legal, etc.
- **Other Engineering**: Hardware, IT Support, etc.

## Self-Hosted Firecrawl

You can use a self-hosted Firecrawl instance:

```bash
# Run Firecrawl locally
docker run -p 3002:3002 firecrawl/firecrawl

# Set the URL
export FIRECRAWL_URL=http://localhost:3002
```

## Security

OpenJobs includes SSRF protection:
- Only allows `http` and `https` schemes
- Blocks private/internal IP addresses
- Blocks localhost and loopback addresses
- Blocks cloud metadata endpoints

## Contributing

Contributions are welcome! Please read our contributing guidelines first.

## License

MIT License - see [LICENSE](LICENSE) for details.
