import re
import sys


def select_project(args):
    if re.search(r"(/|')countries(/|')", args):
        return {'project_name': 'countries', 'default_env': 'QA1'}
    elif re.search(r"(/|')dvdrental(/|')", args):
        return {'project_name': 'dvdrental', 'default_env': 'QA1'}
    else:
        return {'project_name': 'countries', 'default_env': 'QA1'}


args = str(sys.argv)
PROJECT = select_project(args)
