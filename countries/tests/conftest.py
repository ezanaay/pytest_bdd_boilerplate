import settings
from common_code.shared_steps.common_conf_helpers import prepare_report, after_scenario_tasks, before_scenario_tasks
from countries.tests.step_defs.common_imports import *
import pytest

es_index = 'pytestbdd-qa-logs-countries'

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
    after_scenario_tasks(request, scenario, es_index)


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    prepare_report(config, settings.PROJECT['project_name'])


@pytest.fixture
def pytestbdd_strict_gherkin():
    return False
