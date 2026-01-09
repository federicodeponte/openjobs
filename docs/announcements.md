# Launch Announcements

## Twitter/X

### Short (280 chars)
```
Just launched OpenJobs - scrape job listings from any careers page in 3 lines of Python

pip install openjobs

Works with JS-heavy sites, React SPAs, and ATS systems. No custom scrapers needed.

https://github.com/federicodeponte/openjobs
```

### Thread Version
```
1/ Just open-sourced OpenJobs 🚀

Scrape job listings from ANY careers page in 3 lines of code.

pip install openjobs

No custom scrapers. No maintenance. Just works.

2/ The problem: Every careers page has different HTML.

Scrapy? Custom spider per site.
BeautifulSoup? Static HTML only.
Selenium? Slow and breaks constantly.

3/ The solution: Firecrawl (JS rendering) + Gemini AI (smart extraction)

- Works on React, Next.js, Vue
- Handles Lever, Greenhouse, Ashby
- Even heavy SPAs like Retool, Airtable

4/
from openjobs import scrape_careers_page

jobs = scrape_careers_page("https://stripe.com/jobs")
# Returns 142 structured job listings ✓

5/ Features:
- Auto-discover careers URLs from domains
- AI enrichment (categories, tech stacks, salaries)
- Self-hosted option (unlimited free scraping)
- 148 tests, MIT licensed

https://github.com/federicodeponte/openjobs
```

## Reddit r/Python

### Title
```
OpenJobs - Scrape job listings from any careers page in 3 lines of code (Firecrawl + Gemini AI)
```

### Body
```
Hey r/Python!

I just open-sourced OpenJobs, a library that scrapes job listings from any careers page without writing custom scrapers.

**The problem:** Every company has a different careers page. Scrapy needs a custom spider per site. BeautifulSoup can't handle JavaScript. Selenium is slow and breaks.

**The solution:** OpenJobs uses Firecrawl for JS rendering and Gemini AI for smart extraction.

```python
from openjobs import scrape_careers_page

jobs = scrape_careers_page("https://stripe.com/jobs")
# Returns 142 structured job listings
```

**Features:**
- Works on React, Next.js, Vue SPAs
- Handles ATS platforms (Lever, Greenhouse, Ashby)
- Auto-discover careers URLs from company domains
- AI enrichment (categories, tech stacks, salaries)
- Self-hosted Firecrawl option for unlimited free scraping
- 148 tests, fully typed, MIT licensed

**Links:**
- GitHub: https://github.com/federicodeponte/openjobs
- PyPI: https://pypi.org/project/openjobs/

Would love feedback!
```

## Hacker News

### Title
```
Show HN: OpenJobs – Scrape job listings from any careers page with AI
```

### Body
```
I built OpenJobs to solve a problem I kept running into: scraping careers pages is tedious because every site is different.

OpenJobs uses Firecrawl (headless browser → markdown) and Gemini AI (smart extraction) to scrape any careers page without custom code.

    pip install openjobs

    from openjobs import scrape_careers_page
    jobs = scrape_careers_page("https://stripe.com/jobs")

It handles JavaScript SPAs, ATS platforms, and even heavy sites like Retool and Airtable. There's also a self-hosted Firecrawl option for unlimited free scraping.

GitHub: https://github.com/federicodeponte/openjobs
```

## LinkedIn

```
🚀 Just open-sourced OpenJobs

A Python library that scrapes job listings from any careers page in 3 lines of code.

The problem: Every company has a different careers page structure. Building scrapers for each is tedious and they break constantly.

The solution: OpenJobs uses Firecrawl for JavaScript rendering and Gemini AI for intelligent extraction. No custom scrapers needed.

Works with:
✓ JavaScript SPAs (React, Next.js, Vue)
✓ ATS platforms (Lever, Greenhouse, Ashby)
✓ Heavy SPAs (Retool, Airtable, Vercel)

pip install openjobs

GitHub: https://github.com/federicodeponte/openjobs

#opensource #python #webscraping #ai #recruitment
```
