import os
from pages.base_page import BasePage

class AdminPendaftaranPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        # Search & Reset Locators
        self._search_input = page.locator("input[name='cariDokter']")
        self._search_submit_btn = page.locator("button[type='submit']:has(.fa-search)")
        self._reset_search_btn = page.locator("a[title='Reset Pencarian']")

        # Filter Buttons
        self._filter_semua_btn = page.locator("button[name='semua']")
        self._filter_terverifikasi_btn = page.locator("button[name='terverifikasi']")
        self._filter_tinjau_btn = page.locator("button[name='tinjau']")

        # Table & Rows
        self._table = page.locator("table.table")
        self._table_rows = page.locator("table tbody tr")
        self._empty_state = page.locator(".table-empty-state")
        self._total_count_badge = page.locator(".table-control-count .badge")

        # Verification Page Elements
        self._verifikasi_page_header = page.locator(".section-header h1:has-text('Verifikasi Pendaftaran')")
        self._biodata_card = page.locator(".card:has-text('Biodata Pendaftar')")
        self._dokumen_card = page.locator(".card:has-text('Dokumen Berkas Persyaratan')")
        self._document_items = page.locator(".card:has-text('Dokumen Berkas Persyaratan') .card")
        self._verification_form = page.locator("form[action*='/adminPendaftaran/']")
        self._input_tanggal_terdaftar = page.locator("input[name='tanggal_terdaftar']")
        self._select_masa_aktif = page.locator("select[name='masa_aktif']")
        self._select_domisili = page.locator("select[name='domisili_anggota']")
        self._btn_submit_verifikasi = page.locator("button[type='submit']:has-text('Verifikasi & Aktifkan Anggota')")
        self._already_verified_alert = page.locator(".alert-success:has-text('Dokter Ini Sudah Terverifikasi')")
        self._btn_batal_verifikasi = page.locator("a:has-text('Batal')")

    def navigate_to_page(self):
        """Navigate directly to the Administrasi Pendaftaran page."""
        base_url = (os.getenv("BASE_URL") or "http://127.0.0.1:8000").strip().rstrip('/')
        self.page.goto(f"{base_url}/adminPendaftaran")
        self.page.wait_for_load_state("domcontentloaded")

    def search_registration(self, keyword):
        """Type keyword and trigger registration search."""
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

    def filter_by_terverifikasi(self):
        """Click 'Terverifikasi' filter button."""
        self.click(self._filter_terverifikasi_btn)
        self.page.wait_for_load_state("domcontentloaded")

    def filter_by_perlu_ditinjau(self):
        """Click 'Perlu Ditinjau' filter button."""
        self.click(self._filter_tinjau_btn)
        self.page.wait_for_load_state("domcontentloaded")

    def click_first_verification(self):
        """Click 'Verifikasi' button on first registration row."""
        first_btn = self.page.locator("table tbody tr a:has-text('Verifikasi')").first
        first_btn.wait_for(state="visible", timeout=5000)
        self.click(first_btn)
        self.page.wait_for_load_state("domcontentloaded")

    def click_verification_by_doctor_name(self, doctor_name):
        """Click 'Verifikasi' button for specific doctor row."""
        row = self.page.locator(f"table tbody tr:has(td:has-text('{doctor_name}'))")
        btn = row.locator("a:has-text('Verifikasi')")
        self.click(btn)
        self.page.wait_for_load_state("domcontentloaded")

    def is_doctor_present(self, doctor_name, timeout=3000):
        """Check if doctor name exists in the table."""
        locator = self.page.locator(f"table tbody tr td:has-text('{doctor_name}')")
        return self.is_visible(locator, timeout=timeout)

    def is_empty_state_displayed(self, timeout=3000):
        """Check if table empty state is visible."""
        return self.is_visible(self._empty_state, timeout=timeout)

    def get_empty_state_text(self):
        """Retrieve empty state message."""
        return self.get_text(self._empty_state)

    def get_table_row_count(self):
        """Count rows in the table body (excluding empty state)."""
        if self.is_empty_state_displayed(timeout=1000):
            return 0
        return self._table_rows.count()

    # ------------------ Verification Page Helpers ------------------
    def is_verification_page_loaded(self, timeout=5000):
        """Check if verification page sections are loaded."""
        return (
            self.is_visible(self._verifikasi_page_header, timeout=timeout) and
            self.is_visible(self._biodata_card, timeout=timeout) and
            self.is_visible(self._dokumen_card, timeout=timeout)
        )

    def get_documents_count(self):
        """Return the number of document requirement cards displayed."""
        return self._document_items.count()

    def is_verification_form_displayed(self, timeout=3000):
        """Check if approval/activation form is displayed (for unverified doctor)."""
        return self.is_visible(self._btn_submit_verifikasi, timeout=timeout)

    def is_already_verified_banner_displayed(self, timeout=3000):
        """Check if 'Dokter Ini Sudah Terverifikasi' banner is visible."""
        return self.is_visible(self._already_verified_alert, timeout=timeout)

    def verify_and_activate_member(self, masa_aktif="4", domisili="Tetap"):
        """Submit the member verification and activation form."""
        if self.is_verification_form_displayed():
            self._select_masa_aktif.select_option(str(masa_aktif))
            self._select_domisili.select_option(str(domisili))
            self.click(self._btn_submit_verifikasi)
            self.page.wait_for_load_state("domcontentloaded")

    def click_cancel_verification(self):
        """Click 'Batal' to return to registration list."""
        self.click(self._btn_batal_verifikasi)
        self.page.wait_for_load_state("domcontentloaded")
