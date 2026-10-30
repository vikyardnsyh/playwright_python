import pytest
import allure
from pages.login_page import LoginPage
from data.users import ADMIN_USER, MEMBER_USER

@allure.epic("PDHI Banten Portal")
@allure.feature("Authentication")
class TestLogin:

    @pytest.mark.sanity
    @allure.story("Admin Authentication")
    @allure.title("Scenario: [Positive] Admin Success Login")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_successful_login_admin(self, login_page, page):
        """Scenario: Verify admin can successfully log in with valid credentials"""
        with allure.step(f"Login with admin credentials for user '{ADMIN_USER.username}'"):
            login_page.login_to_app(ADMIN_USER.username, ADMIN_USER.password)

        with allure.step("Verify welcome message in dashboard profile dropdown"):
            welcome_msg = login_page.get_welcome_text()
            print(f"Dashboard admin welcome title : {welcome_msg}")
            assert ADMIN_USER.welcome_title in welcome_msg

    @pytest.mark.regression
    @allure.story("Member Authentication")
    @allure.title("Scenario: [Positive] Member Success Login")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_successful_login_member(self, login_page, page):
        """Scenario: Verify member/doctor can successfully log in with valid credentials"""
        with allure.step(f"Login with member credentials for user '{MEMBER_USER.username}'"):
            login_page.login_to_app(MEMBER_USER.username, MEMBER_USER.password)

        with allure.step("Verify welcome message in member profile dropdown"):
            welcome_msg = login_page.get_welcome_text()
            print(f"Dashboard member welcome title : {welcome_msg}")
            assert MEMBER_USER.welcome_title in welcome_msg

    @pytest.mark.regression
    @allure.story("Negative Authentication Scenarios")
    @allure.title("Scenario: [Negative] Login with Invalid Password")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_invalid_password(self, login_page, page):
        """Scenario: Verify login fails when using an incorrect password"""
        wrong_pwd = "WrongPassword999!"

        with allure.step(f"Attempt login with valid user '{ADMIN_USER.username}' and wrong password"):
            login_page.login_to_app(ADMIN_USER.username, wrong_pwd)

        with allure.step("Verify user is not authenticated and stays on login page"):
            assert not login_page.is_dashboard_displayed(timeout=3000), "Dashboard should not be visible"
            assert login_page.is_login_page_displayed(), "User should remain on the login page"

    @pytest.mark.regression
    @allure.story("Negative Authentication Scenarios")
    @allure.title("Scenario: [Negative] Login with Invalid Username")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_invalid_username(self, login_page, page):
        """Scenario: Verify login fails when using an unregistered username"""
        invalid_user = "unregistered_user_xyz"
        pwd = "AnyPassword123!"

        with allure.step("Attempt login with non-existent username"):
            login_page.login_to_app(invalid_user, pwd)

        with allure.step("Verify user is not authenticated"):
            assert not login_page.is_dashboard_displayed(timeout=3000), "Dashboard should not be visible"
            assert login_page.is_login_page_displayed(), "User should remain on the login page"

    @pytest.mark.regression
    @allure.story("Negative Authentication Scenarios")
    @allure.title("Scenario: [Negative] Login with Empty Credentials")
    @allure.severity(allure.severity_level.MINOR)
    def test_login_empty_credentials(self, login_page, page):
        """Scenario: Verify submission is prevented when credentials are empty"""
        with allure.step("Click login button without entering credentials"):
            login_page.click_login()

        with allure.step("Verify form prevents submission or dashboard is not accessed"):
            assert not login_page.is_dashboard_displayed(timeout=2000), "Dashboard should not be accessible"
            assert login_page.is_login_page_displayed(), "User should remain on login page"

    @pytest.mark.regression
    @allure.story("Negative Authentication Scenarios")
    @allure.title("Scenario: [Negative] Login with Empty Password")
    @allure.severity(allure.severity_level.MINOR)
    def test_login_empty_password(self, login_page, page):
        """Scenario: Verify login fails when password field is left blank"""
        with allure.step("Fill username and leave password blank"):
            login_page.login_to_app(user=ADMIN_USER.username, pwd="", submit=False)
            login_page.click_login()

        with allure.step("Verify submission fails and dashboard is not opened"):
            assert not login_page.is_dashboard_displayed(timeout=2000)
            assert login_page.is_login_page_displayed()

    @pytest.mark.regression
    @allure.story("Negative Authentication Scenarios")
    @allure.title("Scenario: [Negative] Login with Empty Username")
    @allure.severity(allure.severity_level.MINOR)
    def test_login_empty_username(self, login_page, page):
        """Scenario: Verify login fails when username field is left blank"""
        with allure.step("Leave username blank and fill password"):
            login_page.login_to_app(user="", pwd=ADMIN_USER.password, submit=False)
            login_page.click_login()

        with allure.step("Verify submission fails and user remains on login page"):
            assert not login_page.is_dashboard_displayed(timeout=2000)
            assert login_page.is_login_page_displayed()

    @pytest.mark.sanity
    @allure.story("Login Page UI Validation")
    @allure.title("Scenario: [UI] Verify Login Page Elements are Displayed")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_page_elements_visibility(self, login_page, page):
        """Scenario: Verify all mandatory elements are rendered on the login page"""
        with allure.step("Check visibility of username field"):
            assert login_page.is_visible(login_page._username_field), "Username field must be visible"

        with allure.step("Check visibility of password field"):
            assert login_page.is_visible(login_page._password_field), "Password field must be visible"

        with allure.step("Check visibility of login button"):
            assert login_page.is_visible(login_page._login_button), "Login button must be visible"

        with allure.step("Check page has a valid title"):
            title = page.title()
            print(f"Login page title: {title}")
            assert len(title) > 0, "Page title should not be empty"

    @pytest.mark.regression
    @allure.story("Login Page UI Validation")
    @allure.title("Scenario: [Security/UI] Verify Password Input Field is Masked")
    @allure.severity(allure.severity_level.NORMAL)
    def test_password_field_is_masked(self, login_page, page):
        """Scenario: Verify password input has type='password' to mask characters"""
        with allure.step("Inspect password field 'type' attribute"):
            input_type = login_page.get_password_field_type()
            assert input_type == "password", f"Expected 'password', got '{input_type}'"
