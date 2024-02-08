import os, sys

file_dir = os.path.dirname(__file__)
module_dir = os.path.join(file_dir, '..')
sys.path.append(module_dir)
from settings import get_env


def pytest_html_report_title(report):
    report.title = f"Countries API Regression Report"


def pytest_configure(config):
    config._metadata = {
        "QA ENV": get_env(sys.argv, '--env'),
        "App Version": "Coming soonish"
    }
