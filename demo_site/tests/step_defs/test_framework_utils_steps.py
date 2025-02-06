from demo_site.tests.step_defs.common_imports import *
from settings import LOG_LEVEL, CONSOLE_OUT, DATA_ROOT

logger = log(__name__, LOG_LEVEL, CONSOLE_OUT)

scenarios(os.path.join(os.path.dirname(__file__), '../features/framework_utils.feature'))
# scenarios(os.path.join(os.path.dirname(__file__), '../features/payroll_report_validation.feature'))

