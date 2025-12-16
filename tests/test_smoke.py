#!/usr/bin/env python3
"""
QuickTest Platform - Smoke Tests
Author: QA Engineer
"""

import pytest
from playwright.sync_api import Page, expect

class TestSmoke:
    """Basic smoke tests for QuickTest Platform"""
    
    def test_website_loads(self, page: Page):
        """Test that demo website loads correctly"""
        page.goto("http://test-website:80")
        expect(page).to_have_title("QuickTest Demo Site")
        
        # Check main sections exist
        expect(page.locator("h1")).to_contain_text("QuickTest Platform")
        expect(page.get_by_text("Login Form")).to_be_visible()
        expect(page.get_by_text("Product Catalog")).to_be_visible()
        
        print("✅ Website loads correctly")
    
    def test_login_form(self, page: Page):
        """Test login form functionality"""
        page.goto("http://test-website:80")
        
        # Fill form
        page.fill("#username", "testuser")
        page.fill("#password", "password123")
        page.click("#login-btn")
        
        # Verify success message
        message = page.locator("#login-message")
        expect(message).to_contain_text("Login successful!")
        
        print("✅ Login form works")
    
    def test_add_to_cart(self, page: Page):
        """Test shopping cart functionality"""
        page.goto("http://test-website:80")
        
        # Initial cart is empty
        cart_count = page.locator("#cart-count")
        expect(cart_count).to_have_text("0")
        
        # Add product to cart
        page.click("button.add-to-cart[data-id='1']")
        
        # Verify cart updated
        expect(cart_count).to_have_text("1")
        
        print("✅ Add to cart works")

def test_simple_check():
    """Simple test without browser"""
    print("✅ Simple test passed")
