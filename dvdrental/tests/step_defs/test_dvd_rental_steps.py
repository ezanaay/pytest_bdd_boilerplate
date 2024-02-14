import settings
from dvdrental.utils.queries import DBQueries
from dvdrental.tests.step_defs.common_imports import *
import os
from pytest_bdd import scenarios

from lib.model.create_db_session import db_session
from settings import LOG_LEVEL, CONSOLE_OUT

logger = log(__name__, LOG_LEVEL, CONSOLE_OUT)

scenarios(os.path.join(os.path.dirname(__file__), '../features/dvd_rental_tests.feature'))


@given(parsers.parse('I query {db_name} database for {query_name} for "{query_param}#{param_name}"'),
       target_fixture='db_result')
def step_impl(db_name, query_name, query_param, param_name):
    session = settings.GLOBAL_DB_SESSION if settings.GLOBAL_DB_SESSION else db_session(db_name)
    result = DBQueries(session).query_for(query_name, query_param)
    logger.debug(f"{query_name} query result", extra={'db_rows': result})
    pytest.test_data.update({query_name: result})
    return result


@then(parsers.parse('I verify that "{query_name}" contains {count:d} db entries'))
# The other option to get data from previous step is to include db_result fixture as an arg from the previous step
# def verify_count(query_name, count, db_result):
def verify_count(query_name, count):
    actual_count = len(pytest.test_data[query_name])
    logger.debug(f"{query_name} actual count", extra={'count': actual_count})
    assert_that(actual_count).is_equal_to(count)
