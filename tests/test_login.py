import os
import pytest
from pages.login_page import LoginPage

@pytest.mark.sanity
def test_successful_login_admin(login_admin):
    """Scenario: [Positive] Admin Success Login"""
    page = login_admin
    assert page.locator("text=HALLO ADMIN").is_visible()

@pytest.mark.regression
def test_successful_login_member(login_users):
    """Scenario: [Positive] Member Success Login"""
    page = login_users
    assert page.locator("text=HALLO DOKTER").is_visible()