import os
import time

import settings

import pytest
from pytest_bdd import scenario, given, when, then, parsers, scenarios
from assertpy import assert_that, soft_assertions, soft_fail

from demo_mobile.tests.pages.base_screen import BaseScreen
from demo_mobile.tests.pages.cart_screen import CartScreen
from demo_mobile.tests.pages.login_screen import LoginScreen
from demo_mobile.tests.pages.products_screen import ProductsScreen
from demo_mobile.tests.appium_helper import get_mobile_app_driver
from lib import log
from steps_helper import demo_id
from lib.api_util.data_helper import search_dict

scenarios(os.path.join(os.path.dirname(__file__), '../features/add_fleet.feature'))
logger = log.get_logger(__name__, settings.LOG_LEVEL, settings.CONSOLE_OUT)


@given(parsers.parse('I start "{demo_name}" mobile app'), target_fixture='driver')
def open_mobile_app(demo_name):
    name = demo_id(demo_name)
    time.sleep(5)
    driver = get_mobile_app_driver(name)
    return driver


@given(parsers.parse("I login as a {demo_name}"))
def login_as(driver, demo_name):
    name = demo_id(demo_name)
    LoginScreen(driver).login(name)


@given(parsers.parse("I should be on {screen_name} screen"))
def verify_landing_screen(driver, screen_name):
    screen_displayed = BaseScreen(driver).screen_displayed(screen_name)
    assert_that(screen_displayed).is_true()


@when(parsers.parse('I add "{demo_name}" to cart'))
def add_products(driver, demo_name):
    name = demo_id(demo_name)
    ProductsScreen(driver).add_product(name)
    BaseScreen(driver).navigate_to('cart')


@given(parsers.parse("I navigate to Cart screen"))
def navigate_to_cart(driver):
    BaseScreen(driver).navigate_to('cart')


@then(parsers.parse('"{demo_name}" should be available in the cart'))
def verify_cart_content(driver, demo_name):
    name = demo_id(demo_name)
    product_in_cart = CartScreen(driver).product_in_cart(name)
    assert_that(product_in_cart).is_true()


@given(parsers.parse("I sort fleet products based on {sort_criteria}"))
def select_sort_option(driver, sort_criteria):
    ProductsScreen(driver).sort_by(sort_criteria)


@then(parsers.parse("I verify that fleet product prices are sorted in {sort_direction} order"))
def verify_sort_order(driver, sort_direction):
    price_list = ProductsScreen(driver).get_prices()
    is_sorted = (sorted(price_list) == price_list) if 'increas' in sort_direction else (sorted(price_list, reverse=True) == price_list)
    assert_that(is_sorted).is_true()
