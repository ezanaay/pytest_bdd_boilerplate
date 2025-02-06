from elasticsearch import Elasticsearch
from requests.auth import HTTPBasicAuth
from lib.encryption import decrypt
from lib.log import get_logger as log
import os
import yaml
import sys
from config.project import PROJECT
from pathlib import Path
from proj_secrets import keys

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
project_name = PROJECT['project_name']
DATA_ROOT = os.path.join(PROJECT_ROOT, project_name, 'tests', 'data')
FEATURE_ROOT = os.path.join(PROJECT_ROOT, project_name, 'tests', 'features')
CONFIG_ROOT = os.path.join(PROJECT_ROOT, 'config')
LIB_ROOT = os.path.join(PROJECT_ROOT, 'lib')
LOG_ROOT = os.path.join(PROJECT_ROOT, 'logs')
WEB_DRIVER_ROOT = f'{LIB_ROOT}/web_drivers'
GLOBAL_DB_SESSION = []
LOG_LEVEL = 'INFO'
CONSOLE_OUT = False


with open(f"{CONFIG_ROOT}/setup.yml", 'r') as file:
    config = yaml.safe_load(file)


def get_env(args_list, arg):
    arg_index = args_list.index(arg) if arg in args_list else -1
    env = PROJECT['default_env']
    if arg_index > 0:
        env = args_list[arg_index + 1]
    elif os.environ.get("QA_ENV"):
        env = os.environ.get("QA_ENV")
    print(f'QA Environment = {env}')
    return env


def is_docker():
    cgroup = Path('/proc/self/cgroup')
    return Path('/.dockerenv').is_file() or (cgroup.is_file() and 'docker' in cgroup.read_text())


ENV = get_env(sys.argv, '--env')

CONFIG_DATA = config[project_name][ENV]
log_env_vars = CONFIG_DATA['log_setting']
LOG_LEVEL = log_env_vars['level'] if 'level' in log_env_vars else LOG_LEVEL
CONSOLE_OUT = log_env_vars['console_out'] if 'console_out' in log_env_vars else CONSOLE_OUT
JIRA_BASE_URL = CONFIG_DATA['jira_url']
logger = log(__name__, LOG_LEVEL, CONSOLE_OUT)

logger.info("Program started")

logger.info("QA Environment", extra={'ENV': ENV})

logger.debug(f'Config data = {CONFIG_DATA}')

DECRYPT_KEY = keys[project_name][ENV]

es = None
es_config = CONFIG_DATA['elasticsearch']

if es_config['turn_on']:
    es = Elasticsearch(es_config['hosts'], api_key=decrypt(eval(es_config['api_key']), DECRYPT_KEY))


def get_base_api_data(api_name, end_point, headers={}):
    api_data = CONFIG_DATA[api_name]
    url = api_data['host'] + end_point
    logger.debug('get base api data', extra={'url': url})
    if 'user' in api_data:
        return {"url": url, "auth": HTTPBasicAuth(api_data['user'],
                                                  decrypt(eval(api_data['password']), DECRYPT_KEY))}
    elif 'bearer_authorization' in api_data:
        return {"url": url,
                "headers": {
                               "Authorization": f"Bearer {decrypt(eval(api_data['bearer_authorization']), DECRYPT_KEY)}"} | headers}
    else:
        logger.warn(f"{api_data} doesnot contain the required base data")
        return {"url": url}


def get_db_uri(db_key):
    db_data = CONFIG_DATA[db_key]
    db_data['password'] = decrypt(eval(db_data['password']), DECRYPT_KEY)
    db_uri = "postgresql+psycopg2://%(username)s:%(password)s@%(host)s/%(db_name)s" % db_data
    return db_uri
