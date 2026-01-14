import os
import pytest
import allure
from dotenv import load_dotenv
from pages.login_page import LoginPage

load_dotenv()

@pytest.fixture
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "ignore_https_errors": True,
        "extra_http_headers": {
            "ngrok-skip-browser-warning": "true"
        }
    }

@pytest.fixture
def login_page(page):
    url = os.getenv("BASE_URL").strip().rstrip('/')
    page.goto(f"{url}/login")  
    return LoginPage(page)

@pytest.fixture
def login_admin(page, login_page):
    user = os.getenv("ADMIN_USER")
    pwd = os.getenv("ADMIN_PASS")
    login_page.login_to_app(user, pwd)
    return page

@pytest.fixture
def login_users(page, login_page):
    user = os.getenv("REG_USER")
    pwd = os.getenv("REG_PASS")
    login_page.login_to_app(user, pwd)
    return page

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == 'call' and rep.failed:
        page = item.funcargs['page']
        allure.attach(page.screenshot(), name="screenshot_failure", attachment_type=allure.attachment_type.PNG)