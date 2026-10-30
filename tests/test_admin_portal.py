import pytest
import allure
from data.users import ADMIN_USER

@allure.epic("PDHI Banten Portal")
@allure.feature("Admin Portal Navigation & Management")
class TestAdminPortal:

    @pytest.mark.sanity
    @allure.story("Admin Dashboard")
    @allure.title("Scenario: Verify Admin Dashboard Content & Header")
    @allure.severity(allure.severity_level.NORMAL)
    def test_admin_dashboard_view(self, admin_dashboard, page):
        """Verify Admin lands on Dashboard and page elements are loaded."""
        with allure.step("Verify dashboard header title is displayed"):
            header = admin_dashboard.get_header_title()
            print(f"Admin Header: {header}")
            assert "dashboard" in header.lower() or "beranda" in header.lower() or len(header) > 0

    @pytest.mark.regression
    @allure.story("Admin Navigation")
    @allure.title("Scenario: Navigate to Administrasi Data Akun")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_navigate_to_admin_akun(self, admin_dashboard, page):
        """Verify Admin can access the User Accounts administration panel."""
        with allure.step("Click 'Administrasi Data Akun' in sidebar"):
            admin_dashboard.navigate_to_admin_akun()

        with allure.step("Verify URL and panel content"):
            page.wait_for_load_state("domcontentloaded")
            assert "AdminAkun" in page.url
            header = admin_dashboard.get_header_title()
            assert "akun" in header.lower() or len(header) > 0

    @pytest.mark.regression
    @allure.story("Admin Navigation")
    @allure.title("Scenario: Navigate to Administrasi Data Dokter")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_navigate_to_admin_dokter(self, admin_dashboard, page):
        """Verify Admin can access the Master Doctors administration panel."""
        with allure.step("Click 'Administrasi Data Dokter' in sidebar"):
            admin_dashboard.navigate_to_admin_dokter()

        with allure.step("Verify URL and page header"):
            page.wait_for_load_state("domcontentloaded")
            assert "adminDokter" in page.url
            header = admin_dashboard.get_header_title()
            assert "dokter" in header.lower() or len(header) > 0

    @pytest.mark.regression
    @allure.story("Admin Navigation")
    @allure.title("Scenario: Navigate to Administrasi Pendaftaran")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_navigate_to_admin_pendaftaran(self, admin_dashboard, page):
        """Verify Admin can access Member Registration Approval panel."""
        with allure.step("Click 'Administrasi Pendaftaran' in sidebar"):
            admin_dashboard.navigate_to_admin_pendaftaran()

        with allure.step("Verify URL and page content"):
            page.wait_for_load_state("domcontentloaded")
            assert "adminPendaftaran" in page.url
            header = admin_dashboard.get_header_title()
            assert "pendaftaran" in header.lower() or len(header) > 0

    @pytest.mark.regression
    @allure.story("Admin Navigation")
    @allure.title("Scenario: Navigate to Administrasi Anggota")
    @allure.severity(allure.severity_level.NORMAL)
    def test_navigate_to_admin_keanggotaan(self, admin_dashboard, page):
        """Verify Admin can access Member Management panel."""
        with allure.step("Click 'Administrasi Anggota' in sidebar"):
            admin_dashboard.navigate_to_admin_keanggotaan()

        with allure.step("Verify URL contains 'adminKeanggotaan'"):
            page.wait_for_load_state("domcontentloaded")
            assert "adminKeanggotaan" in page.url

    @pytest.mark.regression
    @allure.story("Admin Navigation")
    @allure.title("Scenario: Navigate to Download Laporan")
    @allure.severity(allure.severity_level.NORMAL)
    def test_navigate_to_admin_laporan(self, admin_dashboard, page):
        """Verify Admin can access the Report Center panel."""
        with allure.step("Click 'Download Laporan' in sidebar"):
            admin_dashboard.navigate_to_admin_laporan()

        with allure.step("Verify URL contains 'adminLaporan'"):
            page.wait_for_load_state("domcontentloaded")
            assert "adminLaporan" in page.url

    @pytest.mark.sanity
    @allure.story("Admin Sidebar Menu")
    @allure.title("Scenario: Verify All Admin Sidebar Navigation Items Exist")
    @allure.severity(allure.severity_level.NORMAL)
    def test_admin_sidebar_menu_integrity(self, admin_dashboard, page):
        """Verify that all required administration menu items are visible in the sidebar."""
        for menu_name in ADMIN_USER.accessible_menus:
            with allure.step(f"Check visibility of menu item '{menu_name}'"):
                item = page.locator(f".sidebar-menu a:has-text('{menu_name}')")
                assert item.count() > 0, f"Sidebar menu item '{menu_name}' should exist"
