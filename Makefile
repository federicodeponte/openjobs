.PHONY: install dev test lint format clean docker-up docker-down help

help:
	@echo "OpenJobs - Available commands:"
	@echo ""
	@echo "  make install     Install package"
	@echo "  make dev         Install with dev dependencies"
	@echo "  make test        Run tests"
	@echo "  make lint        Run linter"
	@echo "  make format      Format code"
	@echo "  make clean       Remove build artifacts"
	@echo "  make docker-up   Start Firecrawl services"
	@echo "  make docker-down Stop Firecrawl services"

install:
	pip install -e .

dev:
	pip install -e ".[dev]"

test:
	pytest tests/ -v -m "not slow"

test-all:
	pytest tests/ -v

test-cov:
	pytest tests/ --cov=openjobs --cov-report=html --cov-report=term -m "not slow"

lint:
	ruff check openjobs/

format:
	black openjobs/ tests/
	ruff check openjobs/ --fix

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .ruff_cache/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

docker-up:
	docker compose up -d
	@echo "Waiting for services to start..."
	@sleep 10
	@echo "Firecrawl available at http://localhost:3002"

docker-down:
	docker compose down

build:
	python -m build

publish-test:
	python -m twine upload --repository testpypi dist/*

publish:
	python -m twine upload dist/*
