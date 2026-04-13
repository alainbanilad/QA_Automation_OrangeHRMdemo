from pages.saucedemo_login_page import SauceDemoLoginPage
from pages.saucedemo_inventory_page import SauceDemoInventoryPage

def test_add_item_to_cart_and_verify_count(driver):
    login_page = SauceDemoLoginPage(driver)
    inventory_page = SauceDemoInventoryPage(driver)

    login_page.open()
    login_page.login("standard_user", "secret_sauce")

    inventory_page.add_item_to_cart()

    assert inventory_page.get_cart_count() == "1"