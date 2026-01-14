from pages.base_page import BasePage

class AdminAddAccount(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self._fullname_field = page.locator("input[name='nama_lengkap']")
        self._username_field = page.locator("input[name='username']")
        self._password_field = page.locator("input[name='password']")
        self._class_field = page.locator("select[name='id_kelas_pengguna']")
        self._save_button = page.locator("button[type='submit']")
        self._back_button = page.locator("a[href='/AdminAkun']")

    def add_new_account_admin(self,name,usr,pwd,acclass):
        self.type_text(self._fullname_field, name)
        self.type_text(self._username_field, usr)
        self.type_text(self._password_field, pwd)
        self.select_option(self._class_field, acclass)
        self.click(self._save_button)
