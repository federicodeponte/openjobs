# OpenJobs - Project Status & Audit

**Last Updated:** 2026-01-08
**Status:** Production Ready
**Repository:** Private

---

## Quick Summary

OpenJobs is an AI-powered job scraper that extracts listings from any careers page using:
- **Firecrawl** for JavaScript rendering (self-hosted via Docker)
- **Gemini AI** for intelligent job extraction

---

## Test Results

| Metric | Value |
|--------|-------|
| Total Tests | **131** |
| Passing | **131** |
| Coverage | **83%** |
| CI/CD | GitHub Actions (Python 3.9-3.12) |

### Coverage by Module

```
openjobs/__init__.py     100%
openjobs/http_utils.py   100%
openjobs/utils.py         92%
openjobs/processor.py     87%
openjobs/scraper.py       75%
openjobs/logger.py        69%
────────────────────────────
TOTAL                     83%
```

---

## Security Checklist

- [x] **SSRF Protection** - 22 tests verify blocking of localhost, private IPs, metadata endpoints
- [x] **No Hardcoded Credentials** - All API keys via environment variables
- [x] **Rate Limiting** - Implemented for both Firecrawl and Gemini APIs
- [x] **Input Validation** - URL validation before scraping
- [x] **Repository Private** - Not publicly accessible

---

## Architecture

```
openjobs/
├── scraper.py      # Core scraping (Firecrawl + Gemini)
├── processor.py    # AI enrichment & categorization
├── http_utils.py   # HTTP retry logic
├── utils.py        # Slug generation, parsing
└── logger.py       # Logging configuration

tests/              # 131 unit tests
docker-compose.yml  # Self-hosted Firecrawl (5 services)
```

### Docker Services

| Service | Purpose | Port |
|---------|---------|------|
| api (Firecrawl) | Web scraping | 3002 |
| playwright-service | Browser rendering | 3000 |
| postgres | Job queue storage | 5432 |
| redis | Job queue | 6379 |
| rabbitmq | Message broker | 5672 |

---

## Verified Functionality

| Feature | Status | Evidence |
|---------|--------|----------|
| Scraping | ✅ Working | Linear (17 jobs), Raycast (2 jobs) |
| AI Enrichment | ✅ Working | Categories assigned correctly |
| Category Filtering | ✅ Working | Filter by Software Engineering, Data, etc. |
| Docker Self-Hosting | ✅ Working | 5/5 services running |
| pip Install | ✅ Working | `pip install -e .` succeeds |
| CI/CD | ✅ Configured | GitHub Actions on push/PR |

---

## How to Use

### Option 1: Self-Hosted (Recommended)

```bash
# Start Firecrawl locally
docker compose up -d

# Set API key
export GOOGLE_API_KEY=your_key  # Free: https://aistudio.google.com/apikey
export FIRECRAWL_URL=http://localhost:3002

# Scrape
python -c "
from openjobs import scrape_careers_page
jobs = scrape_careers_page('https://linear.app/careers')
print(f'Found {len(jobs)} jobs')
"
```

### Option 2: Firecrawl Cloud

```bash
export GOOGLE_API_KEY=your_key
export FIRECRAWL_API_KEY=your_key  # Free 500/month: https://firecrawl.dev

python -c "
from openjobs import scrape_careers_page
jobs = scrape_careers_page('https://linear.app/careers')
"
```

---

## Run Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run all tests
pytest tests/ -v -m "not slow"

# Run with coverage
pytest tests/ --cov=openjobs --cov-report=term
```

---

## For Other Agents

### Key Files to Read
1. `openjobs/scraper.py` - Main scraping logic
2. `openjobs/processor.py` - AI enrichment
3. `docker-compose.yml` - Self-hosted setup
4. `tests/` - 131 tests for reference

### Main Entry Points
```python
from openjobs import scrape_careers_page, process_jobs

# Scrape jobs
jobs = scrape_careers_page("https://company.com/careers")

# Enrich with AI
enriched = process_jobs(jobs, enrich=True)

# Filter by category
engineering = process_jobs(jobs, filter_categories=["Software Engineering"])
```

### Environment Variables
| Variable | Required | Description |
|----------|----------|-------------|
| `GOOGLE_API_KEY` | Yes | Gemini API key |
| `FIRECRAWL_URL` | For self-hosted | `http://localhost:3002` |
| `FIRECRAWL_API_KEY` | For cloud | Firecrawl API key |

---

## Audit History

| Date | Action | Result |
|------|--------|--------|
| 2026-01-08 | Initial implementation | Complete |
| 2026-01-08 | Added Docker self-hosting | 5 services working |
| 2026-01-08 | Added 131 unit tests | 83% coverage |
| 2026-01-08 | Added GitHub Actions CI/CD | Configured |
| 2026-01-08 | Security audit | SSRF protection verified |
| 2026-01-08 | Made repository private | Confirmed |

---

## Known Limitations

1. **Heavy JS Sites** - Some sites (e.g., Workday) may timeout
2. **Gemini Rate Limits** - Free tier has request limits
3. **No Caching** - Each scrape makes fresh API calls

---

## Contact

Repository: https://github.com/federicodeponte/openjobs (Private)
