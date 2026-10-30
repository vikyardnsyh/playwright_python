import pytest
import allure

@allure.epic("PDHI Banten Portal")
@allure.feature("Admin - Administrasi Anggota")
class TestAdminAnggota:

    @pytest.mark.sanity
    @allure.story("Pencarian Anggota")
    @allure.title("Scenario: Search Member by Doctor Name")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_existing_member(self, admin_anggota_page, page):
        """Verify searching for an existing member doctor returns matched records."""
        keyword = "Ahmad"

        with allure.step(f"Search for member with keyword '{keyword}'"):
            admin_anggota_page.search_member(keyword)

        with allure.step("Verify matched member appears in the results table"):
            assert not admin_anggota_page.is_empty_state_displayed(), "Empty state should not be visible"
            assert admin_anggota_page.get_table_row_count() > 0, "At least one member should be found"
            assert admin_anggota_page.is_member_present(keyword), f"Member '{keyword}' must appear in table"

    @pytest.mark.regression
    @allure.story("Pencarian Anggota")
    @allure.title("Scenario: Search Member with Non-Existent Keyword (Not Found)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_member_not_found(self, admin_anggota_page, page):
        """Verify searching for a non-existent member displays the empty state."""
        non_existent_key = "NonExistentMember999"

        with allure.step(f"Search with non-existent keyword '{non_existent_key}'"):
            admin_anggota_page.search_member(non_existent_key)

        with allure.step("Verify empty state message is shown"):
            assert admin_anggota_page.is_empty_state_displayed(), "Empty state should be displayed"
            empty_msg = admin_anggota_page.get_empty_state_text()
            print(f"Empty state text: {empty_msg}")
            assert "tidak ada data" in empty_msg.lower() or "ditemukan" in empty_msg.lower()

    @pytest.mark.regression
    @allure.story("Pencarian Anggota")
    @allure.title("Scenario: Reset Search Restores Full Member List")
    @allure.severity(allure.severity_level.MINOR)
    def test_reset_search_restores_member_list(self, admin_anggota_page, page):
        """Verify clicking reset search restores the full list of members."""
        with allure.step("Perform empty search"):
            admin_anggota_page.search_member("NonExistentMember999")
            assert admin_anggota_page.is_empty_state_displayed()

        with allure.step("Click reset search button"):
            admin_anggota_page.reset_search()

        with allure.step("Verify member table records are restored"):
            assert not admin_anggota_page.is_empty_state_displayed(), "Members list should be restored"
            assert admin_anggota_page.get_table_row_count() > 0, "Row count should be greater than zero"

    @pytest.mark.regression
    @allure.story("Filter Anggota")
    @allure.title("Scenario: Filter Members by Active Status ('Aktif')")
    @allure.severity(allure.severity_level.NORMAL)
    def test_filter_members_aktif(self, admin_anggota_page, page):
        """Verify clicking 'Aktif' filter displays only members with active valid memberships."""
        with allure.step("Click 'Aktif' filter button"):
            admin_anggota_page.filter_by_aktif()

        with allure.step("Verify URL query parameter and status badges"):
            assert "aktif=aktif" in page.url or "aktif=" in page.url
            active_badges = page.locator("table tbody tr .badge:has-text('Aktif')")
            assert active_badges.count() > 0, "At least one 'Aktif' badge should be visible"

    @pytest.mark.regression
    @allure.story("Filter Anggota")
    @allure.title("Scenario: Filter Members by Inactive Status ('Non Aktif')")
    @allure.severity(allure.severity_level.NORMAL)
    def test_filter_members_nonaktif(self, admin_anggota_page, page):
        """Verify clicking 'Non Aktif' filter displays members with expired memberships."""
        with allure.step("Click 'Non Aktif' filter button"):
            admin_anggota_page.filter_by_nonaktif()

        with allure.step("Verify URL query parameter"):
            assert "nonaktif=nonaktif" in page.url or "nonaktif=" in page.url

    @pytest.mark.regression
    @allure.story("Filter Anggota")
    @allure.title("Scenario: Filter Members 'Semua' Restores Full List")
    @allure.severity(allure.severity_level.MINOR)
    def test_filter_members_semua(self, admin_anggota_page, page):
        """Verify clicking 'Semua' shows all members."""
        with allure.step("Click 'Semua' filter button"):
            admin_anggota_page.filter_by_semua()

        with allure.step("Verify members are displayed"):
            assert not admin_anggota_page.is_empty_state_displayed()
            assert admin_anggota_page.get_table_row_count() > 0

    @pytest.mark.sanity
    @allure.story("Kelola Keanggotaan")
    @allure.title("Scenario: View Manage Membership & Extension Form Page")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_view_manage_member_page(self, admin_anggota_page, page):
        """Verify clicking 'Kelola' opens the membership status and extension panel."""
        with allure.step("Click 'Kelola' button on the first member row"):
            admin_anggota_page.click_first_manage_member()

        with allure.step("Verify navigation to manage membership page"):
            page.wait_for_load_state("domcontentloaded")
            assert "/adminKeanggotaan/" in page.url and "/edit" in page.url

        with allure.step("Verify current status card and extension form are displayed"):
            assert admin_anggota_page.is_manage_page_loaded(), "Manage membership components must be rendered"

    @pytest.mark.regression
    @allure.story("Kelola Keanggotaan")
    @allure.title("Scenario: Cancel Extension and Return to Member List")
    @allure.severity(allure.severity_level.NORMAL)
    def test_cancel_manage_member_returns_to_list(self, admin_anggota_page, page):
        """Verify clicking 'Batal' on manage page returns to member list."""
        with allure.step("Navigate to manage membership page"):
            admin_anggota_page.click_first_manage_member()
            assert "/edit" in page.url

        with allure.step("Click 'Batal' button"):
            admin_anggota_page.click_cancel()

        with allure.step("Verify returned to member list page"):
            assert page.url.rstrip('/').endswith("/adminKeanggotaan")
            assert not admin_anggota_page.is_empty_state_displayed()
            assert admin_anggota_page.get_table_row_count() > 0
