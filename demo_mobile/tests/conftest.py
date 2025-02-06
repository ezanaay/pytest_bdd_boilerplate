from datetime import datetime

import settings
from common_code.shared_steps.common_conf_helpers import prepare_report, after_scenario_tasks, before_scenario_tasks
from demo_api.tests.step_defs.common_imports import *
import pytest

from demo_mobile.tests.appium_helper import quit_driver
from lib.api_util.data_helper import search_dict

es_index = 'pytestbdd-qa-logs-demo_mobile'

logger = log.get_logger(__name__, settings.LOG_LEVEL, settings.CONSOLE_OUT)

pytest_plugins = (
    "config.project",
    "common_code.shared_steps.common_api_steps", "common_code.shared_steps.common_db_steps",
    "common_code.shared_steps.common_util_steps", "common_code.shared_steps.common_conf_helpers"
)


def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="QA2",
                     help="Option to choose QA environments - valid options are QA2 and QA3")


def pytest_bdd_apply_tag(tag, function):
    exec(f"function.{tag} = '{tag}'")
    return True


def pytest_bdd_before_scenario(scenario):
    before_scenario_tasks(scenario)


def pytest_bdd_after_scenario(request, feature, scenario):
    file_name = f'{datetime.today().strftime("%Y-%m-%dT%H-%M-%S")}.png'
    driver = search_dict('driver', pytest.test_data)
    driver.save_screenshot(file_name)
    quit_driver()
    after_scenario_tasks(request, scenario, es_index)


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    prepare_report(config, settings.PROJECT['project_name'])


@pytest.fixture
def pytestbdd_strict_gherkin():
    return False
