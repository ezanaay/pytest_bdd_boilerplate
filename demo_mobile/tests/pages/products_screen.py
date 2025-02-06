import time

from appium.webdriver.common.appiumby import AppiumBy

import settings
from lib import log
logger = log.get_logger(__name__, settings.LOG_LEVEL, settings.CONSOLE_OUT)
from demo_mobile.tests.pages.base_screen import BaseScreen


class ProductsScreen(BaseScreen):

    def __init__(self, driver):
        super().__init__(driver)

    def add_product(self, product_name):
        time.sleep(1)
        self.click("add_to_cart_XPATH")

    def sort_by(self, criteria):
        self.click('toggle_products_view_XPATH')
        self.click('sort_icon_XPATH')
        self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, value=f'UiSelector().text("{criteria}")').click()


    def get_prices(self):
        prices = self.get_list_values('prices_XPATH')
        return [float(price[1:]) for price in prices]
