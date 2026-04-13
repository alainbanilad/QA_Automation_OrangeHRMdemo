from pages.orangehrm_login_page import OrangeHRMLoginPage

def test_orangehrm_login_success(driver):
    login_page = OrangeHRMLoginPage(driver)
    login_page.open()

    login_page.login("Admin", "admin123")

    assert login_page.is_logged_in()