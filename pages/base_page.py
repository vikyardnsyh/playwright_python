class BasePage:
    def __init__(self, page):
        self.page = page

    def navigate(self, url):
        self.page.goto(url)

    def click(self, locator):
        locator.wait_for(state="visible", timeout=5000)
        locator.click()

    def type_text(self, locator, text):
        locator.wait_for(state="visible", timeout=5000)
        locator.click()
        locator.clear()
        if text:
            locator.fill(text)

    def type_and_enter(self, locator, text):
        locator.wait_for(state="visible", timeout=5000)
        locator.fill(text)
        locator.press("Enter")

    def select_option(self, locator, text):
        locator.wait_for(state="visible", timeout=5000)
        locator.select_option(label=text)

    def is_visible(self, locator, timeout=5000):
        try:
            locator.wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            return False

    def get_text(self, locator, timeout=5000):
        locator.wait_for(state="visible", timeout=timeout)
        return locator.inner_text().strip()

    def get_attribute(self, locator, attribute_name, timeout=5000):
        locator.wait_for(state="attached", timeout=timeout)
        return locator.get_attribute(attribute_name)
