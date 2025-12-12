from playwright.sync_api import Page, expect

def test_website_loads(page: Page):
    page.goto("http://localhost:8080")
    expect(page).to_have_title("Test Application")

def test_button_click(page: Page):
    page.goto("http://localhost:8080")
    button = page.locator("#test-btn")
    expect(button).to_have_text("Click me")
    button.click()
    expect(button).to_have_text("Clicked!")