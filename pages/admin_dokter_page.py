import os
from pages.base_page import BasePage

class AdminDokterPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        # Search & Reset Locators
        self._search_input = page.locator("input[name='cariDokter']")
        self._search_submit_btn = page.locator("button[type='submit']:has(.fa-search)")
        self._reset_search_btn = page.locator("a[title='Reset Pencarian']")

        # Filter Buttons
        self._filter_semua_btn = page.locator("button[name='semua']")
        self._filter_terdaftar_btn = page.locator("button[name='terdaftar']")
        self._filter_belum_terdaftar_btn = page.locator("button[name='belumterdaftar']")

        # Table & Rows
        self._table = page.locator("table.table-freeze-dokter")
        self._table_rows = page.locator("table.table-freeze-dokter tbody tr")
        self._empty_state = page.locator(".table-empty-state")
        self._total_count_badge = page.locator(".table-control-count .badge")

        # Detail Page Elements
        self._detail_page_header = page.locator(".section-header h1:has-text('Detail Profil Dokter')")
        self._detail_doctor_name = page.locator(".profile-widget-name h5.text-primary")
        self._detail_username = page.locator(".profile-widget-name strong")
        self._detail_biodata_card = page.locator(".profile-widget")
        self._detail_contact_card = page.locator(".card:has-text('Kontak Dokter')")
        self._detail_clinic_card = page.locator(".card:has-text('Info Tempat Kerja')")
        self._detail_back_btn = page.locator("a:has-text('Kembali ke Daftar Dokter')")

    def navigate_to_page(self):
        """Navigate directly to the Admin Dokter list page."""
        base_url = (os.getenv("BASE_URL") or "http://127.0.0.1:8000").strip().rstrip('/')
        self.page.goto(f"{base_url}/adminDokter")
        self.page.wait_for_load_state("domcontentloaded")

    def search_doctor(self, keyword):
        """Type keyword and trigger doctor search."""
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

    def filter_by_terdaftar(self):
        """Click 'Terdaftar' filter button."""
        self.click(self._filter_terdaftar_btn)
        self.page.wait_for_load_state("domcontentloaded")

    def filter_by_belum_terdaftar(self):
        """Click 'Belum Terdaftar' filter button."""
        self.click(self._filter_belum_terdaftar_btn)
        self.page.wait_for_load_state("domcontentloaded")

    def click_first_doctor_detail(self):
        """Click Detail button on the first doctor row."""
        first_detail_btn = self.page.locator("table tbody tr .col-doctor-action a.btn-info").first
        first_detail_btn.wait_for(state="visible", timeout=5000)
        self.click(first_detail_btn)
        self.page.wait_for_load_state("domcontentloaded")

    def click_doctor_detail_by_name(self, doctor_name):
        """Click Detail button for a specific doctor row matching doctor_name."""
        row = self.page.locator(f"table tbody tr:has(.col-doctor-name:has-text('{doctor_name}'))")
        detail_btn = row.locator("a.btn-info")
        self.click(detail_btn)
        self.page.wait_for_load_state("domcontentloaded")

    def is_doctor_present(self, doctor_name, timeout=3000):
        """Check if doctor name appears in the table."""
        locator = self.page.locator(f"table tbody tr .col-doctor-name:has-text('{doctor_name}')")
        return self.is_visible(locator, timeout=timeout)

    def is_empty_state_displayed(self, timeout=3000):
        """Check if table empty state is visible."""
        return self.is_visible(self._empty_state, timeout=timeout)

    def get_empty_state_text(self):
        """Retrieve empty state message."""
        return self.get_text(self._empty_state)

    def get_table_row_count(self):
        """Count rows in the doctor table (excluding empty state)."""
        if self.is_empty_state_displayed(timeout=1000):
            return 0
        return self._table_rows.count()

    # ------------------ Detail Page Helpers ------------------
    def get_detail_doctor_name(self, timeout=5000):
        """Get doctor name on detail page."""
        self._detail_doctor_name.wait_for(state="visible", timeout=timeout)
        return self._detail_doctor_name.inner_text().strip()

    def get_detail_username(self, timeout=5000):
        """Get doctor username on detail page."""
        self._detail_username.wait_for(state="visible", timeout=timeout)
        return self._detail_username.inner_text().strip()

    def is_detail_page_loaded(self, timeout=5000):
        """Check if all key detail components are rendered."""
        return (
            self.is_visible(self._detail_page_header, timeout=timeout) and
            self.is_visible(self._detail_biodata_card, timeout=timeout) and
            self.is_visible(self._detail_contact_card, timeout=timeout)
        )

    def click_back_to_list(self):
        """Click 'Kembali ke Daftar Dokter' button on detail page."""
        self.click(self._detail_back_btn)
        self.page.wait_for_load_state("domcontentloaded")
