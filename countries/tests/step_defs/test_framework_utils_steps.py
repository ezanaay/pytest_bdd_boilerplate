from dvdrental.tests.step_defs.common_imports import *
from settings import LOG_LEVEL, CONSOLE_OUT
logger = log(__name__, LOG_LEVEL, CONSOLE_OUT)

scenarios(os.path.join(os.path.dirname(__file__), '../features/framework_utils.feature'))

