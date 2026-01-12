from pages.base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self._username_field = page.locator("input[name='username']")
        self._password_field = page.locator("input[name='password']")
        self._login_button = page.locator("button[type='submit']")
        self._profile_icon = page.locator(".nav-link-user") 
        self._dropdown_title = page.locator(".dropdown-title")

    def get_welcome_text(self):
        self.click(self._profile_icon)
        self._dropdown_title.wait_for(state="visible")
        return self._dropdown_title.inner_text()

    def login_to_app(self, user, pwd):
        self.type_text(self._username_field, user)
        self.type_text(self._password_field, pwd)
        self.click(self._login_button)
      
