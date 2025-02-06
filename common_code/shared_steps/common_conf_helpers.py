import os
import traceback
from datetime import datetime

import pytest

from lib.api_util.data_helper import generate_vars, get_yaml_test_data
from lib.log import get_logger as log
import settings
from settings import LOG_LEVEL, CONSOLE_OUT

logger = log(__name__, LOG_LEVEL, CONSOLE_OUT)

"""
A collection of conftest helper methods and fixtures
"""


def before_scenario_tasks(scenario):
    """
    setup method that runs tasks (setup common data, store scenario info) that are required before a scenario
    :param scenario: pytest scenario object
    :return: None
    """
    print(str('Start time: ' + str(datetime.now())))
    pytest.scenario_tags = [tag.strip() for tag in scenario.tags]
    logger.info(f"Started scenario {scenario.name}.")
    if 'skip' in pytest.scenario_tags: pytest.skip(reason=f"{scenario.name} Marked with Skip tag")
    mapping = get_yaml_test_data('nj_demo_mapper')
    pytest.test_data = {'dynamic_vars': generate_vars(), 'api_data_with_response': {}, 'demo_mapper': mapping}


def after_scenario_tasks(request, scenario, es_index):
    """
    teardown and reporting method that runs tasks (cleanup test data, prepare report) after a scenario completes running
    :param request: pytest request object
    :param scenario: pytest scenario object
    :param es_index: elasticsearch index if there is elasticsearch integration for reporting
    :return: None
    """

    if settings.es and es_index:
        update_elasticsearch_report(es_index, request)
    scenario_cleanup_method = [tag for tag in scenario.tags if "scenario_cleanup" in tag]
    if scenario_cleanup_method:
        clean_up_data(scenario_cleanup_method, request)
    else:  # Scenario has failed. Logging traceback
        logger.error("Scenario has failed.", exc_info=traceback.format_exc())
    if scenario_failed(request):
        logger.error(f"Scenario {scenario.name} has FAILED.", exc_info=traceback.format_exc())
    else:
        logger.info(f"Scenario {scenario.name} has PASSED.")
    pytest.test_data = {}
    print(str('End time: ' + str(datetime.now())))


def update_elasticsearch_report(es_index, request):
    es = settings.es
    report_data = {'index': es_index}
    scenario_data = es_scenario_report_data(request)
    report_data.update({'document': scenario_data})
    es.index(**report_data)


def es_scenario_report_data(request):
    env = settings.ENV.lower()
    time_str = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    project_name = settings.PROJECT['project_name']

    try:
        if pytest.regression_id is None: pytest.regression_id = {'regression_id': f'{env}_{time_str}'}
    except Exception as e:
        pytest.regression_id = {'regression_id': f'{env}_{time_str}', 'env': env, 'project': project_name}

    scenario_report = {**request.node.__scenario_report__.serialize(),
                       **{'status': 'pass'}, **pytest.regression_id, **{'@timestamp': datetime.now().isoformat()},
                       'jira_links': get_jira_links()}

    if scenario_failed(request):
        pytest.test_data.pop('dynamic_vars')

        # Prepare error message for elasticsearch reporting
        traceback_data = traceback.format_exc()
        error_category = ((str(traceback_data)).split("Error", 1)[0]).split()[-1] + ' Error'
        trcbk_lines = traceback_data.splitlines()
        error_message = '***'.join(trcbk_lines[:4] + trcbk_lines[-4:])

        scenario_report.update(
            {'error_message': str(error_message), 'traceback_info': str(traceback_data),
             'status': 'fail', 'test_data': str(pytest.test_data), 'error_category': error_category})

    return scenario_report


def scenario_failed(request):
    scenario_report = request.node.__scenario_report__.serialize()

    logger.debug(f'Scenario details', extra={'scenario_report': scenario_report})
    scenario_has_failed = any([step['failed'] for step in scenario_report['steps']])

    if scenario_has_failed:
        logger.warning(f"Scenario, '{scenario_report['name']}', has failed",
                       extra={'scenario_has_failed': scenario_has_failed})
    else:
        logger.info(f"Scenario, '{scenario_report['name']}', has passed")

    return scenario_has_failed


def clean_up_data(data_cleanup_method, request):
    try:
        logger.debug(f'Started cleaning up data, "{data_cleanup_method}"')
        eval(data_cleanup_method[0])(request)
    except NameError:
        raise NameError(
            f"\n---Your scenario has tag '@{data_cleanup_method[0]}'."
            f"\n---Attempted to run data cleanup method '{data_cleanup_method[0]}' but it does not exist.")


def prepare_report(config, project_name):
    report_path = f'{settings.PROJECT_ROOT}/{project_name}/reports'
    if not os.path.exists(report_path):
        os.makedirs(report_path)
    time_str = datetime.now().strftime('%Y-%m-%dT%H-%M-%S')
    config.option.htmlpath = f'{report_path}/{time_str}-{project_name}-QAReport.html'
    config.option.self_contained_html = True


def get_jira_links():
    jira_links = [f"{settings.JIRA_BASE_URL}/{tag.split('_')[-1]}" for tag in pytest.scenario_tags if 'jira_' in tag]
    return '\n'.join(jira_links)
