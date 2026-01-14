from pages.base_page import BasePage

class AdminAccount(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self._admin_account_menu = page.locator("a[href='/AdminAkun']")
        self._add_account = page.locator("a[href='/AdminAkun/create']")

    def go_to_admin_account_page(self):
        self.click(self._admin_account_menu)
        return self

    def add_new(self):
        self.click(self._add_account)
        from pages.admin_account_add_page import AdminAddAccount
        return AdminAddAccount(self.page)