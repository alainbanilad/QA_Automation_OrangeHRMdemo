from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class SauceDemoInventoryPage(BasePage):

    ADD_TO_CART_BACKPACK = (By.ID, "add-to-cart-sauce-labs-backpack")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")

    def add_item_to_cart(self):
        self.click(self.ADD_TO_CART_BACKPACK)

    def get_cart_count(self):
        return self.find(self.CART_BADGE).text
