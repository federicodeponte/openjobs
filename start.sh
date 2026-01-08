#!/bin/bash
# OpenJobs - Quick Start Script
# Starts Firecrawl locally using Docker

set -e

echo "🚀 OpenJobs - Starting Firecrawl..."
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed."
    echo ""
    echo "Please install Docker first:"
    echo "  - Mac: https://docs.docker.com/desktop/install/mac-install/"
    echo "  - Linux: https://docs.docker.com/engine/install/"
    echo "  - Windows: https://docs.docker.com/desktop/install/windows-install/"
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Start Firecrawl
echo "📦 Starting Firecrawl container..."
docker compose up -d

echo ""
echo "⏳ Waiting for Firecrawl to be ready..."
sleep 5

# Check if Firecrawl is responding
for i in {1..30}; do
    if curl -s http://localhost:3002 > /dev/null 2>&1; then
        echo ""
        echo "✅ Firecrawl is running at http://localhost:3002"
        echo ""
        echo "🎉 You're ready to use OpenJobs!"
        echo ""
        echo "Example:"
        echo "  export GOOGLE_API_KEY=your_key"
        echo "  python -c \"from openjobs import scrape_careers_page; print(scrape_careers_page('https://linear.app/careers'))\""
        echo ""
        echo "To stop Firecrawl:"
        echo "  docker compose down"
        exit 0
    fi
    sleep 1
done

echo "⚠️  Firecrawl is taking longer than expected to start."
echo "Check logs with: docker compose logs -f"
