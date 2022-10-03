# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from helpers.data_helper import *


class Base(object):
    """ Basic class for pages """

    test_data = get_test_data()
    default_timeout = test_data["testConfig"]["defaultWaitTimeout"]

    def __init__(self, driver):
        self.driver = driver

    @staticmethod
    def setup_with_headless():
        options = Options()
        options.add_argument("--headless")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('start-maximized')
        des_cap = DesiredCapabilities.CHROME
        des_cap['loggingPrefs'] = {'browser': 'ALL'}
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),  options=options)
        return driver

    @staticmethod
    def locator_by_text(text, node="*"):
        return By.XPATH, f"//{node}[contains(text(),'{text}')]"

    def js_scroll(self, *locator):
        el = self.driver.find_element(*locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", el)

    def open_item(self, wrapper_locator, item_to_open_text, node="*"):
        item_locator = self.locator_by_text(item_to_open_text, node)
        self.driver.find_element(*wrapper_locator).find_element(*item_locator).click()

    @screenshot_decorator
    def wait_for_alert(self):
        WebDriverWait(self.driver, self.default_timeout).until(EC.alert_is_present())

    @screenshot_decorator
    def wait_for_element_to_be_present(self, locator):
        WebDriverWait(self.driver, self.default_timeout).until(EC.visibility_of_element_located(locator))

    @screenshot_decorator
    def wait_for_all_elements_to_be_present(self, locator):
        WebDriverWait(self.driver, 15).until(EC.presence_of_all_elements_located(locator))

    @screenshot_decorator
    def wait_for_text_to_be_preset(self, locator, text):
        WebDriverWait(self.driver, self.default_timeout).until(EC.text_to_be_present_in_element(locator, text))

    def get_alert_text_and_close(self):
        alert = self.driver.switch_to.alert
        alert_text = alert.text
        alert.accept()
        return alert_text

    def add_auth_cookie(self, cookie_name, cookie_value):
        self.driver.add_cookie({"name": cookie_name, "value": cookie_value})
