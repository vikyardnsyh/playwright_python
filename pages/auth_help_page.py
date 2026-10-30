import os
from pages.base_page import BasePage

class AuthHelpPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        # Pengajuan Akun Page Locators
        self._pengajuan_header = page.locator("h4:has-text('Pengajuan Akun Baru')")
        self._pengajuan_card = page.locator(".card.card-primary:has-text('Pengajuan Akun Baru')")
        self._pengajuan_wa_btn = page.locator("a[href*='wa.me']:has-text('Hubungi WhatsApp')")

        # Lupa Password Page Locators
        self._lupa_password_header = page.locator("h4:has-text('Bantuan Lupa Password')")
        self._lupa_password_card = page.locator(".card.card-warning:has-text('Bantuan Lupa Password')")
        self._lupa_password_wa_btn = page.locator("a[href*='wa.me']:has-text('Hubungi WhatsApp Sekretariat')")

        # Shared Elements
        self._pdhi_logo = page.locator("img[alt='Logo PDHI']")
        self._back_to_login_btn = page.locator("a:has-text('Kembali ke Halaman Login')")

    def navigate_to_pengajuan_akun(self):
        """Navigate directly to /pengajuanAkun."""
        base_url = (os.getenv("BASE_URL") or "http://127.0.0.1:8000").strip().rstrip('/')
        self.page.goto(f"{base_url}/pengajuanAkun")
        self.page.wait_for_load_state("domcontentloaded")

    def navigate_to_lupa_password(self):
        """Navigate directly to /lupaPassword."""
        base_url = (os.getenv("BASE_URL") or "http://127.0.0.1:8000").strip().rstrip('/')
        self.page.goto(f"{base_url}/lupaPassword")
        self.page.wait_for_load_state("domcontentloaded")

    def is_pengajuan_akun_loaded(self, timeout=5000):
        """Check if Pengajuan Akun page elements are rendered."""
        return (
            self.is_visible(self._pengajuan_header, timeout=timeout) and
            self.is_visible(self._pengajuan_wa_btn, timeout=timeout) and
            self.is_visible(self._back_to_login_btn, timeout=timeout)
        )

    def is_lupa_password_loaded(self, timeout=5000):
        """Check if Lupa Password page elements are rendered."""
        return (
            self.is_visible(self._lupa_password_header, timeout=timeout) and
            self.is_visible(self._lupa_password_wa_btn, timeout=timeout) and
            self.is_visible(self._back_to_login_btn, timeout=timeout)
        )

    def get_whatsapp_href(self, page_type="pengajuan"):
        """Retrieve href attribute of the WhatsApp contact link."""
        if page_type == "pengajuan":
            return self.get_attribute(self._pengajuan_wa_btn, "href")
        return self.get_attribute(self._lupa_password_wa_btn, "href")

    def click_back_to_login(self):
        """Click 'Kembali ke Halaman Login' button."""
        self.click(self._back_to_login_btn)
        self.page.wait_for_load_state("domcontentloaded")
