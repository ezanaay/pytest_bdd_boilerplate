from pytest_bdd import scenarios, scenario, given, then, parsers
import sys, os
import pytest
from stringcase import snakecase, pascalcase
import yaml

import time
from assertpy import assert_that, soft_assertions, soft_fail
from sttable import parse_str_table

script_dir = os.path.dirname(__file__)
lib_dir = os.path.join(script_dir, '..', '..', 'lib')
sys.path.append(lib_dir)
import lib.log as log

