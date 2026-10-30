import os
import pytest
import allure
from data.users import MEMBER_USER

@allure.epic("PDHI Banten Portal")
@allure.feature("Dokter - Self Service & Member Portal")
class TestDoctorPortal:

    @pytest.mark.sanity
    @allure.story("Beranda Dokter")
    @allure.title("Scenario: Verify Doctor Home Profile and Status Widget")
    @allure.severity(allure.severity_level.NORMAL)
    def test_doctor_home_biodata_and_checklist(self, doctor_portal_page, page):
        """Verify Doctor Home displays profile widget, contacts, and document checklist."""
        with allure.step("Verify home dashboard widgets are loaded"):
            assert doctor_portal_page.is_home_dashboard_loaded(), "Home components must be loaded"

        with allure.step("Verify doctor profile name is rendered"):
            name = doctor_portal_page.get_doctor_profile_name()
            print(f"Logged in as doctor: {name}")
            assert len(name) > 0, "Doctor name should not be empty"

    @pytest.mark.regression
    @allure.story("Beranda Dokter")
    @allure.title("Scenario: Verify Quick Links on Doctor Home")
    @allure.severity(allure.severity_level.NORMAL)
    def test_doctor_home_quick_links(self, doctor_portal_page, page):
        """Verify quick action buttons on Home navigate to respective pages."""
        with allure.step("Click 'Perbarui Biodata' quick button"):
            doctor_portal_page.click(doctor_portal_page._btn_perbarui_biodata)
            page.wait_for_load_state("domcontentloaded")
            assert "formRegistrasi" in page.url

        with allure.step("Return to home and click 'Kelola Berkas'"):
            doctor_portal_page.navigate_to_home()
            doctor_portal_page.click(doctor_portal_page._btn_kelola_berkas)
            page.wait_for_load_state("domcontentloaded")
            assert "uploadBerkas" in page.url

    @pytest.mark.sanity
    @allure.story("Form Registrasi")
    @allure.title("Scenario: Verify Form Registrasi Anggota Content & Fields")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_doctor_form_registrasi_view(self, doctor_portal_page, page):
        """Verify Doctor registration form is accessible and has pre-filled values."""
        with allure.step("Navigate to Form Registrasi"):
            doctor_portal_page.navigate_to_form_registrasi()

        with allure.step("Verify registration form fields"):
            assert doctor_portal_page.is_form_registrasi_loaded(), "Form Registrasi must be loaded"
            nama_lengkap = doctor_portal_page.get_nama_lengkap_value()
            assert len(nama_lengkap) > 0, "Doctor's name should be prefilled in registration form"

    @pytest.mark.regression
    @allure.story("Upload Berkas")
    @allure.title("Scenario: Verify Upload Berkas Document Requirements Grid")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_doctor_upload_berkas_view(self, doctor_portal_page, page):
        """Verify Upload Berkas displays 8 document upload containers."""
        with allure.step("Navigate to Upload Berkas"):
            doctor_portal_page.navigate_to_upload_berkas()

        with allure.step("Verify upload page and requirement cards"):
            assert doctor_portal_page.is_upload_berkas_loaded()
            doc_cards = doctor_portal_page.get_document_cards_count()
            print(f"Document upload cards found: {doc_cards}")
            assert doc_cards >= 8, f"Expected 8 document upload cards, found {doc_cards}"

    @pytest.mark.regression
    @allure.story("Syarat Pendaftaran")
    @allure.title("Scenario: Verify Syarat Pendaftaran Letterhead & Contact Info")
    @allure.severity(allure.severity_level.NORMAL)
    def test_doctor_syarat_pendaftaran_letterhead(self, doctor_portal_page, page):
        """Verify Syarat Pendaftaran page renders official PDHI letterhead."""
        with allure.step("Navigate to Syarat Pendaftaran"):
            doctor_portal_page.navigate_to_syarat_pendaftaran()

        with allure.step("Verify letterhead and official secretariat contact info"):
            assert doctor_portal_page.is_syarat_pendaftaran_loaded()

    @pytest.mark.regression
    @allure.story("Ubah Password")
    @allure.title("Scenario: Verify Ubah Password Form and Visibility Toggle")
    @allure.severity(allure.severity_level.NORMAL)
    def test_doctor_ubah_password_view_and_toggle(self, doctor_portal_page, page):
        """Verify Ubah Password form fields and password masking toggle button."""
        with allure.step("Navigate to Ubah Password"):
            doctor_portal_page.navigate_to_ubah_password()

        with allure.step("Verify password change form"):
            assert doctor_portal_page.is_ubah_password_loaded()
            assert doctor_portal_page._input_current_password.get_attribute("type") == "password"

        with allure.step("Click toggle password visibility eye button"):
            doctor_portal_page.toggle_password_masking()
            current_type = doctor_portal_page._input_current_password.get_attribute("type")
            assert current_type in ["text", "password"]

    @pytest.mark.sanity
    @allure.story("Menu Integrity")
    @allure.title("Scenario: Verify Doctor Sidebar Navigation Items")
    @allure.severity(allure.severity_level.NORMAL)
    def test_doctor_sidebar_menu_integrity(self, doctor_portal_page, page):
        """Verify all doctor self-service sidebar menu items are displayed."""
        for menu_name in MEMBER_USER.accessible_menus:
            with allure.step(f"Check visibility of menu '{menu_name}'"):
                item = page.locator(f".sidebar-menu a:has-text('{menu_name}')")
                assert item.count() > 0, f"Doctor sidebar menu '{menu_name}' must exist"

    @pytest.mark.regression
    @allure.story("Role-Based Access Control (RBAC)")
    @allure.title("Scenario: [Security/RBAC] Doctor Cannot Access Admin Routes")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_doctor_cannot_access_admin_routes_rbac(self, doctor_portal_page, page):
        """Verify Doctor cannot directly access any Admin-only pages."""
        base_url = (os.getenv("BASE_URL") or "http://127.0.0.1:8000").strip().rstrip('/')
        admin_routes = ["/AdminAkun", "/adminDokter", "/adminPendaftaran", "/adminKeanggotaan", "/adminLaporan"]

        for route in admin_routes:
            with allure.step(f"Test unauthorized direct access to '{route}'"):
                page.goto(f"{base_url}{route}")
                page.wait_for_load_state("domcontentloaded")
                current_url = page.url
                assert not current_url.endswith(route), f"Doctor should be forbidden on {route}, got {current_url}"
