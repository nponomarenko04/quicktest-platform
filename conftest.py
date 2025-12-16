
import pytest
from playwright.sync_api import Page, sync_playwright
import allure


@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p


@pytest.fixture
def page(playwright_instance) -> Page:
    browser = playwright_instance.chromium.connect_over_cdp("ws://chrome:3000")
    page = browser.new_page()

    allure.dynamic.description(f"Browser: Chrome via browserless")

    yield page
    browser.close()


@pytest.fixture
def page_firefox(playwright_instance) -> Page:
    browser = playwright_instance.firefox.connect_over_cdp("ws://firefox:3000")
    page = browser.new_page()

    allure.dynamic.description(f"Browser: Firefox via browserless")

    yield page
    browser.close()


@pytest.fixture(autouse=True)
def attach_screenshot_on_failure(request, page):
    yield
    if request.node.rep_call.failed:
        screenshot = page.screenshot(full_page=True)

        allure.attach(
            screenshot,
            name=f"screenshot_{request.node.name}",
            attachment_type=allure.attachment_type.PNG
        )

        print(f"📸 Screenshot captured for failed test: {request.node.name}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)