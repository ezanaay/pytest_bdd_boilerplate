from demo_mobile.tests.pages.base_screen import BaseScreen
import settings
from lib import log
logger = log.get_logger(__name__, settings.LOG_LEVEL, settings.CONSOLE_OUT)


class LoginScreen(BaseScreen):

    def __init__(self, driver):
        super().__init__(driver)

    def login(self, username):
        self.send_keys('username_input_ACCESSIBILITYID', username)
        self.send_keys('password_input_ACCESSIBILITYID', 'secret_sauce')
        self.click('login_btn_ACCESSIBILITYID')
