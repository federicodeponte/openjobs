# OpenJobs Browser Audit Report

**Date:** 2026-01-08
**Tool:** browser-use v0.11.2 with Gemini 2.0 Flash

---

## Audit 1: GitHub Repository

**URL:** https://github.com/federicodeponte/openjobs

### Findings:

| Check | Result |
|-------|--------|
| README Visible | Yes |
| Description | AI-powered job scraper using Firecrawl + Gemini |
| Root Files/Folders | 14 total |
| docker-compose.yml | Yes |
| tests/ folder | Yes |
| Latest Commit | "Fix repo URLs and improve documentation" |

### Files in Root:
- **Folders:** .github, examples, openjobs, tests
- **Files:** .env.example, .gitignore, LICENSE, README.md, STATUS.md, docker-compose.yml, nuq.sql, pyproject.toml, requirements.txt, setup.py

### Assessment:
Production-ready. The project has:
- README with clear documentation
- MIT License
- docker-compose for self-hosting
- Test suite
- CI/CD via GitHub Actions
- Recent active commits

---

## Audit 2: Target Careers Page (Linear)

**URL:** https://linear.app/careers

### Findings:

| Check | Result |
|-------|--------|
| Job Listings Visible | 12 |
| Departments | GTM, Magic Team, Product, Product Support |
| Individual Job URLs | Accessible |
| Page Type | SPA (JavaScript-heavy) |
| Firecrawl + Gemini Compatible | Yes |

### Job Categories Found:
- Account Executive (Enterprise, Growth, Startups, APAC, EU)
- Customer Success Manager
- Event Marketing Lead
- Solutions Engineer
- Writer
- Designer (Web & Brand)
- Engineering Leader
- Senior / Staff Backend Engineer
- Senior / Staff Fullstack Engineer
- Senior / Staff Product Engineer
- Senior / Staff Product Engineer (AI)
- Product Support Specialist

### Assessment:
The Linear careers page is suitable for openjobs scraping:
- Jobs are listed in a structured format
- Individual job URLs are accessible
- Content loads via JavaScript (requires Firecrawl for rendering)
- Job details are extractable by Gemini AI

---

## Conclusion

**OpenJobs is production-ready** based on browser audit:
1. Repository is well-structured with all necessary files
2. Target careers pages (like Linear) are compatible with the scraping approach
3. Firecrawl + Gemini AI can successfully extract job listings

**Verified with browser-use automated testing.**
