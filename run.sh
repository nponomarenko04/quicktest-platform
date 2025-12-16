#!/bin/bash
set -e

echo "🚀 Starting QuickTest Platform..."

# Start services
docker compose up -d --build

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Install dependencies in test-runner
echo "📦 Installing dependencies..."
docker compose exec test-runner pip install -r requirements.txt
docker compose exec test-runner playwright install chromium firefox

# Run tests
echo "🧪 Running tests..."
docker compose exec test-runner pytest tests/ -v

# Generate reports
echo "📊 Generating reports..."
docker compose exec test-runner allure generate allure-results --clean -o results/allure-reports

echo ""
echo "✅ QuickTest Platform executed successfully!"
echo "📊 View reports:"
echo "   - HTML: results/report.html"
echo "   - Allure: results/allure-reports/index.html"
echo "   - Videos: results/videos/"
echo ""
echo "To stop: docker compose down"
