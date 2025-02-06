import re
import sys


def select_project(args):
    if re.search(r"(/|')demo_api(/|')", args):
        return {'project_name': 'demo_api', 'default_env': 'QA1'}
    elif re.search(r"(/|')demo_database(/|')", args):
        return {'project_name': 'demo_database', 'default_env': 'QA1'}
    elif re.search(r"(/|')demo_site(/|')", args):
        return {'project_name': 'demo_site', 'default_env': 'QA1'}
    elif re.search(r"(/|')demo_desk(/|')", args):
        return {'project_name': 'demo_desk', 'default_env': 'QA1'}
    elif re.search(r"(/|')demo_mobile(/|')", args):
        return {'project_name': 'demo_mobile', 'default_env': 'QA1'}
    else:
        return {'project_name': 'demo_api', 'default_env': 'QA1'}


args = str(sys.argv)
PROJECT = select_project(args)
