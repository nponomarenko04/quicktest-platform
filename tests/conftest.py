import pytest
from playwright.sync_api import Page, sync_playwright

@pytest.fixture(scope="session")
def playwright_instance():
    """Global playwright instance"""
    with sync_playwright() as p:
        yield p

@pytest.fixture
def page(playwright_instance) -> Page:
    """Page fixture for Chrome"""
    # Подключаемся к browserless Chrome
    browser = playwright_instance.chromium.connect_over_cdp("ws://chrome:3000")
    page = browser.new_page()
    yield page
    browser.close()
