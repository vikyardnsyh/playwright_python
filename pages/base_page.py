class BasePage:
    def __init__(self, page):
        self.page = page

    def navigate(self, url):
        self.page.goto(url)

    def click(self, locator):
        locator.wait_for(state="visible")
        locator.click()

    def type_text(self, locator, text):
        locator.wait_for(state="visible")
        locator.fill(text)

    def select_option(self, locator, text):
        locator.wait_for(state="visible")
        locator.select_option(label=text)