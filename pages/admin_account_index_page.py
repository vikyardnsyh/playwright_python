from pages.base_page import BasePage

class AdminAccount(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self._admin_account_menu = page.locator("a[href='/AdminAkun']")
        self._add_account_btn = page.locator("a[href='/AdminAkun/create']")
        self._search = page.locator("input[type='search']")
        self._delete_btn = page.locator("button[data-original-title*='Hapus']")
        self._reset_password_btn = page.locator("button[title='Reset Password']")
        self._reset_edit_btn = page.locator("button[title='Edit Data Akun' i]")


    def go_to_admin_account_page(self):
        self.click(self._admin_account_menu)
        return self

    def add_new(self):
        self.click(self._add_account_btn)
        from pages.admin_account_add_page import AdminAddAccount
        return AdminAddAccount(self.page)
    
    def search_user(self, username):
        #Clear Search Field
        self._search.fill("")
        self.type_and_enter(self._search, username)
        return self
    
    def delete_account(self, username):
        self.search_user(username)
        target_row = self.page.locator("tr").filter(has_text=username).first
        target_row.wait_for(state="visible")
        self.click(target_row.locator(self._delete_btn))
        return self