import os, sys

script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, '..')
sys.path.append(mymodule_dir)
from settings import get_env


def pytest_html_report_title(report):
    report.title = f"DVDRental DB Regression Report"


def pytest_configure(config):
    config._metadata = {
        "QA ENV": get_env(sys.argv, '--env'),
        "App Version": "Coming soonish"
    }
