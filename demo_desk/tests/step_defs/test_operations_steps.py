import pytest
from pytest_bdd import scenario, given, when, then, parsers, scenarios
from pywinauto import Desktop, Application
from subprocess import Popen
import os
from assertpy import assert_that, soft_assertions, soft_fail
import settings
from demo_desk.tests.desktop_driver import start_desktop_app
from lib import log

logger = log.get_logger(__name__, settings.LOG_LEVEL, settings.CONSOLE_OUT)

from demo_desk.tests.step_defs.steps_helper import evaluate_query, open_calc_menu, \
    conversion_combobox, unit_conversion, demo_id
from lib.api_util.data_helper import search_dict

scenarios(os.path.join(os.path.dirname(__file__), '../features/jet_pricing.feature'))


@given(parsers.parse('I open "{demo_name}" app'))
def open_app(demo_name):
    name = demo_id(demo_name)
    start_desktop_app(name)


@then("I close the app")
def close_desktop_app():
    dlg = search_dict('dialog_obj', pytest.test_data)
    dlg.window(auto_id="Close", control_type='Button').click()


@given(parsers.parse('I open "{demo_name}" menu item'))
def open_menu_item(demo_name):
    name = demo_id(demo_name)
    open_calc_menu(name)


@then(parsers.parse('I verify the conversion from "{input}" equals "{output}"'))
def verify_unit_conversion(input, output):
    actual = unit_conversion(input, output)
    expected = output.split()[0]
    assert_that(actual).is_equal_to(expected)


@given(parsers.parse("based on the given {weather_condition}, {runway_condition}, {aircraft_performance}, {fuel_rate}"),
       target_fixture='lease_query_str')
def create_lease_query(weather_condition, runway_condition, aircraft_performance, fuel_rate):
    lease_query_str = f'({aircraft_performance}+{runway_condition}-{weather_condition})*{fuel_rate}/{weather_condition}'
    return lease_query_str


@then(parsers.parse('I verify that the calculated lease cost equals {expected}'))
def verify_operation(lease_query_str, expected):
    actual = evaluate_query(lease_query_str)
    assert_that(actual).is_equal_to(expected)


@then(parsers.parse('I verify that "{input}" aircraft fuel equals "{output}"'))
def verify_unit_conversion(input, output):
    actual = unit_conversion(input, output)
    expected = output.split()[0]
    assert_that(actual).is_equal_to(expected)
