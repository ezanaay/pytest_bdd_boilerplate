import time
import settings
from lib import log
logger = log.get_logger(__name__, settings.LOG_LEVEL, settings.CONSOLE_OUT)

from appium.webdriver.common.appiumby import AppiumBy

from demo_mobile.tests.pages.base_screen import BaseScreen


class CartScreen(BaseScreen):

    def __init__(self, driver):
        super().__init__(driver)

    def product_in_cart(self, product_name):
        time.sleep(1)
        return self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, value=f'UiSelector().text("{product_name}")').is_displayed()