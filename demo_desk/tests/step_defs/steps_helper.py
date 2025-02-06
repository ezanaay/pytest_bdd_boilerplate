import time

import pytest
import re
from pywinauto import Desktop, Application, timings
import settings
from lib import log

logger = log.get_logger(__name__, settings.LOG_LEVEL, settings.CONSOLE_OUT)

from lib.api_util.data_helper import search_dict





def evaluate_query(query_str):
    dlg = search_dict('dialog_obj', pytest.test_data)
    for elt in query_str:
        enter_input(elt)
    dlg.type_keys("=")
    result = dlg.window(auto_id='CalculatorResults', control_type='Text').window_text()
    return result.split()[-1]


def enter_input(elt):
    dlg = search_dict('dialog_obj', pytest.test_data)
    if elt in map_elt.keys():
        dlg.window(auto_id=map_elt[elt], control_type='Button').click()
        logger.debug(f"Clicked on {elt}", extra={'key': elt})
    else:
        dlg.type_keys(elt)


map_elt = {
    '(': 'openParenthesisButton',
    ')': 'closeParenthesisButton',
    '+': 'plusButton'
}


def open_calc_menu(item):
    dlg = search_dict('dialog_obj', pytest.test_data)
    # breakpoint()
    dlg.child_window(auto_id="TogglePaneButton", control_type="Button").click()
    dlg.child_window(auto_id=item, control_type="ListItem").select()


def conversion_combobox(input_or_output, item):
    combobox_title = 'Input unit' if 'input' in input_or_output.lower() else 'Output unit'
    dlg = search_dict('dialog_obj', pytest.test_data)
    dlg.child_window(title=combobox_title, control_type="ComboBox").select(item)
    logger.debug(f"Selected {item} from combobox list.", extra={'key': item})


def unit_conversion(input, output):
    dlg = search_dict('dialog_obj', pytest.test_data)
    input_value = input.split()[0]
    input_unit = ' '.join(input.split()[1:])
    output_unit = ' '.join(output.split()[1:])
    conversion_combobox('input', input_unit)
    conversion_combobox('output', output_unit)
    enter_input(input_value)
    result_str = dlg.window(auto_id="Value2", control_type="Text").window_text()
    return re.findall(r"[-+]?(?:\d*\.*\d+)", result_str)[0]


def demo_id(name):
    mapped_name = search_dict(name, pytest.test_data)
    return mapped_name if mapped_name else name
