import os
from pages.base_page import BasePage

class AdminLaporanPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        # Page Header
        self._page_header = page.locator(".section-header h1:has-text('Laporan & Ekspor Data')")

        # Excel Export Section
        self._card_export_anggota = page.locator(".card:has-text('Data Seluruh Anggota')")
        self._btn_export_anggota = page.locator("form[action*='/adminLaporan/export'] button[name='anggota']")
        self._card_export_non_anggota = page.locator(".card:has-text('Data Non-Anggota')")
        self._btn_export_non_anggota = page.locator("form[action*='/adminLaporan/export'] button[name='nonanggota']")

        # PDF Search Section
        self._search_input = page.locator("input[name='cariDokter']")
        self._search_submit_btn = page.locator("button[type='submit']:has(.fa-search)")
        self._reset_search_btn = page.locator("a[title='Reset']")
        self._initial_search_prompt = page.locator(".card-body:has-text('Ketikkan nama dokter pada kolom pencarian')")

        # Table & Empty State
        self._table = page.locator("table.table")
        self._table_rows = page.locator("table tbody tr")
        self._empty_state = page.locator(".table-empty-state")
        self._btn_cetak_pdf = page.locator("button:has-text('Cetak PDF')")

    def navigate_to_page(self):
        """Navigate directly to the Laporan & Ekspor page."""
        base_url = (os.getenv("BASE_URL") or "http://127.0.0.1:8000").strip().rstrip('/')
        self.page.goto(f"{base_url}/adminLaporan")
        self.page.wait_for_load_state("domcontentloaded")

    def is_export_cards_displayed(self, timeout=5000):
        """Check if both Excel export cards are displayed."""
        return (
            self.is_visible(self._card_export_anggota, timeout=timeout) and
            self.is_visible(self._card_export_non_anggota, timeout=timeout)
        )

    def is_initial_prompt_displayed(self, timeout=3000):
        """Check if initial helper prompt is displayed before searching."""
        return self.is_visible(self._initial_search_prompt, timeout=timeout)

    def search_doctor_for_pdf(self, keyword):
        """Type doctor name and search to reveal PDF download actions."""
        self.type_text(self._search_input, keyword)
        self._search_input.press("Enter")
        self.page.wait_for_load_state("domcontentloaded")

    def reset_search(self):
        """Click reset search button."""
        self.click(self._reset_search_btn)
        self.page.wait_for_load_state("domcontentloaded")

    def is_doctor_present_in_results(self, doctor_name, timeout=3000):
        """Check if doctor row appears in search results table."""
        locator = self.page.locator(f"table tbody tr td:has-text('{doctor_name}')")
        return self.is_visible(locator, timeout=timeout)

    def is_empty_state_displayed(self, timeout=3000):
        """Check if empty state is visible."""
        return self.is_visible(self._empty_state, timeout=timeout)

    def get_empty_state_text(self):
        """Retrieve empty state message."""
        return self.get_text(self._empty_state)

    def get_results_row_count(self):
        """Count rows in the results table (excluding empty state)."""
        if self.is_empty_state_displayed(timeout=1000):
            return 0
        return self._table_rows.count()

    def get_first_pdf_button(self):
        """Get first 'Cetak PDF' button."""
        return self._btn_cetak_pdf.first
