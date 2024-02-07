import requests
import sys, os
from requests import Response
import lib.log as log
import settings
script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, '..', '..')
sys.path.append(mymodule_dir)


GET_API_TIMEOUT = 15
API_TIMEOUT = 60

logger = log.get_logger(__name__, settings.LOG_LEVEL, settings.CONSOLE_OUT)


def send_request(api_data: dict) -> Response:
    """
    A method that sends all types of api requests
    :param api_data: json/dict object that contains at least a method name(GET, POST, ...), an endpoint and a header
    :return: a Requests response object
    """
    response = {}

    # add api timeout
    api_data.update({'timeout': GET_API_TIMEOUT}) if api_data['method'].lower() == 'get' else api_data.update(
        {'timeout': API_TIMEOUT})
    logger.debug("API query data just before an api call", extra={'api_data': api_data})

    try:
        response = requests.request(**api_data)
        logger.debug(f"{api_data['method']} {api_data['url']} response status_code:",
                     extra={'response': response.status_code})

        return response if response.ok else response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        logger.exception(f"Url , {api_data['url']}, is incorrect", exc_info=errh)
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        logger.exception(f"Request for Url , '{api_data['url']}', has connection error", exc_info=errc)
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        logger.exception(f"Request for Url , '{api_data['url']}', has Timed out", exc_info=errt)
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        logger.exception(f"Request for Url , '{api_data['url']}', has an error", exc_info=err)
        print("General Error:", err)
    return response
