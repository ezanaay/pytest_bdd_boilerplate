import settings
from common_code.shared_steps.common_conf_helpers import after_scenario_tasks, prepare_report, before_scenario_tasks
import pytest
from lib.api_util.data_helper import search_dict

from lib.log import get_logger as log

logger = log(__name__, settings.LOG_LEVEL, settings.CONSOLE_OUT)

# elasticsearch index
es_index = 'dvdrental-automation'

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
    # close db session if there is any
    db_session = search_dict('db_session', pytest.test_data)
    if db_session:
        db_session.close()
        logger.info("DB Session is closed.")
    after_scenario_tasks(request, scenario, es_index)


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    prepare_report(config, settings.PROJECT['project_name'])


@pytest.fixture
def pytestbdd_strict_gherkin():
    return False
