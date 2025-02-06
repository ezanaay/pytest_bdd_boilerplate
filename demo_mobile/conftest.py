import os, sys, time

import pytest
from appium.options.android import UiAutomator2Options
from appium import webdriver

file_dir = os.path.dirname(__file__)
module_dir = os.path.join(file_dir, '..')
sys.path.append(module_dir)
from settings import get_env


@pytest.fixture(scope="function")
def appium_driver(request):
    capabilities = {
        'deviceName': 'Pixel XL API 30',
        'platformName': 'Android',
        'automationName': 'UiAutomator2',
        'platformVersion': '11.0',
        'appPackage': 'com.google.android.contacts',
        'appActivity': 'com.google.android.apps.contacts.activities.PeopleActivity',
        'language': 'en',
        'locale': 'US'
    }
    driver = webdriver.Remote('http://localhost:4723',
                              options=UiAutomator2Options().load_capabilities(capabilities))
    request.cls.driver = driver
    driver.implicitly_wait(10)
    yield driver
    time.sleep(2)
    driver.quit()


def pytest_html_report_title(report):
    report.title = f"Demodesk Regression Report"


def pytest_configure(config):
    config._metadata = {
        "QA ENV": get_env(sys.argv, '--env'),
        "App Version": "Coming soonish"
    }
