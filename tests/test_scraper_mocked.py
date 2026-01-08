"""Mocked tests for openjobs.scraper module - no live API required."""

import pytest
from unittest.mock import patch, MagicMock
import json

from openjobs.scraper import (
    scrape_careers_page,
    scrape_with_firecrawl,
    extract_jobs_from_markdown,
    RateLimiter,
)


class TestRateLimiter:
    """Tests for RateLimiter class."""

    def test_rate_limiter_creation(self):
        """Test rate limiter can be created."""
        limiter = RateLimiter(requests_per_minute=10)
        assert limiter.requests_per_minute == 10
        assert limiter.requests == []

    def test_rate_limiter_wait_under_limit(self):
        """Test wait() doesn't block when under limit."""
        limiter = RateLimiter(requests_per_minute=100)
        # Should not block
        limiter.wait()
        assert len(limiter.requests) == 1


class TestScrapeWithFirecrawlMocked:
    """Mocked tests for scrape_with_firecrawl."""

    @patch('openjobs.scraper.post_json_with_retry')
    @patch('openjobs.scraper.firecrawl_rate_limiter')
    def test_successful_scrape(self, mock_limiter, mock_post):
        """Test successful Firecrawl scrape."""
        mock_post.return_value = {
            'data': {
                'markdown': '# Jobs\n- Software Engineer\n- Product Manager'
            }
        }

        result = scrape_with_firecrawl('https://example.com/careers')

        assert result == '# Jobs\n- Software Engineer\n- Product Manager'
        mock_post.assert_called_once()

    @patch('openjobs.scraper.post_json_with_retry')
    @patch('openjobs.scraper.firecrawl_rate_limiter')
    def test_empty_response(self, mock_limiter, mock_post):
        """Test handling of empty Firecrawl response."""
        mock_post.return_value = {}

        result = scrape_with_firecrawl('https://example.com/careers')

        assert result == ''

    @patch('openjobs.scraper.post_json_with_retry')
    @patch('openjobs.scraper.firecrawl_rate_limiter')
    def test_exception_handling(self, mock_limiter, mock_post):
        """Test exception handling in scrape."""
        mock_post.side_effect = Exception("Network error")

        result = scrape_with_firecrawl('https://example.com/careers')

        assert result == ''


