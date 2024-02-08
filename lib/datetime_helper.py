import json
import re
from datetime import datetime, timedelta, timezone
from dateutil.parser import parse
import ast
from settings import LOG_LEVEL, CONSOLE_OUT
import lib.log as log

logger = log.get_logger(__name__, LOG_LEVEL, CONSOLE_OUT)
"""
Creates a time interval 5 minutes before and 5 minutes after the given date.
"""


def create_time_interval(base_date, interval=5):
    date_time_obj = datetime.fromisoformat(base_date)
    start_time = str(date_time_obj - timedelta(minutes=interval))
    start_time = start_time.replace(" ", "T")
    end_time = str(date_time_obj + timedelta(minutes=interval))
    end_time = end_time.replace(" ", "T")

    return start_time, end_time


def is_str_num(str) -> bool:
    try:
        int(str)
        return True
    except ValueError:
        try:
            float(str)
            return True
        except ValueError:
            return False


def is_str_date(str):
    if is_str_num(str): return False
    try:
        logger.debug(f"'{str}' string is a date object. Changing the string to Date format")
        parse(str, fuzzy=False)
        return True
    except ValueError:
        logger.debug(f"'{str}' string is not a date object")
        return False


def convert_str_date_format(value):
    if is_str_date(value):
        return parse(value, fuzzy=False).date()
    else:
        return value


# accepts datetime objects
def is_given_time_in_time_period(start_time, end_time, given_time):
    if start_time < end_time:
        return given_time >= start_time and given_time <= end_time
    else:
        # Over midnight:
        return given_time >= start_time or given_time <= end_time


# This method converts custom str dates when passed as %(custom_date)t:
# 1_year_ago returns current_date - 1 year
# 2_year_after returns current_date + 2 year
# 37_days_ago returns current_date - 37 days
# 20_weeks_ago returns current_date - 20 weeks
# 1_year_ago-7_day returns (current_date - 1 year - 7_days)
# 3_year_after-7_day returns (current_date + 3 year - 7_days)
# 0_year_ago+7_day returns (current_year_start_date + 7_days)
def replace_date_vars(str):
    date_vars = re.findall(r'%\((.*?)\)t', str)
    if not date_vars: return str
    for date_var in date_vars:
        str = str.replace(f'%({date_var})t', time_calc(date_var))
    return str


def time_calc(given_time, ref=datetime.now(timezone.utc)):
    if any(op in given_time for op in ['+', '-']):
        ref_str, sup = re.split('\+|\-', given_time)
        ref = eval_time(ref_str, ref)
        before_or_after = 'after' if '+' in given_time else 'ago'
        given_time = f'{sup}_{before_or_after}'
    return eval_time(given_time, ref).isoformat()[:-6] + '000Z'


def eval_time(given_time, ref=datetime.now(timezone.utc)):
    len, type, bk_or_after = given_time.split('_')
    if type == 'year':
        if int(len) == 0: return datetime(datetime.today().year, 1, 1, 0, 0, 0, 100000)
        len, type = f'{int(len) * 52}', 'weeks'
    if type[-1] != 's':
        type += 's'
    frequencies = ['seconds', 'minutes', 'hours', 'days', 'weeks']
    if type in frequencies:
        len = -int(len) if bk_or_after in ['ago'] else int(len)
        kwargs = {type: len}
        ztime = (ref + timedelta(**kwargs))
    else:
        raise ValueError(f"{given_time} should have {frequencies}.")
    return ztime


# given_date should be a datetime object
def previous_weekday(ref_date):
    ref_date -= timedelta(days=1)
    while ref_date.weekday() > 4:  # Mon-Fri are 0-4
        ref_date -= timedelta(days=1)
    return ref_date
