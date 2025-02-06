import time

import settings
from lib import log

logger = log.get_logger(__name__, settings.LOG_LEVEL, settings.CONSOLE_OUT)

from appium.webdriver.common.appiumby import AppiumBy

from demo_mobile.tests.pages.locators import read_locator


class BaseScreen:
    def __init__(self, driver):
        self.driver = driver

    def click(self, locator):
        if str(locator).endswith("_XPATH"):
            logger.debug(f"Clicked on {locator} based on xpath locator", extra={'locator': locator})
            self.driver.find_element(by=AppiumBy.XPATH, value=read_locator(locator)).click()
        elif str(locator).endswith("_ACCESSIBILITYID"):
            self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value=read_locator(locator)).click()
            logger.debug(f"Clicked on {locator} based on ACCESSIBILITY_ID locator", extra={'locator': locator})
        elif str(locator).endswith("_ID"):
            self.driver.find_element(by=AppiumBy.ID, value=read_locator(locator)).click()
            logger.debug(f"Clicked on {locator} based on ID locator", extra={'locator': locator})
        elif str(locator).endswith("_TEXT"):
            self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value=read_locator(locator)).click()
            logger.debug(f"Clicked on {locator} based on ANDROID_UIAUTOMATOR locator", extra={'locator': locator})

    def send_keys(self, locator, content):
        if str(locator).endswith("_XPATH"):
            self.driver.find_element(by=AppiumBy.XPATH, value=read_locator(locator)) \
                .send_keys(content)
            self.driver.hide_keyboard()
        if str(locator).endswith("_TEXT"):
            self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value=read_locator(locator)) \
                .send_keys(content)
            self.driver.hide_keyboard()
        if str(locator).endswith("_ACCESSIBILITYID"):
            self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value=read_locator(locator)) \
                .send_keys(content)
            self.driver.hide_keyboard()

    def screen_displayed(self, expected_screen):
        screen = expected_screen.lower()
        time.sleep(3)
        if screen == 'products':
            return self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                                            value='UiSelector().text("PRODUCTS")').is_displayed()

    def navigate_to(self, screen_name):
        screen = screen_name.lower()
        time.sleep(1)
        if screen == 'cart':
            self.driver.find_element(by=AppiumBy.XPATH,
                                     value='//android.view.ViewGroup[@content-desc="test-Cart"]/android.view.ViewGroup/android.widget.ImageView').click()

    def get_list_values(self, locator):
        elts = []
        if str(locator).endswith("_XPATH"):
            elts = self.driver.find_elements(by=AppiumBy.XPATH, value=read_locator(locator))
        return [elt.text for elt in elts]