class TestExtractJobsFromMarkdownMocked:
    """Mocked tests for extract_jobs_from_markdown."""

    @patch('openjobs.scraper.requests.post')
    def test_successful_extraction(self, mock_post):
        """Test successful job extraction from markdown."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'candidates': [{
                'content': {
                    'parts': [{
                        'text': '[{"title": "Engineer", "location": "Remote"}]'
                    }]
                }
            }]
        }
        mock_post.return_value = mock_response

        # Markdown must be > 50 chars
        long_markdown = '# Jobs at Company\n- Software Engineer - Remote\n- Product Manager - NYC\n' * 2
        result = extract_jobs_from_markdown(
            long_markdown,
            api_key='test-key'
        )

        assert len(result) == 1
        assert result[0]['title'] == 'Engineer'

    @patch('openjobs.scraper.requests.post')
    def test_extraction_with_markdown_code_block(self, mock_post):
        """Test extraction handles markdown code blocks in response."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'candidates': [{
                'content': {
                    'parts': [{
                        'text': '```json\n[{"title": "Designer"}]\n```'
                    }]
                }
            }]
        }
        mock_post.return_value = mock_response

        # Markdown must be > 50 chars
        long_markdown = '# Jobs at Company\n- Designer - Remote\n- Another role here\n' * 2
        result = extract_jobs_from_markdown(long_markdown, api_key='test-key')

        assert len(result) == 1
        assert result[0]['title'] == 'Designer'

    @patch('openjobs.scraper.requests.post')
    def test_extraction_api_error(self, mock_post):
        """Test handling of API error response."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = 'Internal Server Error'
        mock_post.return_value = mock_response

        result = extract_jobs_from_markdown('# Jobs', api_key='test-key')

        assert result == []

    def test_extraction_no_api_key(self):
        """Test extraction fails gracefully without API key."""
        with patch.dict('os.environ', {'GOOGLE_API_KEY': ''}):
            result = extract_jobs_from_markdown('# Jobs')
            assert result == []

    def test_extraction_empty_markdown(self):
        """Test extraction with empty markdown."""
        result = extract_jobs_from_markdown('')
        assert result == []

    def test_extraction_short_markdown(self):
        """Test extraction with too-short markdown."""
        result = extract_jobs_from_markdown('Hi')
        assert result == []

    @patch('openjobs.scraper.requests.post')
    def test_extraction_invalid_json(self, mock_post):
        """Test handling of invalid JSON in response."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'candidates': [{
                'content': {
                    'parts': [{
                        'text': 'This is not valid JSON'
                    }]
                }
            }]
        }
        mock_post.return_value = mock_response

        result = extract_jobs_from_markdown('# Jobs', api_key='test-key')

        assert result == []

    @patch('openjobs.scraper.requests.post')
    def test_extraction_filters_invalid_jobs(self, mock_post):
        """Test that jobs without titles are filtered out."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'candidates': [{
                'content': {
                    'parts': [{
                        'text': '[{"title": "Valid"}, {"location": "NoTitle"}, {"title": ""}]'
                    }]
                }
            }]
        }
        mock_post.return_value = mock_response

        # Markdown must be > 50 chars
        long_markdown = '# Jobs at Company\n- Valid Job - Remote\n- Another role\n' * 2
        result = extract_jobs_from_markdown(long_markdown, api_key='test-key')

        assert len(result) == 1
        assert result[0]['title'] == 'Valid'


class TestScrapeCareersPageMocked:
    """Mocked tests for scrape_careers_page."""

    @patch('openjobs.scraper.extract_jobs_from_markdown')
    @patch('openjobs.scraper.scrape_with_firecrawl')
    def test_full_scrape_pipeline(self, mock_firecrawl, mock_extract):
        """Test full scraping pipeline."""
        mock_firecrawl.return_value = '# Careers\n- Engineer'
        mock_extract.return_value = [
            {'title': 'Software Engineer', 'location': 'Remote', 'url': 'https://example.com/job1'}
        ]

        result = scrape_careers_page('https://example.com/careers')

        assert len(result) == 1
        assert result[0]['title'] == 'Software Engineer'
        assert result[0]['company'] == 'example'
        assert 'slug' in result[0]
        assert 'date_scraped' in result[0]

    @patch('openjobs.scraper.extract_jobs_from_markdown')
    @patch('openjobs.scraper.scrape_with_firecrawl')
    def test_scrape_with_company_name(self, mock_firecrawl, mock_extract):
        """Test scraping with explicit company name."""
        mock_firecrawl.return_value = '# Careers'
        mock_extract.return_value = [{'title': 'Engineer'}]

        result = scrape_careers_page('https://example.com/careers', company_name='Acme Corp')

        assert result[0]['company'] == 'Acme Corp'

    @patch('openjobs.scraper.scrape_with_firecrawl')
    def test_scrape_empty_firecrawl_response(self, mock_firecrawl):
        """Test handling when Firecrawl returns empty."""
        mock_firecrawl.return_value = ''

        result = scrape_careers_page('https://example.com/careers')

        assert result == []

    @patch('openjobs.scraper.extract_jobs_from_markdown')
    @patch('openjobs.scraper.scrape_with_firecrawl')
    def test_scrape_no_jobs_found(self, mock_firecrawl, mock_extract):
        """Test handling when no jobs are extracted."""
        mock_firecrawl.return_value = '# About Us'
        mock_extract.return_value = []

        result = scrape_careers_page('https://example.com/careers')

        assert result == []

    def test_scrape_empty_url(self):
        """Test scraping with empty URL."""
        result = scrape_careers_page('')
        assert result == []

    def test_scrape_invalid_url(self):
        """Test scraping with invalid URL (SSRF blocked)."""
        result = scrape_careers_page('http://localhost/admin')
        assert result == []

    def test_scrape_adds_https(self):
        """Test that URLs without protocol get https added."""
        with patch('openjobs.scraper.scrape_with_firecrawl') as mock_fc:
            mock_fc.return_value = ''
            scrape_careers_page('example.com/careers')
            # URL should have been converted to https
            mock_fc.assert_called_once()

    @patch('openjobs.scraper.extract_jobs_from_markdown')
    @patch('openjobs.scraper.scrape_with_firecrawl')
    def test_scrape_generates_job_url_fallback(self, mock_firecrawl, mock_extract):
        """Test that jobs without URLs get fallback URL generated."""
        mock_firecrawl.return_value = '# Careers'
        mock_extract.return_value = [{'title': 'Engineer'}]  # No URL

        result = scrape_careers_page('https://example.com/careers')

        assert 'job_url' in result[0]
        assert 'example.com' in result[0]['job_url']
