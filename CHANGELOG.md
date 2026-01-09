# Changelog

All notable changes to OpenJobs will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-08

### Added

- Initial release
- `scrape_careers_page()` - Scrape jobs from any careers page URL
- `discover_careers_url()` - Find careers page URL from company domain
- `process_jobs()` - AI enrichment with categorization, tech stack extraction
- `scrape_with_firecrawl()` - Low-level Firecrawl scraping
- `extract_jobs_from_markdown()` - Extract jobs from markdown/HTML content
- Tiered scraping with fallbacks for JavaScript-heavy sites
- Embedded JSON extraction for React/Next.js SPAs
- SSRF protection and URL validation
- Rate limiting (30 req/min)
- Self-hosted Firecrawl support via Docker Compose
- 148 unit tests
- CLI entry point: `openjobs <url>`

### Supported Sites

- Company career pages (Stripe, Linear, Figma, etc.)
- JavaScript SPAs (React, Next.js, Vue)
- ATS platforms (Lever, Greenhouse, Ashby)
- Heavy SPAs (Retool, Airtable, Vercel, Notion)

### Security

- SSRF protection (blocks localhost, private IPs, metadata endpoints)
- Blocked domains: LinkedIn, Indeed, Glassdoor (ToS compliance)
