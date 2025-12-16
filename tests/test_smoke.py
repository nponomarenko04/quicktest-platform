"""
QuickTest Platform - Smoke Tests
Author: [Your Name]
Date: $(date)
"""

import pytest
from playwright.sync_api import Page, expect
import requests


class TestSmoke:

    def test_website_loads(self, page: Page):
        page.goto("http://test-website:80")
        expect(page).to_have_title("QuickTest Demo Site")

        expect(page.locator("h1")).to_contain_text("QuickTest Platform")
        expect(page.get_by_text("Login Form")).to_be_visible()
        expect(page.get_by_text("Product Catalog")).to_be_visible()

        print("✅ Website loads correctly")

    def test_login_form(self, page: Page):
        page.goto("http://test-website:80")

        page.fill("#username", "testuser")
        page.fill("#password", "password123")
        page.click("#login-btn")

        message = page.locator("#login-message")
        expect(message).to_contain_text("Login successful!")

        print("✅ Login form works")

    def test_add_to_cart(self, page: Page):
        page.goto("http://test-website:80")

        cart_count = page.locator("#cart-count")
        expect(cart_count).to_have_text("0")

        page.click("button.add-to-cart[data-id='1']")

        expect(cart_count).to_have_text("1")

        print("✅ Add to cart works")

    def test_mock_api(self):
        response = requests.get("http://mock-api:1080")
        assert response.status_code in [200, 404, 400]  # MockServer responds

        print("✅ Mock API server is reachable")


@pytest.mark.chrome
def test_chrome_browser(page: Page):
    page.goto("http://test-website:80")
    title = page.title()
    assert "QuickTest" in title
    print(f"✅ Chrome test passed: {title}")


@pytest.mark.firefox
def test_firefox_browser(page_firefox: Page):
    page_firefox.goto("http://test-website:80")
    title = page_firefox.title()
    assert "QuickTest" in title
    print(f"✅ Firefox test passed: {title}")
