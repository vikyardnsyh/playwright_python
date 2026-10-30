import pytest
import allure

@allure.epic("PDHI Banten Portal")
@allure.feature("Admin - Administrasi Data Dokter")
class TestAdminDokter:

    @pytest.mark.sanity
    @allure.story("Pencarian Dokter")
    @allure.title("Scenario: Search Doctor with Existing Name")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_existing_doctor(self, admin_dokter_page, page):
        """Verify searching for an existing doctor name returns matching results."""
        keyword = "Ahmad"

        with allure.step(f"Search for doctor with keyword '{keyword}'"):
            admin_dokter_page.search_doctor(keyword)

        with allure.step("Verify matched doctor appears in the results table"):
            assert not admin_dokter_page.is_empty_state_displayed(), "Empty state should not be visible"
            assert admin_dokter_page.get_table_row_count() > 0, "At least one doctor should be found"
            assert admin_dokter_page.is_doctor_present(keyword), f"Doctor containing '{keyword}' must appear in table"

    @pytest.mark.regression
    @allure.story("Pencarian Dokter")
    @allure.title("Scenario: Search Doctor with Non-Existent Name (Not Found)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_doctor_not_found(self, admin_dokter_page, page):
        """Verify searching for a non-existent doctor displays the empty state message."""
        non_existent_name = "DokterFiktif99999"

        with allure.step(f"Search with non-existent keyword '{non_existent_name}'"):
            admin_dokter_page.search_doctor(non_existent_name)

        with allure.step("Verify empty state message is shown"):
            assert admin_dokter_page.is_empty_state_displayed(), "Empty state should be displayed"
            empty_msg = admin_dokter_page.get_empty_state_text()
            print(f"Empty state text: {empty_msg}")
            assert "tidak ada data" in empty_msg.lower() or "ditemukan" in empty_msg.lower()

    @pytest.mark.regression
    @allure.story("Pencarian Dokter")
    @allure.title("Scenario: Reset Search Restores Full Doctor List")
    @allure.severity(allure.severity_level.MINOR)
    def test_reset_search_restores_doctor_list(self, admin_dokter_page, page):
        """Verify clicking reset search restores the full list of doctors."""
        with allure.step("Perform empty search"):
            admin_dokter_page.search_doctor("DokterFiktif99999")
            assert admin_dokter_page.is_empty_state_displayed()

        with allure.step("Click reset search button"):
            admin_dokter_page.reset_search()

        with allure.step("Verify doctor table records are restored"):
            assert not admin_dokter_page.is_empty_state_displayed(), "Doctor list should be restored"
            assert admin_dokter_page.get_table_row_count() > 0, "Rows should be greater than zero"

    @pytest.mark.regression
    @allure.story("Filter Dokter")
    @allure.title("Scenario: Filter Doctors by Status 'Terdaftar'")
    @allure.severity(allure.severity_level.NORMAL)
    def test_filter_doctors_terdaftar(self, admin_dokter_page, page):
        """Verify clicking 'Terdaftar' filter displays only registered doctors."""
        with allure.step("Click 'Terdaftar' filter button"):
            admin_dokter_page.filter_by_terdaftar()

        with allure.step("Verify URL query parameter and status badges"):
            assert "terdaftar=terdaftar" in page.url or "terdaftar=" in page.url
            terdaftar_badges = page.locator("table tbody tr .col-doctor-status .badge:has-text('Terdaftar')")
            assert terdaftar_badges.count() > 0, "At least one 'Terdaftar' badge should be visible"

    @pytest.mark.regression
    @allure.story("Filter Dokter")
    @allure.title("Scenario: Filter Doctors by Status 'Belum Terdaftar'")
    @allure.severity(allure.severity_level.NORMAL)
    def test_filter_doctors_belum_terdaftar(self, admin_dokter_page, page):
        """Verify clicking 'Belum Terdaftar' filter displays unverified/new doctors."""
        with allure.step("Click 'Belum Terdaftar' filter button"):
            admin_dokter_page.filter_by_belum_terdaftar()

        with allure.step("Verify URL query parameter"):
            assert "belumterdaftar=belumterdaftar" in page.url or "belumterdaftar=" in page.url

    @pytest.mark.regression
    @allure.story("Filter Dokter")
    @allure.title("Scenario: Filter Doctors 'Semua' Restores Full List")
    @allure.severity(allure.severity_level.MINOR)
    def test_filter_doctors_semua(self, admin_dokter_page, page):
        """Verify clicking 'Semua' shows all doctors."""
        with allure.step("Click 'Semua' filter button"):
            admin_dokter_page.filter_by_semua()

        with allure.step("Verify doctors are displayed"):
            assert not admin_dokter_page.is_empty_state_displayed()
            assert admin_dokter_page.get_table_row_count() > 0

    @pytest.mark.sanity
    @allure.story("Detail Dokter")
    @allure.title("Scenario: View Doctor Full Detail Profile Page")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_view_doctor_detail_page(self, admin_dokter_page, page):
        """Verify clicking Detail button opens the complete doctor profile."""
        with allure.step("Click 'Detail' button on the first doctor row"):
            admin_dokter_page.click_first_doctor_detail()

        with allure.step("Verify navigation to detail page"):
            page.wait_for_load_state("domcontentloaded")
            assert "/adminDokter/" in page.url and "/edit" in page.url

        with allure.step("Verify detail profile widgets and information are displayed"):
            assert admin_dokter_page.is_detail_page_loaded(), "Detail components should be visible"
            doctor_name = admin_dokter_page.get_detail_doctor_name()
            username = admin_dokter_page.get_detail_username()
            print(f"Viewing Detail Profile for: {doctor_name} ({username})")
            assert len(doctor_name) > 0, "Doctor name should not be empty"
            assert len(username) > 0, "Doctor username should not be empty"

    @pytest.mark.regression
    @allure.story("Detail Dokter")
    @allure.title("Scenario: Return to Doctor List from Detail Page")
    @allure.severity(allure.severity_level.NORMAL)
    def test_back_to_list_from_detail_page(self, admin_dokter_page, page):
        """Verify clicking 'Kembali ke Daftar Dokter' returns to the list table."""
        with allure.step("Navigate to doctor detail page"):
            admin_dokter_page.click_first_doctor_detail()
            assert "/edit" in page.url

        with allure.step("Click 'Kembali ke Daftar Dokter' button"):
            admin_dokter_page.click_back_to_list()

        with allure.step("Verify returned to doctor list page"):
            assert page.url.rstrip('/').endswith("/adminDokter"), "Should return to /adminDokter list"
            assert not admin_dokter_page.is_empty_state_displayed()
            assert admin_dokter_page.get_table_row_count() > 0
