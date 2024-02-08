
import pytest
from settings import LOG_LEVEL, CONSOLE_OUT
from pytest_bdd import given, then, parsers, when
from lib.api_util.data_helper import search_dict
from lib.log import get_logger as log
logger = log(__name__, LOG_LEVEL, CONSOLE_OUT)

@given(parsers.parse("the response status code for {query_name} is {code:d}"))
@then(parsers.parse("the response status code for {query_name} is {code:d}"))
def verify_status(query_name, code):
    api_data_with_resp = search_dict(query_name, pytest.test_data)
    url = search_dict('url', api_data_with_resp)
    method = search_dict('method', api_data_with_resp)
    resp = search_dict('response', api_data_with_resp)
    actual_code = resp.status_code

    logger.debug("Api request status",
                 extra={'url': url, 'method': method, 'actual_status_code': actual_code})
    assert actual_code == code, f"{method.upper()} {url}: actual status code {actual_code}. Expected: {code}"

