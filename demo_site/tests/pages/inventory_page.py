from selenium.webdriver.common.keys import Keys
from .locators import *
from .base_page import BasePage
from stringcase import spinalcase
from settings import CONFIG_DATA


class InventoryPage(BasePage):
    def __init__(self, driver):
        self.locator = InventoryLocators
        self.pg_url = f'{CONFIG_DATA["base_url"]}inventory.html'
        super().__init__(driver)

    def add_product_to_cart(self, product_name):
        loc = list(self.locator.add_to_cart)
        loc[1] = f'add-to-cart-{spinalcase(product_name.lower())}'
        self.find_element(*loc).click()

    def get_list_of_products(self):
        product_elts = self.find_elements(*self.locator.list_of_products)
        return [elt.text.strip() for elt in product_elts]

    def navigate_to(self, pg):
        if pg == 'cart':
            self.find_element(*self.locator.shopping_cart).click()