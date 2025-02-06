import json

from common_imports import *
from pytest_bdd import scenarios, scenario, given, then, parsers, when

from demo_site.tests.pages.cart_page import CartPage
from demo_site.tests.pages.inventory_page import InventoryPage
from demo_site.tests.pages.login_page import LoginPage

scenarios(os.path.join(os.path.dirname(__file__), '../features/swag_products.feature'))


@given(parsers.parse("a {user_type} logs in"))
def login(browser, user_type):
    LoginPage(browser).login(user_type, 'secret_sauce')


@given(parsers.parse("the user should be on {page_name} page"))
@when(parsers.parse("the user should be on {page_name} page"))
@then(parsers.parse("the user should be on {page_name} page"))
def verify_page(browser, page_name):
    expected_url = getattr(sys.modules[__name__], f'{page_name.capitalize()}Page')(browser).pg_url
    assert_that(browser.get_url()).is_equal_to(expected_url)


@then(parsers.parse("{actual_items} on {page_name} page should contain {expected_items}"))
def verify_content(browser, actual_items, page_name, expected_items):
    page_obj = getattr(sys.modules[__name__], pascalcase(f'{snakecase(page_name)}_page'))(browser)
    get_list = getattr(page_obj, f'get_{snakecase(actual_items)}')()
    expected_items = [item.strip() for item in expected_items.split(',')]
    assert_that(get_list).is_equal_to(expected_items)


@when(parsers.parse("the user adds {product_names} to cart"))
def add_item_to_cart(browser, product_names):
    product_names = [item.strip() for item in product_names.split(',')]
    [InventoryPage(browser).add_product_to_cart(item) for item in product_names]


@when(parsers.parse("the user navigates to {page_name} page"))
def navigate_to_cart_page(browser, page_name):
    InventoryPage(browser).navigate_to(page_name.lower())
    expected_url = CartPage(browser).pg_url
    assert_that(browser.get_url()).is_equal_to(expected_url)


@then(parsers.parse("{product_names} should be available in cart"))
def verify_cart_content(browser, product_names):
    expected_products = [item.strip() for item in product_names.split(',')]
    cart_content = CartPage(browser).get_items_in_cart()
    assert_that(cart_content).is_equal_to(expected_products)
