import os
import pytest
from pages.login_page import LoginPage

@pytest.mark.sanity
def test_successful_login_admin(login_page, page):
    """Scenario: [Positive] Admin Success Login"""
    user = os.getenv("ADMIN_USER", "ayu")
    pwd = os.getenv("ADMIN_PASS", "rahasia")
    login_page.login_to_app(user, pwd)
    page.screenshot(path="screenshot_debug.png")
    print(page.url)
    welcome_msg = login_page.get_welcome_text()
    assert "HALLO ADMIN" in welcome_msg
    print(f"Dashboard admin welcome title : {welcome_msg}")

@pytest.mark.regression
def test_successful_login_member(login_page, page):
    """Scenario: [Positive] Member Success Login"""
    user = os.getenv("REG_USER", "aldy")
    pwd = os.getenv("REG_PASS", "PdhiBanten2!")
    login_page.login_to_app(user, pwd)
    page.screenshot(path="screenshot_debug.png")
    print(page.url)
    welcome_msg = login_page.get_welcome_text()
    assert "HALLO DOKTER" in welcome_msg
    print(f"Dashboard member welcome title : {welcome_msg}")