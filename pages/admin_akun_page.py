import os
from pages.base_page import BasePage

class AdminAkunPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        # Main Controls
        self._search_input = page.locator("input[name='cariAkun']")
        self._search_submit_btn = page.locator("button[type='submit']:has(.fa-search)")
        self._reset_search_btn = page.locator("a[title='Reset Pencarian']")

        # Filter Buttons
        self._filter_semua_btn = page.locator("button[name='semua']")
        self._filter_admin_btn = page.locator("button[name='admin']")
        self._filter_user_btn = page.locator("button[name='user']")

        # Action Buttons
        self._tambah_akun_btn = page.locator("a[href*='/AdminAkun/create'], a:has-text('Tambah Akun')")

        # Table & Empty State
        self._table = page.locator("table.table")
        self._table_rows = page.locator("table tbody tr")
        self._empty_state = page.locator(".table-empty-state")
        self._total_count_badge = page.locator(".table-control-count .badge")

        # Tambah Akun Form Elements
        self._input_nama_lengkap = page.locator("input[name='nama_lengkap']")
        self._input_username = page.locator("input[name='username']")
        self._input_password = page.locator("input[name='password']")
        self._select_kelas_pengguna = page.locator("select[name='id_kelas_pengguna']")
        self._btn_submit_tambah = page.locator("button[type='submit']:has-text('Tambahkan Akun')")

        # Edit Akun Form Elements
        self._select_status_pengguna = page.locator("select[name='status_pengguna']")
        self._btn_submit_edit = page.locator("button[type='submit']:has-text('Simpan Perubahan')")

        # SweetAlert Modals
        self._swal_modal = page.locator(".swal-modal")
        self._swal_confirm_delete_btn = page.locator(".swal-button--confirm, button.swal-button:has-text('Hapus')")
        self._swal_cancel_btn = page.locator(".swal-button--cancel, button.swal-button:has-text('Batal')")

    def navigate_to_page(self):
        """Navigate directly to the Admin Akun list page."""
        base_url = (os.getenv("BASE_URL") or "http://127.0.0.1:8000").strip().rstrip('/')
        self.page.goto(f"{base_url}/AdminAkun")
        self.page.wait_for_load_state("domcontentloaded")

    def search_account(self, keyword):
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

    def filter_by_admin(self):
        """Click 'Admin' filter button."""
        self.click(self._filter_admin_btn)
        self.page.wait_for_load_state("domcontentloaded")

    def filter_by_user(self):
        """Click 'User' filter button."""
        self.click(self._filter_user_btn)
        self.page.wait_for_load_state("domcontentloaded")

    def click_add_account(self):
        """Click 'Tambah Akun' button."""
        self.click(self._tambah_akun_btn)
        self.page.wait_for_load_state("domcontentloaded")

    def create_account(self, nama_lengkap, username, password, role_id="1"):
        """Fill and submit new account creation form."""
        self.click_add_account()
        self.type_text(self._input_nama_lengkap, nama_lengkap)
        self.type_text(self._input_username, username)
        self.type_text(self._input_password, password)
        self._select_kelas_pengguna.select_option(str(role_id))
        self.click(self._btn_submit_tambah)
        self.page.wait_for_load_state("domcontentloaded")

    def click_edit_account(self, username):
        """Find row for specified username and click Edit button."""
        row = self.page.locator(f"table tbody tr:has(code:text-is('{username}'))")
        edit_btn = row.locator("a.btn-action-edit, a[href*='/edit']")
        self.click(edit_btn)
        self.page.wait_for_load_state("domcontentloaded")

    def edit_account(self, username, new_nama_lengkap=None, new_status=None, new_role=None):
        """Navigate to edit form, change values, and submit."""
        self.click_edit_account(username)
        if new_nama_lengkap:
            self.type_text(self._input_nama_lengkap, new_nama_lengkap)
        if new_status:
            self._select_status_guna = self.page.locator("select[name='status_pengguna']")
            self._select_status_guna.select_option(str(new_status))
        if new_role:
            self._select_kelas_pengguna.select_option(str(new_role))
        self.click(self._btn_submit_edit)
        self.page.wait_for_load_state("domcontentloaded")

    def delete_account(self, username):
        """Find row for specified username, click Delete, and confirm SweetAlert."""
        row = self.page.locator(f"table tbody tr:has(code:text-is('{username}'))")
        delete_btn = row.locator("button.btn-action-delete, button.show-alert-delete-confirm")
        self.click(delete_btn)
        # Wait for SweetAlert dialog and confirm
        self._swal_confirm_delete_btn.wait_for(state="visible", timeout=5000)
        self.click(self._swal_confirm_delete_btn)
        self.page.wait_for_load_state("domcontentloaded")

    def is_account_present(self, username, timeout=3000):
        """Check if username code tag exists in the table."""
        locator = self.page.locator(f"table tbody tr td code:text-is('{username}')")
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
