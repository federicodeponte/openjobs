# Contributing to OpenJobs

Thanks for your interest in contributing to OpenJobs!

## Quick Start

```bash
# Clone the repo
git clone https://github.com/federicodeponte/openjobs.git
cd openjobs

# Install dev dependencies
pip install -e ".[dev]"

# Run tests
make test

# Run linter
make lint
```

## Development Setup

### Prerequisites

- Python 3.9+
- Docker (for self-hosted Firecrawl testing)

### Environment Variables

```bash
export GOOGLE_API_KEY=your_key  # Required for AI extraction
export FIRECRAWL_URL=http://localhost:3002  # For self-hosted testing
```

### Running Firecrawl Locally

```bash
docker compose up -d
```

## Making Changes

### Code Style

- We use `black` for formatting
- We use `ruff` for linting
- Run `make format` before committing

### Tests

- All new features need tests
- Run `make test` to verify
- Run `make test-cov` for coverage report

### Commit Messages

Use clear, descriptive commit messages:

```
Add support for Workday ATS pages
Fix rate limiting for concurrent requests
Update README with new examples
```

## Pull Request Process

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`make test`)
5. Run linter (`make lint`)
6. Commit your changes
7. Push to your fork
8. Open a Pull Request

## Reporting Issues

### Bug Reports

Include:
- Python version
- OpenJobs version
- URL you were trying to scrape (if applicable)
- Full error traceback

### Feature Requests

Describe:
- What problem it solves
- Example use case
- Proposed API (if applicable)

## Code of Conduct

Be respectful and constructive. We're all here to build something useful.

## Questions?

Open an issue with the "question" label.
