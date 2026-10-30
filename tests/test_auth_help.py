import pytest
import allure

@allure.epic("PDHI Banten Portal")
@allure.feature("Bantuan Akses & Akun")
class TestAuthHelp:

    @pytest.mark.sanity
    @allure.story("Pengajuan Akun Baru")
    @allure.title("Scenario: Navigate to 'Ajukan Akun Baru' from Login Page")
    @allure.severity(allure.severity_level.NORMAL)
    def test_navigate_to_pengajuan_akun_from_login(self, login_page, auth_help_page, page):
        """Verify user can access account application procedure page from login footer."""
        with allure.step("Click 'Ajukan Akun Baru' link on login page"):
            login_page.click_ajukan_akun_baru()

        with allure.step("Verify navigation to /pengajuanAkun"):
            assert "pengajuanAkun" in page.url
            assert auth_help_page.is_pengajuan_akun_loaded()

    @pytest.mark.regression
    @allure.story("Pengajuan Akun Baru")
    @allure.title("Scenario: Verify WhatsApp Secretariat Link on Pengajuan Akun Page")
    @allure.severity(allure.severity_level.NORMAL)
    def test_pengajuan_akun_whatsapp_contact_button(self, auth_help_page, page):
        """Verify WhatsApp contact button points to official secretariat number."""
        with allure.step("Navigate to /pengajuanAkun"):
            auth_help_page.navigate_to_pengajuan_akun()

        with allure.step("Inspect WhatsApp contact link"):
            wa_href = auth_help_page.get_whatsapp_href(page_type="pengajuan")
            print(f"WhatsApp URL: {wa_href}")
            assert wa_href is not None
            assert "wa.me" in wa_href
            assert "62895346222492" in wa_href

    @pytest.mark.regression
    @allure.story("Pengajuan Akun Baru")
    @allure.title("Scenario: Return to Login Page from Pengajuan Akun Page")
    @allure.severity(allure.severity_level.MINOR)
    def test_back_to_login_from_pengajuan_akun(self, auth_help_page, login_page, page):
        """Verify user can return to login page from account application page."""
        with allure.step("Navigate to /pengajuanAkun"):
            auth_help_page.navigate_to_pengajuan_akun()

        with allure.step("Click 'Kembali ke Halaman Login'"):
            auth_help_page.click_back_to_login()

        with allure.step("Verify returned to login page"):
            assert "login" in page.url or page.url.endswith("/")
            assert login_page.is_login_page_displayed()

    @pytest.mark.sanity
    @allure.story("Lupa Password")
    @allure.title("Scenario: Navigate to 'Lupa Password?' from Login Page")
    @allure.severity(allure.severity_level.NORMAL)
    def test_navigate_to_lupa_password_from_login(self, login_page, auth_help_page, page):
        """Verify user can access password reset guidance page from login form."""
        with allure.step("Click 'Lupa Password?' link on login form"):
            login_page.click_lupa_password()

        with allure.step("Verify navigation to /lupaPassword"):
            assert "lupaPassword" in page.url
            assert auth_help_page.is_lupa_password_loaded()

    @pytest.mark.regression
    @allure.story("Lupa Password")
    @allure.title("Scenario: Verify WhatsApp Secretariat Link on Lupa Password Page")
    @allure.severity(allure.severity_level.NORMAL)
    def test_lupa_password_whatsapp_contact_button(self, auth_help_page, page):
        """Verify WhatsApp reset password link contains pre-filled message parameter."""
        with allure.step("Navigate to /lupaPassword"):
            auth_help_page.navigate_to_lupa_password()

        with allure.step("Inspect WhatsApp reset request link"):
            wa_href = auth_help_page.get_whatsapp_href(page_type="lupa_password")
            print(f"WhatsApp Reset URL: {wa_href}")
            assert wa_href is not None
            assert "wa.me" in wa_href
            assert "password" in wa_href.lower()

    @pytest.mark.regression
    @allure.story("Lupa Password")
    @allure.title("Scenario: Return to Login Page from Lupa Password Page")
    @allure.severity(allure.severity_level.MINOR)
    def test_back_to_login_from_lupa_password(self, auth_help_page, login_page, page):
        """Verify user can return to login page from forgot password page."""
        with allure.step("Navigate to /lupaPassword"):
            auth_help_page.navigate_to_lupa_password()

        with allure.step("Click 'Kembali ke Halaman Login'"):
            auth_help_page.click_back_to_login()

        with allure.step("Verify returned to login page"):
            assert "login" in page.url or page.url.endswith("/")
            assert login_page.is_login_page_displayed()
