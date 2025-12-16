#!/bin/bash
set -e

echo "🚀 Starting QuickTest Platform..."

mkdir -p tests results/{videos,screenshots,allure-reports} demo-site allure-results

if [ ! -f "demo-site/index.html" ]; then
  cat > demo-site/index.html << 'SITE'
<!DOCTYPE html>
<html>
<head>
    <title>QuickTest Demo</title>
    <style>
        body { font-family: Arial; padding: 40px; }
        button { background: #4CAF50; color: white; padding: 15px; border: none; cursor: pointer; margin: 10px; }
        .result { padding: 15px; margin: 10px 0; background: #f0f0f0; }
    </style>
</head>
<body>
    <h1>✅ QuickTest Platform Demo</h1>
    
    <div>
        <button id="test-btn">Click Me</button>
        <div id="result" class="result">Click the button</div>
    </div>
    
    <div>
        <input type="text" id="input-field" placeholder="Type something">
        <button id="submit-btn">Submit</button>
    </div>
    
    <script>
        document.getElementById('test-btn').onclick = function() {
            document.getElementById('result').innerHTML = 'Button clicked! 🎉';
        };
        
        document.getElementById('submit-btn').onclick = function() {
            const value = document.getElementById('input-field').value;
            document.getElementById('result').innerHTML = 'You typed: ' + value;
        };
    </script>
</body>
</html>
SITE
fi

echo "🐳 Starting Docker services..."
docker compose down 2>/dev/null || true
docker compose up -d --build

echo "⏳ Waiting for services to start..."
sleep 8

echo "🔍 Checking Chrome..."
curl -s http://localhost:3000/json/version 2>/dev/null && echo "✅ Chrome is running" || echo "⚠️  Chrome check failed"

echo "🔍 Checking website..."
curl -s http://localhost:8080 | grep -q "QuickTest" && echo "✅ Website is running" || echo "⚠️  Website check failed"

echo "📦 Installing dependencies..."
docker compose exec -T test-runner bash << 'INSTALL'
pip install --upgrade pip
pip install playwright==1.45.0 pytest==7.4.4 pytest-playwright==0.4.3 allure-pytest==2.13.2
playwright install chromium
echo "✅ Dependencies installed"
INSTALL

if [ ! -f "tests/test_smoke.py" ]; then
  cat > tests/test_smoke.py << 'TEST'
import pytest
from playwright.sync_api import Page, expect

def test_website_loads(page: Page):
    """Test that the website loads"""
    page.goto("http://test-website:80")
    expect(page).to_have_title("QuickTest Demo")
    print("✅ Website loaded")

def test_button_click(page: Page):
    """Test button click functionality"""
    page.goto("http://test-website:80")
    
    # Click button
    page.click("#test-btn")
    
    # Check result
    result = page.locator("#result")
    expect(result).to_contain_text("Button clicked!")
    print("✅ Button click works")

def test_input_field(page: Page):
    """Test input field functionality"""
    page.goto("http://test-website:80")
    
    # Type text
    page.fill("#input-field", "Hello from test!")
    page.click("#submit-btn")
    
    # Check result
    result = page.locator("#result")
    expect(result).to_contain_text("Hello from test!")
    print("✅ Input field works")

if __name__ == "__main__":
    print("Run with: pytest tests/test_smoke.py -v")
TEST
fi

echo "🧪 Running tests..."
docker compose exec test-runner pytest tests/test_smoke.py -v

echo ""
echo "📊 Test execution completed!"
echo "To view the website: http://localhost:8080"
echo "To view Chrome DevTools: http://localhost:3000"
echo "To stop: docker compose down"
