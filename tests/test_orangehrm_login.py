from pages.orangehrm_login_page import OrangeHRMLoginPage
import pytest


@pytest.mark.smoke
@pytest.mark.orangehrm
def test_login_success_with_valid_credentials(driver, orangehrm_base_url, orangehrm_valid_credentials):
    login_page = OrangeHRMLoginPage(driver)
    username, password = orangehrm_valid_credentials

    login_page.open(orangehrm_base_url)
    login_page.login(username, password)

    assert login_page.is_logged_in()


@pytest.mark.smoke
@pytest.mark.orangehrm
def test_login_fails_with_invalid_credentials(driver, orangehrm_base_url, orangehrm_invalid_credentials):
    login_page = OrangeHRMLoginPage(driver)
    username, invalid_password = orangehrm_invalid_credentials

    login_page.open(orangehrm_base_url)
    login_page.login(username, invalid_password)

    assert login_page.is_login_error_visible()
    assert "invalid credentials" in login_page.get_login_error_text().lower()


@pytest.mark.orangehrm
def test_login_shows_required_error_when_credentials_are_blank(driver, orangehrm_base_url):
    login_page = OrangeHRMLoginPage(driver)

    login_page.open(orangehrm_base_url)
    login_page.submit_blank_login()

    assert login_page.are_required_field_errors_visible()


@pytest.mark.smoke
@pytest.mark.orangehrm
def test_logout_ends_session_and_returns_to_login(driver, orangehrm_base_url, orangehrm_valid_credentials):
    login_page = OrangeHRMLoginPage(driver)
    username, password = orangehrm_valid_credentials

    login_page.open(orangehrm_base_url)
    login_page.login(username, password)
    assert login_page.is_logged_in()

    login_page.logout()

    assert login_page.is_login_page_displayed()


@pytest.mark.orangehrm
def test_protected_route_redirects_to_login_after_logout(driver, orangehrm_base_url, orangehrm_valid_credentials):
    login_page = OrangeHRMLoginPage(driver)
    username, password = orangehrm_valid_credentials

    login_page.open(orangehrm_base_url)
    login_page.login(username, password)
    assert login_page.is_logged_in()

    login_page.logout()
    assert login_page.is_login_page_displayed()

    login_page.open_protected_dashboard(orangehrm_base_url)

    assert login_page.is_login_page_displayed()