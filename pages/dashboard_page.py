from pages.base_page import BasePage

class DashboardPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        # Header & Navigation
        self._page_title = page.locator(".section-header h1, h1.section-title, .section-header")
        self._profile_icon = page.locator(".nav-link-user")
        self._dropdown_title = page.locator(".dropdown-title")
        self._logout_button = page.locator("a[href='/logout'], a:has-text('Logout')")
        self._sidebar_menu = page.locator(".sidebar-menu")

        # Admin Sidebar Navigation Locators
        self._menu_admin_dashboard = page.locator(".sidebar-menu a[href='/']")
        self._menu_admin_akun = page.locator(".sidebar-menu a[href='/AdminAkun']")
        self._menu_admin_dokter = page.locator(".sidebar-menu a[href='/adminDokter']")
        self._menu_admin_pendaftaran = page.locator(".sidebar-menu a[href='/adminPendaftaran']")
        self._menu_admin_keanggotaan = page.locator(".sidebar-menu a[href='/adminKeanggotaan']")
        self._menu_admin_laporan = page.locator(".sidebar-menu a[href='/adminLaporan']")

        # Doctor / Member Sidebar Navigation Locators
        self._menu_doctor_home = page.locator(".sidebar-menu a[href='/']")
        self._menu_doctor_registrasi = page.locator(".sidebar-menu a[href='/formRegistrasi']")
        self._menu_doctor_upload_berkas = page.locator(".sidebar-menu a[href='/uploadBerkas']")
        self._menu_doctor_syarat = page.locator(".sidebar-menu a[href='/syaratPendaftaran']")
        self._menu_doctor_ubah_password = page.locator(".sidebar-menu a[href='/ubahPassword']")

    def get_header_title(self, timeout=5000):
        """Get the main page header title (e.g., Dashboard, Administrasi Data Dokter)."""
        self._page_title.first.wait_for(state="visible", timeout=timeout)
        return self._page_title.first.inner_text().strip()

    def get_welcome_text(self, timeout=5000):
        """Click user profile dropdown and retrieve the welcome text."""
        self._profile_icon.wait_for(state="visible", timeout=timeout)
        self.click(self._profile_icon)
        self._dropdown_title.wait_for(state="visible", timeout=timeout)
        return self._dropdown_title.inner_text().strip()

    def logout(self):
        """Perform user logout."""
        self._profile_icon.wait_for(state="visible", timeout=10000)
        self.click(self._profile_icon)
        self._logout_button.first.wait_for(state="visible", timeout=5000)
        self.click(self._logout_button.first)

    # ------------------ Admin Navigation Methods ------------------
    def navigate_to_admin_dashboard(self):
        self.click(self._menu_admin_dashboard)

    def navigate_to_admin_akun(self):
        self.click(self._menu_admin_akun)

    def navigate_to_admin_dokter(self):
        self.click(self._menu_admin_dokter)

    def navigate_to_admin_pendaftaran(self):
        self.click(self._menu_admin_pendaftaran)

    def navigate_to_admin_keanggotaan(self):
        self.click(self._menu_admin_keanggotaan)

    def navigate_to_admin_laporan(self):
        self.click(self._menu_admin_laporan)

    # ------------------ Doctor / Member Navigation Methods ------------------
    def navigate_to_doctor_home(self):
        self.click(self._menu_doctor_home)

    def navigate_to_form_registrasi(self):
        self.click(self._menu_doctor_registrasi)

    def navigate_to_upload_berkas(self):
        self.click(self._menu_doctor_upload_berkas)

    def navigate_to_syarat_pendaftaran(self):
        self.click(self._menu_doctor_syarat)

    def navigate_to_ubah_password(self):
        self.click(self._menu_doctor_ubah_password)
