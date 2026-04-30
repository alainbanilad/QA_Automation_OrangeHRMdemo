from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage


class OrangeHRMLoginPage(BasePage):
    """Page object for OrangeHRM auth flows used by critical smoke tests.

    Keep test methods scenario-focused by using this class for all selector and
    wait logic. Add new auth interactions here rather than in test files.
    """
    USERNAME = (By.NAME, "username")
    PASSWORD = (By.NAME, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    DASHBOARD_HEADER = (By.XPATH, "//h6[normalize-space()='Dashboard']")
    LOGIN_ERROR = (By.CSS_SELECTOR, "p.oxd-alert-content-text")
    REQUIRED_ERRORS = (By.XPATH, "//span[normalize-space()='Required']")
    USER_DROPDOWN = (By.CSS_SELECTOR, "span.oxd-userdropdown-tab")
    LOGOUT_LINK = (By.XPATH, "//a[normalize-space()='Logout']")

    def open(self, base_url):
        self.driver.get(f"{base_url}/web/index.php/auth/login")

    def login(self, username, password):
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN_BUTTON)

    def submit_blank_login(self):
        self.click(self.LOGIN_BUTTON)

    def is_logged_in(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.DASHBOARD_HEADER))
            return True
        except TimeoutException:
            return False

    def is_login_error_visible(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.LOGIN_ERROR))
            return True
        except TimeoutException:
            return False

    def get_login_error_text(self):
        return self.find(self.LOGIN_ERROR).text.strip()

    def are_required_field_errors_visible(self):
        try:
            errors = self.wait.until(EC.presence_of_all_elements_located(self.REQUIRED_ERRORS))
            return len(errors) >= 1
        except TimeoutException:
            return False

    def logout(self):
        self.click(self.USER_DROPDOWN)
        self.wait.until(EC.element_to_be_clickable(self.LOGOUT_LINK)).click()

    def is_login_page_displayed(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.USERNAME))
            return "/auth/login" in self.driver.current_url
        except TimeoutException:
            return False

    def open_protected_dashboard(self, base_url):
        self.driver.get(f"{base_url}/web/index.php/dashboard/index")
