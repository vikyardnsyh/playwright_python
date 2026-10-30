import time
import pytest
import allure
from data.users import MEMBER_USER

@allure.epic("PDHI Banten Portal")
@allure.feature("Admin - Manajemen Data Akun")
class TestAdminAkun:

    @pytest.mark.sanity
    @allure.story("Pencarian Akun")
    @allure.title("Scenario: Search Account with Existing Username")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_existing_account(self, admin_akun_page, page):
        """Verify searching for an existing username returns the matched record."""
        target_username = MEMBER_USER.username

        with allure.step(f"Search for username '{target_username}'"):
            admin_akun_page.search_account(target_username)

        with allure.step(f"Verify '{target_username}' is visible in the result table"):
            assert admin_akun_page.is_account_present(target_username), f"Account {target_username} should be in table"
            assert not admin_akun_page.is_empty_state_displayed(), "Empty state should not be visible"

    @pytest.mark.regression
    @allure.story("Pencarian Akun")
    @allure.title("Scenario: Search Account with Non-Existent Keyword (Not Found)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_not_found_account(self, admin_akun_page, page):
        """Verify searching for a non-existent account displays the empty state message."""
        non_existent_key = "non_existent_user_99999"

        with allure.step(f"Search for non-existent keyword '{non_existent_key}'"):
            admin_akun_page.search_account(non_existent_key)

        with allure.step("Verify empty state message is shown"):
            assert admin_akun_page.is_empty_state_displayed(), "Empty state should be visible"
            empty_msg = admin_akun_page.get_empty_state_text()
            print(f"Empty state message: {empty_msg}")
            assert "tidak ada data" in empty_msg.lower() or "ditemukan" in empty_msg.lower()

    @pytest.mark.regression
    @allure.story("Pencarian Akun")
    @allure.title("Scenario: Reset Search Restores Full Account List")
    @allure.severity(allure.severity_level.MINOR)
    def test_reset_search_restores_list(self, admin_akun_page, page):
        """Verify resetting search clears filters and restores the account list."""
        with allure.step("Perform a filter search"):
            admin_akun_page.search_account("non_existent_user_99999")
            assert admin_akun_page.is_empty_state_displayed()

        with allure.step("Click reset search button"):
            admin_akun_page.reset_search()

        with allure.step("Verify account rows are restored"):
            assert not admin_akun_page.is_empty_state_displayed(), "Table should have records after reset"
            assert admin_akun_page.get_table_row_count() > 0, "Row count should be greater than zero"

    @pytest.mark.regression
    @allure.story("Filter Akun")
    @allure.title("Scenario: Filter Accounts by Admin Role")
    @allure.severity(allure.severity_level.NORMAL)
    def test_filter_accounts_by_admin(self, admin_akun_page, page):
        """Verify clicking 'Admin' filter displays only administrator accounts."""
        with allure.step("Click 'Admin' filter button"):
            admin_akun_page.filter_by_admin()

        with allure.step("Verify URL query parameter and filtered results"):
            assert "admin=admin" in page.url or "admin=" in page.url
            admin_badges = page.locator("table tbody tr .badge:has-text('Admin')")
            assert admin_badges.count() > 0, "At least one Admin badge should be displayed"

    @pytest.mark.regression
    @allure.story("Filter Akun")
    @allure.title("Scenario: Filter Accounts by User / Doctor Role")
    @allure.severity(allure.severity_level.NORMAL)
    def test_filter_accounts_by_user(self, admin_akun_page, page):
        """Verify clicking 'User' filter displays only doctor/user accounts."""
        with allure.step("Click 'User' filter button"):
            admin_akun_page.filter_by_user()

        with allure.step("Verify URL query parameter and filtered results"):
            assert "user=user" in page.url or "user=" in page.url
            user_badges = page.locator("table tbody tr .badge:has-text('User')")
            assert user_badges.count() > 0, "At least one User badge should be displayed"

    @pytest.mark.regression
    @allure.story("Manajemen Akun")
    @allure.title("Scenario: Add New Doctor Account")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_new_account(self, admin_akun_page, page):
        """Verify Administrator can create a new account successfully."""
        ts = int(time.time())
        new_username = f"auto_{ts}"
        new_fullname = f"Drh. Auto Test {ts}"
        password = "PdhiBanten2!"

        with allure.step(f"Create account for '{new_username}'"):
            admin_akun_page.create_account(
                nama_lengkap=new_fullname,
                username=new_username,
                password=password,
                role_id="1"
            )

        with allure.step("Search and verify newly created account"):
            admin_akun_page.search_account(new_username)
            assert admin_akun_page.is_account_present(new_username), f"Created user {new_username} must be in table"

    @pytest.mark.regression
    @allure.story("Manajemen Akun")
    @allure.title("Scenario: Update Existing Account Details")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_account(self, admin_akun_page, page):
        """Verify Administrator can edit and update an existing account."""
        ts = int(time.time())
        target_username = f"upd_{ts}"
        initial_name = f"Drh. Pre Edit {ts}"
        updated_name = f"Drh. Post Edit {ts}"

        with allure.step(f"Pre-setup: Create account '{target_username}' to update"):
            admin_akun_page.create_account(
                nama_lengkap=initial_name,
                username=target_username,
                password="PdhiBanten2!",
                role_id="1"
            )

        with allure.step("Edit account with new full name"):
            admin_akun_page.edit_account(
                username=target_username,
                new_nama_lengkap=updated_name
            )

        with allure.step("Verify updated full name appears in table"):
            admin_akun_page.search_account(target_username)
            row = page.locator(f"table tbody tr:has(code:text-is('{target_username}'))")
            assert updated_name in row.inner_text(), "Row should display the updated doctor name"

    @pytest.mark.regression
    @allure.story("Manajemen Akun")
    @allure.title("Scenario: Delete Account with Pre-setup Lifecycle")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_account_lifecycle(self, admin_akun_page, page):
        """Verify Administrator can delete an account with pre-setup creation."""
        ts = int(time.time())
        target_username = f"del_{ts}"
        fullname = f"Drh. For Deletion {ts}"

        with allure.step(f"Pre-setup: Create dedicated account '{target_username}'"):
            admin_akun_page.create_account(
                nama_lengkap=fullname,
                username=target_username,
                password="PdhiBanten2!",
                role_id="1"
            )
            admin_akun_page.search_account(target_username)
            assert admin_akun_page.is_account_present(target_username), "Account must exist before deletion"

        with allure.step(f"Delete account '{target_username}' and confirm dialog"):
            admin_akun_page.delete_account(target_username)

        with allure.step(f"Verify account '{target_username}' is permanently removed"):
            admin_akun_page.search_account(target_username)
            assert not admin_akun_page.is_account_present(target_username), "Deleted account should not exist"
            assert admin_akun_page.is_empty_state_displayed(), "Empty state should show after deleting searched item"
