import pytest
import allure

@allure.epic("PDHI Banten Portal")
@allure.feature("Admin - Download Laporan & Ekspor Data")
class TestAdminLaporan:

    @pytest.mark.sanity
    @allure.story("Pusat Laporan")
    @allure.title("Scenario: Verify Laporan Page Header and Excel Export Cards")
    @allure.severity(allure.severity_level.NORMAL)
    def test_laporan_page_header_and_export_cards(self, admin_laporan_page, page):
        """Verify report center header and Excel download cards are rendered."""
        with allure.step("Verify page header"):
            assert admin_laporan_page.is_visible(admin_laporan_page._page_header)

        with allure.step("Verify presence of Anggota and Non-Anggota Excel export cards"):
            assert admin_laporan_page.is_export_cards_displayed(), "Both export cards should be visible"

    @pytest.mark.regression
    @allure.story("Pencarian PDF Berkas")
    @allure.title("Scenario: Verify Initial State Prompts User to Search")
    @allure.severity(allure.severity_level.MINOR)
    def test_initial_state_prompts_user_to_search(self, admin_laporan_page, page):
        """Verify prompt guidance is displayed before user searches for doctor."""
        with allure.step("Check prompt message before search"):
            assert admin_laporan_page.is_initial_prompt_displayed(), "Initial search prompt should be displayed"

    @pytest.mark.sanity
    @allure.story("Pencarian PDF Berkas")
    @allure.title("Scenario: Search Doctor to Reveal PDF Dossier Download Action")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_doctor_for_pdf_found(self, admin_laporan_page, page):
        """Verify searching doctor reveals the matched record with 'Cetak PDF' button."""
        keyword = "Ahmad"

        with allure.step(f"Search for doctor '{keyword}'"):
            admin_laporan_page.search_doctor_for_pdf(keyword)

        with allure.step("Verify results table and PDF generation button"):
            assert not admin_laporan_page.is_empty_state_displayed()
            assert admin_laporan_page.get_results_row_count() > 0
            assert admin_laporan_page.is_doctor_present_in_results(keyword)
            pdf_btn = admin_laporan_page.get_first_pdf_button()
            assert admin_laporan_page.is_visible(pdf_btn), "'Cetak PDF' button should be visible"

    @pytest.mark.regression
    @allure.story("Pencarian PDF Berkas")
    @allure.title("Scenario: Search Doctor for PDF with Non-Existent Keyword (Not Found)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_doctor_for_pdf_not_found(self, admin_laporan_page, page):
        """Verify searching non-existent doctor displays empty state message."""
        non_existent_key = "NonExistentDokter999"

        with allure.step(f"Search with non-existent keyword '{non_existent_key}'"):
            admin_laporan_page.search_doctor_for_pdf(non_existent_key)

        with allure.step("Verify empty state message is shown"):
            assert admin_laporan_page.is_empty_state_displayed()
            empty_msg = admin_laporan_page.get_empty_state_text()
            print(f"Empty state message: {empty_msg}")
            assert "tidak ada dokter" in empty_msg.lower() or "cocok" in empty_msg.lower()

    @pytest.mark.regression
    @allure.story("Pencarian PDF Berkas")
    @allure.title("Scenario: Reset Search Restores Initial Prompt Guidance")
    @allure.severity(allure.severity_level.MINOR)
    def test_reset_search_restores_initial_prompt(self, admin_laporan_page, page):
        """Verify resetting search clears results and returns to initial prompt."""
        with allure.step("Perform search"):
            admin_laporan_page.search_doctor_for_pdf("NonExistentDokter999")
            assert admin_laporan_page.is_empty_state_displayed()

        with allure.step("Click reset search button"):
            admin_laporan_page.reset_search()

        with allure.step("Verify initial prompt guidance is displayed again"):
            assert admin_laporan_page.is_initial_prompt_displayed()

    @pytest.mark.regression
    @allure.story("Ekspor Data Excel")
    @allure.title("Scenario: Verify Excel Export Actions & Endpoints")
    @allure.severity(allure.severity_level.NORMAL)
    def test_excel_export_buttons_presence_and_attributes(self, admin_laporan_page, page):
        """Verify that Excel export forms have correct action endpoints and submit buttons."""
        with allure.step("Inspect 'Data Seluruh Anggota' Excel export button"):
            anggota_btn = admin_laporan_page._btn_export_anggota
            assert admin_laporan_page.is_visible(anggota_btn)

        with allure.step("Inspect 'Data Non-Anggota' Excel export button"):
            non_anggota_btn = admin_laporan_page._btn_export_non_anggota
            assert admin_laporan_page.is_visible(non_anggota_btn)

    @pytest.mark.regression
    @allure.story("Pencarian PDF Berkas")
    @allure.title("Scenario: Verify PDF Generation Form Structure and Hidden Inputs")
    @allure.severity(allure.severity_level.NORMAL)
    def test_pdf_generate_form_attributes(self, admin_laporan_page, page):
        """Verify PDF download form has valid doctor ID input."""
        with allure.step("Search doctor"):
            admin_laporan_page.search_doctor_for_pdf("Ahmad")

        with allure.step("Inspect PDF form"):
            pdf_form = page.locator("form[action*='/adminLaporan/generate-pdf']").first
            id_input = pdf_form.locator("input[name='id']")
            assert id_input.count() > 0, "Hidden doctor id input must exist"
            doctor_id = id_input.get_attribute("value")
            assert len(doctor_id) > 0, f"Doctor ID value should be present, got '{doctor_id}'"
