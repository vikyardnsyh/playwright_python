from pages.base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self._username_field = page.locator("input[name='username']")
        self._password_field = page.locator("input[name='password']")
        self._login_button = page.locator("button[type='submit']")
        self._profile_icon = page.locator(".nav-link-user")
        self._dropdown_title = page.locator(".dropdown-title")
        self._error_alert = page.locator(".alert, .invalid-feedback, div[role='alert']")
        self._logout_button = page.locator("a:has-text('Logout'), a[href*='logout'], a.text-danger")
        self._remember_me_checkbox = page.locator("input[name='remember'], #remember-me, input[type='checkbox']")

        # Public Help Links
        self._link_lupa_password = page.locator("a[href*='lupaPassword'], a:has-text('Lupa Password')")
        self._link_ajukan_akun = page.locator("a[href*='pengajuanAkun'], a:has-text('Ajukan Akun Baru')")

    def handle_security_warning(self):
        """Handle browser mixed-content / insecure form warning if it appears."""
        try:
            send_anyway_btn = self.page.get_by_text("Send anyway")
            if send_anyway_btn.is_visible(timeout=3000):
                print("Debug: Peringatan keamanan muncul, mengeklik 'Send anyway'...")
                send_anyway_btn.click(force=True)
                send_anyway_btn.dispatch_event("click")
        except Exception:
            pass

    def login_to_app(self, user=None, pwd=None, submit=True):
        """Fill credentials and optionally submit form."""
        if user is not None:
            self.type_text(self._username_field, user)
        if pwd is not None:
            self.type_text(self._password_field, pwd)
        
        if submit:
            if pwd:
                self._password_field.press("Enter")
            else:
                self.click(self._login_button)
            self.handle_security_warning()

    def click_login(self):
        """Click the submit login button."""
        self.click(self._login_button)
        self.handle_security_warning()

    def click_lupa_password(self):
        """Click 'Lupa Password?' link on login form."""
        self.click(self._link_lupa_password)
        self.page.wait_for_load_state("domcontentloaded")

    def click_ajukan_akun_baru(self):
        """Click 'Ajukan Akun Baru' link on login footer."""
        self.click(self._link_ajukan_akun)
        self.page.wait_for_load_state("domcontentloaded")

    def get_welcome_text(self):
        """Retrieve welcome text from user profile dropdown."""
        self._profile_icon.wait_for(state="visible", timeout=10000)
        self.click(self._profile_icon)
        self._dropdown_title.wait_for(state="visible")
        return self._dropdown_title.inner_text().strip()

    def logout(self):
        """Log out the currently authenticated user."""
        self._profile_icon.wait_for(state="visible", timeout=10000)
        self.click(self._profile_icon)
        self._logout_button.first.wait_for(state="visible", timeout=5000)
        self.click(self._logout_button.first)
        self.handle_security_warning()

    def is_login_page_displayed(self, timeout=5000):
        """Check if login page elements are displayed."""
        return self.is_visible(self._login_button, timeout=timeout) or self.is_visible(self._username_field, timeout=timeout)

    def is_dashboard_displayed(self, timeout=10000):
        """Check if dashboard header profile icon is visible."""
        return self.is_visible(self._profile_icon, timeout=timeout)

    def get_error_message(self, timeout=3000):
        """Retrieve error alert or validation message if present."""
        try:
            self._error_alert.first.wait_for(state="visible", timeout=timeout)
            return self._error_alert.first.inner_text().strip()
        except Exception:
            return None

    def is_error_displayed(self, timeout=3000):
        """Check whether error alert is visible."""
        return self.get_error_message(timeout=timeout) is not None

    def get_password_field_type(self):
        """Return the HTML type attribute of password input."""
        return self.get_attribute(self._password_field, "type")

    def get_username_validation_message(self):
        """Return browser HTML5 validation message for username input."""
        return self._username_field.evaluate("el => el.validationMessage")

    def get_password_validation_message(self):
        """Return browser HTML5 validation message for password input."""
        return self._password_field.evaluate("el => el.validationMessage")
