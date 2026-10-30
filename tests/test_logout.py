import pytest
import allure
from pages.login_page import LoginPage
from data.users import ADMIN_USER, MEMBER_USER

@allure.epic("PDHI Banten Portal")
@allure.feature("Logout")
class TestLogout:

    @pytest.mark.regression
    @allure.story("Admin Logout")
    @allure.title("Scenario: [Positive] Admin Success Logout")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_successful_logout_admin(self, login_page, page):
        """Scenario: Verify authenticated admin can log out and return to login page"""
        with allure.step(f"Login as admin ({ADMIN_USER.username})"):
            login_page.login_to_app(ADMIN_USER.username, ADMIN_USER.password)
            welcome_msg = login_page.get_welcome_text()
            assert ADMIN_USER.welcome_title in welcome_msg

        with allure.step("Perform logout from profile menu"):
            login_page.logout()

        with allure.step("Verify redirection to login page"):
            assert login_page.is_login_page_displayed(), "User should be redirected back to the login page"

    @pytest.mark.regression
    @allure.story("Member Logout")
    @allure.title("Scenario: [Positive] Member Success Logout")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_successful_logout_member(self, login_page, page):
        """Scenario: Verify authenticated member can log out and return to login page"""
        with allure.step(f"Login as member ({MEMBER_USER.username})"):
            login_page.login_to_app(MEMBER_USER.username, MEMBER_USER.password)
            welcome_msg = login_page.get_welcome_text()
            assert MEMBER_USER.welcome_title in welcome_msg

        with allure.step("Perform logout from profile menu"):
            login_page.logout()

        with allure.step("Verify redirection to login page"):
            assert login_page.is_login_page_displayed(), "User should be redirected back to the login page"
