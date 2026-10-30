import pytest
import allure

@allure.epic("PDHI Banten Portal")
@allure.feature("Admin - Administrasi Pendaftaran")
class TestAdminPendaftaran:

    @pytest.mark.sanity
    @allure.story("Pencarian Pendaftaran")
    @allure.title("Scenario: Search Registration by Doctor Name")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_existing_registration(self, admin_pendaftaran_page, page):
        """Verify searching for a registering doctor returns matching results."""
        keyword = "Ahmad"

        with allure.step(f"Search for registration with keyword '{keyword}'"):
            admin_pendaftaran_page.search_registration(keyword)

        with allure.step("Verify matched doctor appears in the results table"):
            assert not admin_pendaftaran_page.is_empty_state_displayed(), "Empty state should not be visible"
            assert admin_pendaftaran_page.get_table_row_count() > 0, "At least one registration should be found"
            assert admin_pendaftaran_page.is_doctor_present(keyword), f"Doctor '{keyword}' must appear in table"

    @pytest.mark.regression
    @allure.story("Pencarian Pendaftaran")
    @allure.title("Scenario: Search Registration with Non-Existent Name (Not Found)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_registration_not_found(self, admin_pendaftaran_page, page):
        """Verify searching for a non-existent registrant displays the empty state."""
        non_existent_key = "NonExistentRegistrant999"

        with allure.step(f"Search with non-existent keyword '{non_existent_key}'"):
            admin_pendaftaran_page.search_registration(non_existent_key)

        with allure.step("Verify empty state message is shown"):
            assert admin_pendaftaran_page.is_empty_state_displayed(), "Empty state should be displayed"
            empty_msg = admin_pendaftaran_page.get_empty_state_text()
            print(f"Empty state text: {empty_msg}")
            assert "tidak ada data" in empty_msg.lower() or "ditemukan" in empty_msg.lower()

    @pytest.mark.regression
    @allure.story("Pencarian Pendaftaran")
    @allure.title("Scenario: Reset Search Restores Full Registration List")
    @allure.severity(allure.severity_level.MINOR)
    def test_reset_search_restores_registration_list(self, admin_pendaftaran_page, page):
        """Verify clicking reset search restores the full list of registrations."""
        with allure.step("Perform empty search"):
            admin_pendaftaran_page.search_registration("NonExistentRegistrant999")
            assert admin_pendaftaran_page.is_empty_state_displayed()

        with allure.step("Click reset search button"):
            admin_pendaftaran_page.reset_search()

        with allure.step("Verify registration table records are restored"):
            assert not admin_pendaftaran_page.is_empty_state_displayed(), "Registrations list should be restored"
            assert admin_pendaftaran_page.get_table_row_count() > 0, "Row count should be greater than zero"

    @pytest.mark.regression
    @allure.story("Filter Pendaftaran")
    @allure.title("Scenario: Filter Registrations by Status 'Terverifikasi'")
    @allure.severity(allure.severity_level.NORMAL)
    def test_filter_registrations_terverifikasi(self, admin_pendaftaran_page, page):
        """Verify clicking 'Terverifikasi' filter displays only verified doctors."""
        with allure.step("Click 'Terverifikasi' filter button"):
            admin_pendaftaran_page.filter_by_terverifikasi()

        with allure.step("Verify URL query parameter and status badges"):
            assert "terverifikasi=terverifikasi" in page.url or "terverifikasi=" in page.url
            verified_badges = page.locator("table tbody tr .badge:has-text('Terverifikasi')")
            assert verified_badges.count() > 0, "At least one 'Terverifikasi' badge should be visible"

    @pytest.mark.regression
    @allure.story("Filter Pendaftaran")
    @allure.title("Scenario: Filter Registrations by Status 'Perlu Ditinjau'")
    @allure.severity(allure.severity_level.NORMAL)
    def test_filter_registrations_perlu_ditinjau(self, admin_pendaftaran_page, page):
        """Verify clicking 'Perlu Ditinjau' filter displays pending review registrations."""
        with allure.step("Click 'Perlu Ditinjau' filter button"):
            admin_pendaftaran_page.filter_by_perlu_ditinjau()

        with allure.step("Verify URL query parameter"):
            assert "tinjau=tinjau" in page.url or "tinjau=" in page.url

    @pytest.mark.regression
    @allure.story("Filter Pendaftaran")
    @allure.title("Scenario: Filter Registrations 'Semua' Restores Full List")
    @allure.severity(allure.severity_level.MINOR)
    def test_filter_registrations_semua(self, admin_pendaftaran_page, page):
        """Verify clicking 'Semua' shows all registrations."""
        with allure.step("Click 'Semua' filter button"):
            admin_pendaftaran_page.filter_by_semua()

        with allure.step("Verify registrations are displayed"):
            assert not admin_pendaftaran_page.is_empty_state_displayed()
            assert admin_pendaftaran_page.get_table_row_count() > 0

    @pytest.mark.sanity
    @allure.story("Halaman Verifikasi")
    @allure.title("Scenario: View Registration Verification & Document Inspection Page")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_view_verification_detail_page(self, admin_pendaftaran_page, page):
        """Verify clicking 'Verifikasi' opens the verification page with biodata and documents."""
        with allure.step("Click 'Verifikasi' button on the first registration row"):
            admin_pendaftaran_page.click_first_verification()

        with allure.step("Verify navigation to verification page"):
            page.wait_for_load_state("domcontentloaded")
            assert "/adminPendaftaran/" in page.url and "/edit" in page.url

        with allure.step("Verify biodata and document requirements cards are displayed"):
            assert admin_pendaftaran_page.is_verification_page_loaded(), "Verification page sections must be loaded"
            doc_count = admin_pendaftaran_page.get_documents_count()
            print(f"Total document requirement items rendered: {doc_count}")
            assert doc_count > 0, "Document requirements cards should be rendered"

    @pytest.mark.regression
    @allure.story("Halaman Verifikasi")
    @allure.title("Scenario: Cancel Verification and Return to Registration List")
    @allure.severity(allure.severity_level.NORMAL)
    def test_cancel_verification_returns_to_list(self, admin_pendaftaran_page, page):
        """Verify clicking 'Batal' on verification page returns to registration list."""
        with allure.step("Navigate to verification page"):
            admin_pendaftaran_page.click_first_verification()
            assert "/edit" in page.url

        with allure.step("Click 'Batal' button if present or navigate back"):
            admin_pendaftaran_page.navigate_to_page()

        with allure.step("Verify returned to registration list page"):
            assert page.url.rstrip('/').endswith("/adminPendaftaran")
            assert not admin_pendaftaran_page.is_empty_state_displayed()
            assert admin_pendaftaran_page.get_table_row_count() > 0
