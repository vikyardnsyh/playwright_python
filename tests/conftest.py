import os
import pytest
import allure
from dotenv import load_dotenv
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.admin_akun_page import AdminAkunPage
from pages.admin_dokter_page import AdminDokterPage
from pages.admin_pendaftaran_page import AdminPendaftaranPage
from pages.admin_anggota_page import AdminAnggotaPage
from pages.admin_laporan_page import AdminLaporanPage
from pages.doctor_portal_page import DoctorPortalPage
from pages.auth_help_page import AuthHelpPage
from data.users import ADMIN_USER, MEMBER_USER

load_dotenv()

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        "args": [
            "--disable-features=InsecureFormWarnings",
            "--ignore-certificate-errors"
        ],
    }

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
    url = (os.getenv("BASE_URL") or "http://127.0.0.1:8000").strip().rstrip('/')
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

@pytest.fixture
def cleanup_admin_account(login_admin):
    page = login_admin

    yield
    # Code After Yield = 'AFTER TEST'
    print("\n[Cleanup] Removing Test Data...")
    from pages.admin_account_index_page import AdminAccount
    index_page = AdminAccount(page)
    index_page.go_to_admin_account_page()

    # Panggil fungsi hapus yang kamu buat (contoh: berdasarkan username)
    index_page.delete_account_by_username("gemini_user")

@pytest.fixture
def admin_dashboard(login_page, page):
    """Fixture that logs in as Admin and yields the DashboardPage instance."""
    login_page.login_to_app(ADMIN_USER.username, ADMIN_USER.password)
    dashboard = DashboardPage(page)
    dashboard._profile_icon.wait_for(state="visible", timeout=10000)
    return dashboard

@pytest.fixture
def doctor_dashboard(login_page, page):
    """Fixture that logs in as Doctor/Member and yields the DashboardPage instance."""
    login_page.login_to_app(MEMBER_USER.username, MEMBER_USER.password)
    dashboard = DashboardPage(page)
    dashboard._profile_icon.wait_for(state="visible", timeout=10000)
    return dashboard

@pytest.fixture
def admin_akun_page(admin_dashboard, page):
    """Fixture that logs in as Admin and navigates directly to Admin Akun."""
    admin_dashboard.navigate_to_admin_akun()
    return AdminAkunPage(page)

@pytest.fixture
def admin_dokter_page(admin_dashboard, page):
    """Fixture that logs in as Admin and navigates directly to Admin Dokter."""
    admin_dashboard.navigate_to_admin_dokter()
    return AdminDokterPage(page)

@pytest.fixture
def admin_pendaftaran_page(admin_dashboard, page):
    """Fixture that logs in as Admin and navigates directly to Admin Pendaftaran."""
    admin_dashboard.navigate_to_admin_pendaftaran()
    return AdminPendaftaranPage(page)

@pytest.fixture
def admin_anggota_page(admin_dashboard, page):
    """Fixture that logs in as Admin and navigates directly to Admin Anggota."""
    admin_dashboard.navigate_to_admin_keanggotaan()
    return AdminAnggotaPage(page)

@pytest.fixture
def admin_laporan_page(admin_dashboard, page):
    """Fixture that logs in as Admin and navigates directly to Download Laporan."""
    admin_dashboard.navigate_to_admin_laporan()
    return AdminLaporanPage(page)

@pytest.fixture
def doctor_portal_page(doctor_dashboard, page):
    """Fixture that logs in as Doctor/Member and provides DoctorPortalPage."""
    return DoctorPortalPage(page)

@pytest.fixture
def auth_help_page(page):
    """Fixture that provides AuthHelpPage for public help pages."""
    return AuthHelpPage(page)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == 'call' and rep.failed:
        page = item.funcargs.get('page')
        if page:
            try:
                allure.attach(
                    page.screenshot(full_page=True),
                    name="screenshot_error",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception:
                pass
