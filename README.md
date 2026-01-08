# OpenJobs

AI-powered job scraper that extracts listings from any careers page using Firecrawl + Gemini.

## Quick Start

### Option 1: Self-Hosted (Recommended - Unlimited Free Scraping)

```bash
# Clone and start Firecrawl locally
git clone https://github.com/yourusername/openjobs.git
cd openjobs
docker compose up -d

# Wait ~30 seconds for services to start, then:
pip install requests tenacity

# Set only your Gemini key (free: https://aistudio.google.com/apikey)
export GOOGLE_API_KEY=your_key
export FIRECRAWL_URL=http://localhost:3002

# Run
python -c "
from openjobs import scrape_careers_page
for job in scrape_careers_page('https://linear.app/careers'):
    print(f\"- {job['title']} ({job['location']})\")
"
```

### Option 2: Firecrawl Cloud (Easiest)

```bash
pip install requests tenacity
git clone https://github.com/yourusername/openjobs.git
cd openjobs

# Set API keys (both have free tiers)
export GOOGLE_API_KEY=your_key      # Free: https://aistudio.google.com/apikey
export FIRECRAWL_API_KEY=your_key   # Free 500/month: https://firecrawl.dev

python -c "
from openjobs import scrape_careers_page
for job in scrape_careers_page('https://linear.app/careers'):
    print(f\"- {job['title']} ({job['location']})\")
"
```

## What It Does

1. **Firecrawl** renders JavaScript-heavy career pages
2. **Gemini AI** extracts job listings intelligently
3. **Works on any site** - no custom scrapers needed

## Usage

### Basic Scraping

```python
from openjobs import scrape_careers_page

jobs = scrape_careers_page("https://stripe.com/jobs")
for job in jobs:
    print(f"- {job['title']} @ {job['location']}")
```

### With AI Enrichment

```python
from openjobs import scrape_careers_page, process_jobs

jobs = scrape_careers_page("https://figma.com/careers")
enriched = process_jobs(jobs, enrich=True)

for job in enriched:
    print(f"{job['title_original']}")
    print(f"  Category: {job['category']}")
    print(f"  Tech: {job.get('tech_stack', [])}")
```

### Filter by Category

```python
engineering = process_jobs(jobs, filter_categories=["Software Engineering", "Data"])
```

## Output Format

```json
{
  "company": "Linear",
  "title": "Senior Software Engineer",
  "department": "Product",
  "location": "Europe",
  "job_url": "https://linear.app/careers/...",
  "slug": "linear-senior-software-engineer",
  "date_scraped": "2025-01-08T10:00:00"
}
```

## Job Categories

- Software Engineering
- Data
- Product
- Design
- Operations & Strategy
- Sales & Account Management
- Marketing
- People/HR/Recruitment
- Finance/Legal & Compliance

## Self-Hosting Firecrawl

The included `docker-compose.yml` runs Firecrawl locally with all dependencies:

```bash
# Start services
docker compose up -d

# Check status
docker compose ps

# Stop services
docker compose down
```

Services included:
- **Redis** - Job queue
- **PostgreSQL** - Job metadata storage
- **RabbitMQ** - Message broker
- **Playwright** - Browser rendering
- **Firecrawl API** - Main scraping service (port 3002)

Set `FIRECRAWL_URL=http://localhost:3002` to use local instance.

## API Keys

| Service | Free Tier | Link |
|---------|-----------|------|
| Google Gemini | Generous | [aistudio.google.com](https://aistudio.google.com/apikey) |
| Firecrawl Cloud | 500 credits/month | [firecrawl.dev](https://firecrawl.dev) |

## License

MIT
