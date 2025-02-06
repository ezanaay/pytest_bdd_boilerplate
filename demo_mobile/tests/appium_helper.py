import os

import pytest
from appium.options.android import UiAutomator2Options
from appium import webdriver
import time

from lib.api_util.data_helper import search_dict


# @pytest.fixture(scope="function")
def appium_driver(additional_cap):  # request
    capabilities = {
        # 'deviceName': 'Pixel 5 API 29',
        'platformName': 'Android',
        'automationName': 'UiAutomator2',
        'platformVersion': '11.0',
        # 'language': 'en',
        # 'locale': 'US'
    }
    capabilities.update(additional_cap)
    driver = webdriver.Remote('http://localhost:4723',
                              options=UiAutomator2Options().load_capabilities(capabilities))
    # request.cls.driver = driver
    # breakpoint()
    driver.implicitly_wait(10)
    pytest.test_data['api_data_with_response'].update({'driver': driver})
    return driver
    # yield driver
    # time.sleep(2)
    # driver.quit()


def get_app_id(app_name):
    if app_name.lower() == 'contacts':
        app_capability = {'appPackage': 'com.google.android.contacts',
                          'appActivity': 'com.google.android.apps.contacts.activities.PeopleActivity',
                          'noReset': 'false',
                          'fullReset': 'true'}
        return app_capability
    if app_name.lower() == 'sauce labs':
        app_capability = {
            'appPackage': 'com.swaglabsmobileapp',
            'appActivity': 'com.swaglabsmobileapp.MainActivity',
            'app': os.path.join(os.path.dirname(__file__), 'app/Android.SauceLabs.Mobile.Sample.app.2.7.1.apk')
        }
        return app_capability


def get_mobile_app_driver(app_name):
    return appium_driver(get_app_id(app_name))


def capture_screenshot():
    driver = search_dict('driver', pytest.test_data)
    screenshotBase64 = driver.get_screenshot_as_base64()


def quit_driver():
    driver = search_dict('driver', pytest.test_data)
    driver.quit()
