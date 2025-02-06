from selenium.webdriver.common.keys import Keys
from .locators import *
from .base_page import BasePage
from stringcase import spinalcase
from settings import CONFIG_DATA


class CartPage(BasePage):
    def __init__(self, driver):
        self.locator = CartLocators
        self.pg_url = f'{CONFIG_DATA["base_url"]}cart.html'
        super().__init__(driver)

    def get_items_in_cart(self, ):
        cart_elts = self.find_elements(*self.locator.items_in_cart)
        return [elt.text.strip() for elt in cart_elts]
