# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it by emailing the maintainers directly rather than opening a public issue.

**Do not open a public GitHub issue for security vulnerabilities.**

We will acknowledge receipt within 48 hours and provide a detailed response within 7 days.

## Security Measures

OpenJobs implements the following security measures:

### SSRF Protection

All URLs are validated before scraping to prevent Server-Side Request Forgery:

- Blocks `localhost`, `127.0.0.1`, `::1`, and other loopback addresses
- Blocks private IP ranges (10.x.x.x, 172.16.x.x, 192.168.x.x)
- Blocks cloud metadata endpoints (169.254.169.254)
- Blocks internal hostnames
- Only allows `http://` and `https://` schemes

### API Key Handling

- API keys are only accepted via environment variables
- No secrets are stored in code or configuration files
- `.env` files are excluded from version control via `.gitignore`

### Input Validation

- All user-provided URLs are validated and sanitized
- URLs with blocked patterns (LinkedIn, Indeed, etc.) are rejected
- File extensions (.pdf, .zip, etc.) are blocked

### Rate Limiting

- Built-in rate limiting (30 requests/minute) prevents abuse
- Thread-safe implementation for concurrent usage

## Blocked Domains

The following are blocked to comply with Terms of Service:

- linkedin.com
- indeed.com
- glassdoor.com
- monster.com
- ziprecruiter.com
- *.myworkdayjobs.com

## Best Practices

When using OpenJobs:

1. **Never commit API keys** - Use environment variables
2. **Use self-hosted Firecrawl** - For sensitive scraping operations
3. **Review scraped data** - Before storing or processing
4. **Respect robots.txt** - OpenJobs does not automatically check robots.txt
