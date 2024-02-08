from datetime import datetime, timedelta, timezone
from stringcase import snakecase
import sys, os
import yaml

import flatdict

from lib.datetime_helper import replace_date_vars
from settings import DATA_ROOT, get_base_api_data, CONSOLE_OUT, LOG_LEVEL

script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, '..', '..')
sys.path.append(mymodule_dir)
from lib.api_util.nested_lookup import nested_lookup, nested_delete
import lib.log as log

import json
import pytest

logger = log.get_logger(__name__, LOG_LEVEL, CONSOLE_OUT)

"""
Collection of functions that contains data helper methods. To cleanup, search, generate and modify data
"""


def search_dict(key: str, data: dict, expected_count=1) -> [str, list]:
    """
    Searches a value(s) of a given key
    :param key: dict key to be searched for
    :param data: a nested dict that we want to search for the value of a key
    :param expected_count: do we want a list of values or just one value. Any expected_count value other than 1 will return a list.
     if expected_count is 1, which is the default for this method, it will return only a searched value, not a list
    :return: returns the value of the searched key
    """
    logger.debug(f"'Started searching key '{key}' in nested dict {data}'")
    result_list = nested_lookup(document=data, key=key)

    logger.debug(f'Nested dict search for key "{key}" has {len(result_list)} count')
    logger.debug(f'{key} search result = {result_list})')

    if len(result_list) == 0:
        logger.warning(f'"{key}" is not present in the nested hash.')
        return []
    return result_list[0] if expected_count == 1 else result_list


def generate_vars() -> dict:
    """
    dynamic data that will be integrated to our test executions
    :return: dict of dynamic data that will be available for scenario test data to make it dynamic
    """
    now = datetime.now(timezone.utc)
    return {'today_mdy': now.strftime("%m/%d/%Y"),
            'today_ydm': now.strftime("%Y/%d/%m"),
            'today_ydm_dash': now.strftime("%Y-%m-%d"),
            'rand_str': now.strftime("%m%d%H%M%S%f"),
            'iso_now': now.isoformat()[:-6] + '000Z',
            }


# replace_with is a dictionary
def replace_variables(data, replace_with=None, ignore_error=False):
    """
    Replaces variables in a dictionary object
    :param data: dict object with dynamic variables
    :param replace_with: optional dict object with variable name key and value the value of the variable
    :param ignore_error: If it is True returns a dict with variables ( variables are not replaced).
    False will make the return strict such that the returned value should have all variables replaced
    :return: a dict object
    """
    logger.info('Started replacing dict variables')
    dynamic_vars = pytest.test_data['dynamic_vars']

    logger.info('merging dynamically generated variables with scenario specific variables dict data')
    replace_with = {**replace_with, **dynamic_vars} if replace_with else dynamic_vars

    # logger.info("'replace_with' variables content", extra= {'replace_with': replace_with})
    replaced = ''
    try:
        dict_str = json.dumps(data)
        dict_str = replace_date_vars(dict_str)
        replaced = dict_str % replace_with
    except Exception as e:
        if ignore_error:
            replaced = json.dumps(data)
            pass
        else:
            str(e)
    logger.debug('Completed replacing dict variables', extra={'replaced': replaced})
    return json.loads(replaced)


def prepare_content(content, method):
    """
    Based on a given method(GET, POST, PATCH) it will assign the content as params or as a body
    :param content: dict object
    :param method: method name (GET, POST, PATCH)
    :return: dict object
    """
    if method.lower() == 'get':
        logger.debug('Preparing params for GET method', extra={'params': content})
        return {'params': content}
    else:
        logger.debug(f'Preparing payload for "{method}" method', extra={'content': content})
        return {'json': content}


def prepare_api_data(api_name, api_data, content=None, replace_with=None, ignore_error=False):
    """
    Prepares a dict/json api data that can be used in `send_request` method
    :param api_name: required api name key available in config/setup.yml
    :param api_data: required raw incomplete api data that needs to be cleaned up and prepared for successful api requests
    :param content: Optional params/body dict objects
    :param replace_with: Optional dict of dynamic variables that will be used to replace variables in the raw incomplete api_data
    :param ignore_error: Optional Boolean object to make it strict when there is an error during data processing
    :return:
    """
    api_data = replace_variables(api_data, replace_with, ignore_error)
    logger.debug('api_data after replacing variables', extra={'api_data': api_data})

    logger.info('merging basic env specific api data with scenario specific api data')
    headers = api_data['headers'] if api_data and ('headers' in api_data.keys()) else {}

    base_data = get_base_api_data(snakecase(api_name.lower()), api_data['endpoint'], headers)

    # Content will be either params for GET requests or body for other type of requests
    if content: api_data = {**api_data, **prepare_content(content, api_data['method'])}

    api_data = {**api_data, **base_data}

    if 'data' in api_data:
        logger.info('convert "data" key to json string')
        api_data['data'] = json.dumps(api_data['data'])
        logger.debug('Converted payload "data"', extra={'data': api_data['data']})

    for k in ['assert', 'endpoint']: nested_delete(api_data, k, in_place=True)
    logger.debug('api_data ready for a Request call', extra={'api_data': api_data})

    logger.info('api_data ready for a Request call')
    return api_data


def get_yaml_test_data(yml_key):
    """
    Searches and returns content of a given key from a collection of test data yaml files
    :param yml_key: test data key that contains scenario test data
    :return: returns a dict object or errors out if the key is not available
    """
    directory = DATA_ROOT

    logger.info(f"Started searching for YAML key '{yml_key}' in directory '{directory}'")
    try:
        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)
            # checking if it is a yaml file
            if os.path.isfile(f) and f.endswith('.yml'):
                with open(f, 'r') as file:
                    scenario_data = yaml.safe_load(file)
                if yml_key.lower() in scenario_data:
                    logger.info(f"Found YAML key '{yml_key}' in filename '{filename}'")
                    logger.info(f"YAML key '{yml_key}' data is",
                                extra={yml_key: scenario_data[yml_key.lower()]})
                    return scenario_data[yml_key.lower()]
    except KeyError as e:
        logger.error(
            f"The key, '{yml_key}', was not found in the test data directory, '{directory}'. Please check data key spelling or the format.",
            exc_info=e)
        raise KeyError(e)


def flatten_nested_dict(dic: dict) -> flatdict:
    """
    Converts a given nested dict to a flattened single level dict object
    :param dic: nested dict
    :return: single level flattened dict object
    """
    logger.debug('Dict before flattening:', extra={'dict': dic})
    flattened_dict = flatdict.FlatDict(dic, delimiter='.')

    logger.debug(f"Started flattening dict with delimiter '.'")
    return flattened_dict


def search_item_from_list_of_dict(list_of_dict, key, value):
    """
    Searches a particular dict item from a list of dicts that contains a particular key value pair
    :param list_of_dict: List of dicts
    :param key: search for key
    :param value: value of the key to search for
    :return: dict item
    """
    return next((item for item in list_of_dict if item[key] == value), None)
