from .locators import *
from .base_page import BasePage
# from utils import users


class LoginPage(BasePage):
# class LoginPage:
    def __init__(self, driver):
        self.locator = LoginPageLocators
        self.suffix = ''
        super().__init__(driver)

    def enter_username(self, email):
        self.find_element(*self.locator.username).send_keys(email)

    def enter_password(self, password):
        self.find_element(*self.locator.password).send_keys(password)

    def click_login_button(self):
        self.find_element(*self.locator.submit).click()

    def login(self, user, password):
        print(user)
        self.enter_username(user)
        self.enter_password(password)
        self.click_login_button()
