from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By


# this Base class is serving basic attributes for every single page inherited from Page class
class BasePage(object):
    def __init__(self, driver, base_url='https://www.saucedemo.com/'):
        self.base_url = base_url
        self.driver = driver
        self.timeout = 30

    def find_element(self, *locator):
        return self.driver.find_element(*locator)

    def find_elements(self, *locator):
        return self.driver.find_elements(*locator)

    def open(self, url):
        url = self.base_url + url
        self.driver.get(url)

    def get_title(self):
        return self.driver.title

    def get_url(self):
        return self.driver.current_url

    def hover(self, *locator):
        element = self.find_element(*locator)
        hover = ActionChains(self.driver).move_to_element(element)
        hover.perform()

    def wait_element(self, *locator):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(locator))
        except TimeoutException:
            print("\n * ELEMENT NOT FOUND WITHIN GIVEN TIME! --> %s" % (locator[1]))
            self.driver.quit()

    def type_into_element(self, text, locator_name, locator_value):
        element = self.get_element(locator_name, locator_value)
        element.click()
        element.clear()
        element.send_keys(text)

    def element_click(self, locator_name, locator_value):
        element = self.get_element(locator_name, locator_value)
        element.click()

    def check_display_status_of_element(self, locator_name, locator_value):
        element = self.get_element(locator_name, locator_value)
        return element.is_displayed()

    def retrieve_element_text(self, locator_name, locator_value):
        element = self.get_element(locator_name, locator_value)
        return element.text

    def get_element(self, locator_name, locator_value):
        element = None
        if locator_name.endswith("_id"):
            element = self.driver.find_element(By.ID, locator_value)
        elif locator_name.endswith("_name"):
            element = self.driver.find_element(By.NAME, locator_value)
        elif locator_name.endswith("_class_name"):
            element = self.driver.find_element(By.CLASS_NAME, locator_value)
        elif locator_name.endswith("_link_text"):
            element = self.driver.find_element(By.LINK_TEXT, locator_value)
        elif locator_name.endswith("_xpath"):
            element = self.driver.find_element(By.XPATH, locator_value)
        elif locator_name.endswith("_css"):
            element = self.driver.find_element(By.CSS_SELECTOR, locator_value)
        return element

    def populate_page(self, data):
        # Wait for the page to load
        wait = WebDriverWait(self.driver, 10)

        # Find and fill in the form fields
        for key, value in data.items():
            by = self.element_loc(key.split('_')[-1])
            loc = f'self.locator.{key}'
            element = wait.until(EC.presence_of_element_located(eval(by), eval(loc)))
            if element.get_attribute("type") in self.type_into_fields():
                element.send_keys(value)
            else:
                element.click()

    def element_loc(self, suffix):
        select_loc = {'id': 'By.ID', 'name': 'By.NAME',
                      'classname': 'By.CLASS_NAME', 'linktext': 'By.LINK_TEXT',
                      'xpath': 'By.XPATH', 'css': 'By.CSS_SELECTOR'}
        if select_loc[suffix]:
            return select_loc[suffix]
        else:
            raise f"{suffix} is not a valid option as element identifier."

    def type_into_fields(self):
        return ['text', 'password',
                'email', 'number',
                'date', 'hidden']

    def click_fields(self):
        return ['checkbox', 'radio',
                'submit', 'button',
                'file', 'hidden']
