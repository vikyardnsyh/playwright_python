import os
from pages.base_page import BasePage

class AdminAnggotaPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        # Search & Reset Locators
        self._search_input = page.locator("input[name='cariDokter']")
        self._search_submit_btn = page.locator("button[type='submit']:has(.fa-search)")
        self._reset_search_btn = page.locator("a[title='Reset Pencarian']")

        # Filter Buttons
        self._filter_semua_btn = page.locator("button[name='semua']")
        self._filter_aktif_btn = page.locator("button[name='aktif']")
        self._filter_nonaktif_btn = page.locator("button[name='nonaktif']")

        # Table & Rows
        self._table = page.locator("table.table")
        self._table_rows = page.locator("table tbody tr")
        self._empty_state = page.locator(".table-empty-state")
        self._total_count_badge = page.locator(".table-control-count .badge")

        # Kelola / Perpanjang Page Locators
        self._kelola_header = page.locator(".section-header h1:has-text('Kelola Keanggotaan')")
        self._current_status_card = page.locator(".card:has-text('Status Keanggotaan Saat Ini')")
        self._extension_card = page.locator(".card:has-text('Perpanjang / Ubah Domisili')")
        self._select_domisili = page.locator("select[name='domisili_anggota']")
        self._select_masa_aktif = page.locator("select[name='masa_aktif']")
        self._btn_submit_update = page.locator("button[type='submit']:has-text('Simpan Perubahan')")
        self._btn_batal = page.locator("a:has-text('Batal')")

    def navigate_to_page(self):
        """Navigate directly to the Administrasi Anggota page."""
        base_url = (os.getenv("BASE_URL") or "http://127.0.0.1:8000").strip().rstrip('/')
        self.page.goto(f"{base_url}/adminKeanggotaan")
        self.page.wait_for_load_state("domcontentloaded")

    def search_member(self, keyword):
        """Type keyword and trigger search."""
        self.type_text(self._search_input, keyword)
        self._search_input.press("Enter")
        self.page.wait_for_load_state("domcontentloaded")

    def reset_search(self):
        """Click reset search button."""
        self.click(self._reset_search_btn)
        self.page.wait_for_load_state("domcontentloaded")

    def filter_by_semua(self):
        """Click 'Semua' filter button."""
        self.click(self._filter_semua_btn)
        self.page.wait_for_load_state("domcontentloaded")

    def filter_by_aktif(self):
        """Click 'Aktif' filter button."""
        self.click(self._filter_aktif_btn)
        self.page.wait_for_load_state("domcontentloaded")

    def filter_by_nonaktif(self):
        """Click 'Non Aktif' filter button."""
        self.click(self._filter_nonaktif_btn)
        self.page.wait_for_load_state("domcontentloaded")

    def click_first_manage_member(self):
        """Click 'Kelola' button on the first member row."""
        first_btn = self.page.locator("table tbody tr a:has-text('Kelola')").first
        first_btn.wait_for(state="visible", timeout=5000)
        self.click(first_btn)
        self.page.wait_for_load_state("domcontentloaded")

    def click_manage_by_member_name(self, member_name):
        """Click 'Kelola' button for a specific member matching member_name."""
        row = self.page.locator(f"table tbody tr:has(td:has-text('{member_name}'))")
        btn = row.locator("a:has-text('Kelola')")
        self.click(btn)
        self.page.wait_for_load_state("domcontentloaded")

    def is_member_present(self, member_name, timeout=3000):
        """Check if member name exists in the table."""
        locator = self.page.locator(f"table tbody tr td:has-text('{member_name}')")
        return self.is_visible(locator, timeout=timeout)

    def is_empty_state_displayed(self, timeout=3000):
        """Check if table empty state is visible."""
        return self.is_visible(self._empty_state, timeout=timeout)

    def get_empty_state_text(self):
        """Retrieve empty state message."""
        return self.get_text(self._empty_state)

    def get_table_row_count(self):
        """Count rows in the member table (excluding empty state)."""
        if self.is_empty_state_displayed(timeout=1000):
            return 0
        return self._table_rows.count()

    # ------------------ Kelola / Perpanjang Page Helpers ------------------
    def is_manage_page_loaded(self, timeout=5000):
        """Check if Kelola Keanggotaan page components are loaded."""
        return (
            self.is_visible(self._kelola_header, timeout=timeout) and
            self.is_visible(self._current_status_card, timeout=timeout) and
            self.is_visible(self._extension_card, timeout=timeout)
        )

    def update_membership(self, domisili="Tetap", masa_aktif="4"):
        """Update member domicile and extension period."""
        self._select_domisili.select_option(str(domisili))
        self._select_masa_aktif.select_option(str(masa_aktif))
        self.click(self._btn_submit_update)
        self.page.wait_for_load_state("domcontentloaded")

    def click_cancel(self):
        """Click 'Batal' to return to member list."""
        self.click(self._btn_batal)
        self.page.wait_for_load_state("domcontentloaded")
