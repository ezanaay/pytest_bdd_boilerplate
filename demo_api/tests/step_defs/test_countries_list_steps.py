import json

import settings
from common_code.shared_steps.shared_steps_helpers import is_str_dict_or_list
from demo_api.tests.step_defs.common_imports import *
import os
from pytest_bdd import scenarios, when

from lib.api_util.api import send_request
from lib.api_util.data_helper import prepare_api_data, get_yaml_test_data, search_dict, flatten_nested_dict

scenarios(os.path.join(os.path.dirname(__file__), '../features/countries_list_test.feature'))
logger = log.get_logger(__name__, settings.LOG_LEVEL, settings.CONSOLE_OUT)


@given(parsers.parse("a {query_name} request with params {params} is sent to {api_name}"),
       target_fixture='api_data_with_resp')
@then(parsers.parse("a {query_name} request with params {params} is sent to {api_name}"),
      target_fixture='api_data_with_resp')
def api_query(query_name, params, api_name):
    logger.info("Preparing api test data")
    if is_str_dict_or_list(params): params = json.loads(params)
    api_data = prepare_api_data(api_name, get_yaml_test_data(query_name), None, params)
    api_data_with_resp = {'response': send_request(api_data), 'api_data': api_data, 'api_name': api_name}
    pytest.test_data['api_data_with_response'].update({query_name: api_data_with_resp})
    return api_data_with_resp


@then(parsers.parse("I verify that {query_name} query response contains {q_response} for key {search_key}"))
def verify_response(request, query_name, q_response, search_key):
    api_data_with_resp = search_dict(query_name, pytest.test_data)
    response_jsn = search_dict('response', api_data_with_resp).json()
    expected = [item.strip() for item in q_response.split(',')]
    actual = [flatten_nested_dict(jsn)[search_key] for jsn in response_jsn]
    assert_that(sorted(actual)).is_equal_to(expected)


@then(parsers.parse("I verify that {query_name} query response has {count:d} entries"))
@when(parsers.parse("I verify that {query_name} query response has {count:d} entries"))
def response_count(query_name, count):
    api_data_with_resp = search_dict(query_name, pytest.test_data)
    response_jsn = search_dict('response', api_data_with_resp).json()
    assert_that(len(response_jsn)).is_equal_to(count)
