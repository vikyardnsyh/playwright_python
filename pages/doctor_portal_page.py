import os
from pages.base_page import BasePage

class DoctorPortalPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        # Doctor Home Dashboard Locators
        self._home_header = page.locator(".section-header h1:has-text('Beranda Dokter')")
        self._profile_widget = page.locator(".profile-widget")
        self._profile_name = page.locator(".profile-widget-name h5")
        self._contact_card = page.locator(".card:has-text('Kontak Dokter')")
        self._clinic_card = page.locator(".card:has-text('Info Tempat Kerja')")
        self._checklist_card = page.locator(".card:has-text('Checklist Kelengkapan Berkas')")
        self._btn_perbarui_biodata = page.locator("a:has-text('Perbarui Biodata')")
        self._btn_kelola_berkas = page.locator("a:has-text('Kelola Berkas')")

        # Form Registrasi Locators
        self._form_registrasi_header = page.locator(".section-header h1:has-text('Form Registrasi')")
        self._form_biodata = page.locator(".card:has-text('Formulir Biodata Anggota')")
        self._input_nama_lengkap = page.locator("input[name='nama_lengkap']")
        self._input_nama_panggilan = page.locator("input[name='nama_panggilan']")
        self._input_tempat_lahir = page.locator("input[name='tempat_lahir']")
        self._select_bidang_kerja = page.locator("select[name='bidang_kerja']")
        self._btn_submit_registrasi = page.locator("button[type='submit']:has-text('Data')")

        # Upload Berkas Locators
        self._upload_berkas_header = page.locator(".section-header h1:has-text('Upload Berkas')")
        self._document_upload_cards = page.locator(".card.border:has(.card-header)")

        # Syarat Pendaftaran Locators
        self._syarat_header = page.locator(".section-header h1:has-text('Syarat Pendaftaran')")
        self._letterhead_card = page.locator(".card:has-text('PERHIMPUNAN DOKTER HEWAN INDONESIA')")

        # Ubah Password Locators
        self._ubah_password_header = page.locator(".section-header h1:has-text('Ubah Password')")
        self._input_current_password = page.locator("input[name='password_saat_ini']")
        self._input_new_password = page.locator("input[name='password_baru']")
        self._btn_submit_password = page.locator("button[type='submit']:has-text('Simpan Kata Sandi Baru')")
        self._btn_toggle_password = page.locator("button[title='Lihat / Sembunyikan Password']").first

    def navigate_to_home(self):
        """Navigate to Doctor Home."""
        base_url = (os.getenv("BASE_URL") or "http://127.0.0.1:8000").strip().rstrip('/')
        self.page.goto(f"{base_url}/")
        self.page.wait_for_load_state("domcontentloaded")

    def is_home_dashboard_loaded(self, timeout=5000):
        """Verify doctor home elements are rendered."""
        return (
            self.is_visible(self._home_header, timeout=timeout) and
            self.is_visible(self._profile_widget, timeout=timeout) and
            self.is_visible(self._contact_card, timeout=timeout) and
            self.is_visible(self._checklist_card, timeout=timeout)
        )

    def get_doctor_profile_name(self):
        """Get doctor name displayed on home profile widget."""
        return self.get_text(self._profile_name)

    # ------------------ Form Registrasi Helpers ------------------
    def navigate_to_form_registrasi(self):
        base_url = (os.getenv("BASE_URL") or "http://127.0.0.1:8000").strip().rstrip('/')
        self.page.goto(f"{base_url}/formRegistrasi")
        self.page.wait_for_load_state("domcontentloaded")

    def is_form_registrasi_loaded(self, timeout=5000):
        return (
            self.is_visible(self._form_registrasi_header, timeout=timeout) and
            self.is_visible(self._input_nama_lengkap, timeout=timeout)
        )

    def get_nama_lengkap_value(self):
        return self._input_nama_lengkap.input_value()

    # ------------------ Upload Berkas Helpers ------------------
    def navigate_to_upload_berkas(self):
        base_url = (os.getenv("BASE_URL") or "http://127.0.0.1:8000").strip().rstrip('/')
        self.page.goto(f"{base_url}/uploadBerkas")
        self.page.wait_for_load_state("domcontentloaded")

    def is_upload_berkas_loaded(self, timeout=5000):
        return self.is_visible(self._upload_berkas_header, timeout=timeout)

    def get_document_cards_count(self):
        return self._document_upload_cards.count()

    # ------------------ Syarat Pendaftaran Helpers ------------------
    def navigate_to_syarat_pendaftaran(self):
        base_url = (os.getenv("BASE_URL") or "http://127.0.0.1:8000").strip().rstrip('/')
        self.page.goto(f"{base_url}/syaratPendaftaran")
        self.page.wait_for_load_state("domcontentloaded")

    def is_syarat_pendaftaran_loaded(self, timeout=5000):
        return (
            self.is_visible(self._syarat_header, timeout=timeout) and
            self.is_visible(self._letterhead_card, timeout=timeout)
        )

    # ------------------ Ubah Password Helpers ------------------
    def navigate_to_ubah_password(self):
        base_url = (os.getenv("BASE_URL") or "http://127.0.0.1:8000").strip().rstrip('/')
        self.page.goto(f"{base_url}/ubahPassword")
        self.page.wait_for_load_state("domcontentloaded")

    def is_ubah_password_loaded(self, timeout=5000):
        return (
            self.is_visible(self._ubah_password_header, timeout=timeout) and
            self.is_visible(self._input_current_password, timeout=timeout) and
            self.is_visible(self._input_new_password, timeout=timeout)
        )

    def toggle_password_masking(self):
        """Click the visibility toggle eye button."""
        self.click(self._btn_toggle_password)
