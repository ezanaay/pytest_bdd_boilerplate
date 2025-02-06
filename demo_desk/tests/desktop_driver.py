from pywinauto import Desktop, Application, timings
import time
import pytest

from lib.api_util.data_helper import search_dict
from lib.log import get_logger as log
from settings import LOG_LEVEL, CONSOLE_OUT
logger = log(__name__, LOG_LEVEL, CONSOLE_OUT)


def start_desktop_app(app_name):

    if app_name.lower() == 'calculator':
        # app object
        app = Application(backend="uia").start('calc.exe')
        logger.info("App is started.")
        # desktop object
        dlg = Desktop(backend="uia").Calculator
        time.sleep(3)
        pytest.test_data['api_data_with_response'].update({'app_obj': app, 'dialog_obj': dlg})

def close_app():
    app = search_dict('app_obj', pytest.test_data)
    app.kill()
    logger.info("App is stopped.")
