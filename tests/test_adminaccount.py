import os
import pytest
from pages.admin_account_index_page import AdminAccount

DUMMY_ADMIN_DATA = {"nama": "Van Hallen", "user": "van_hallen", "pass":"rahasia", "role": "Admin"}
DUMMY_USER_DATA = {"nama": "Dr.Frankenstein", "user": "Gemini", "pass":"rahasia", "role": "User"}

@pytest.mark.regression
def test_add_new_admin(login_admin):
    #Fetch Login Session Using Admin Credentials
    page = login_admin
    #Transfer Session To AdminAccount class
    dashboard_admin = AdminAccount(page)
    dashboard_admin.go_to_admin_account_page()
    add_account_button = dashboard_admin.add_new()
    #Go To AdminAddAccount class
    add_account_button.add_new_account_admin("Gemini", "gemini_user", "rahasia", "Admin")

@pytest.mark.development
def test_delete_account_user(login_admin):
    #Fetch Login Session Using Admin Credentials
    page = login_admin  
    #Transfer Session To AdminAccount class
    dashboard_admin = AdminAccount(page)
    index_page = dashboard_admin.go_to_admin_account_page()
    target_user = DUMMY_USER_DATA["user"]
    index_page.delete_account(target_user)
    print(f"Success Delete Account: {target_user}")

    