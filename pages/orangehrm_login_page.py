from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class OrangeHRMLoginPage(BasePage):
    URL = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"

    USERNAME = (By.NAME, "username")
    PASSWORD = (By.NAME, "password")
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")
    DASHBOARD_HEADER = (By.XPATH, "//h6[text()='Dashboard']")

    def open(self):
        self.driver.get(self.URL)

    def login(self, username, password):
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN_BUTTON)

    def is_logged_in(self):
        return self.find(self.DASHBOARD_HEADER).is_displayed()
