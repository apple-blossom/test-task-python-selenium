# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By

from pages.base import Base


class SignUpLogInPage(Base):

    """ Sign Up popup """

    LOGIN_BTN_LOCATOR = (By.XPATH, "//button[contains(text(),'Log in')]")
    SIGNUP_BTN_LOCATOR = (By.XPATH, "//button[contains(text(),'Sign up')]")
    CLOSE_BTN_LOCATOR = (By.XPATH, "//button[contains(text(),'Close')]")
    USERNAME_SIGNUP_LOCATOR = (By.ID, "sign-username")
    PASSWORD_SIGNUP_LOCATOR = (By.ID, "sign-password")
    USERNAME_LOGIN_LOCATOR = (By.ID, "loginusername")
    PASSWORD_LOGIN_LOCATOR = (By.ID, "loginpassword")

    def __init__(self, driver):
        super().__init__(driver)

    def wait_for_sign_up_form_to_load(self):
        self.wait_for_element_to_be_present(self.SIGNUP_BTN_LOCATOR)

    def wait_for_log_in_form_to_load(self):
        self.wait_for_element_to_be_present(self.LOGIN_BTN_LOCATOR)

    def fill_sign_up_form(self, username, password):
        self.driver.find_element(*self.USERNAME_SIGNUP_LOCATOR).send_keys(username)
        self.driver.find_element(*self.PASSWORD_SIGNUP_LOCATOR).send_keys(password)

    def fill_in_log_in_form(self, username, password):
        self.driver.find_element(*self.USERNAME_LOGIN_LOCATOR).send_keys(username)
        self.driver.find_element(*self.PASSWORD_LOGIN_LOCATOR).send_keys(password)

    def press_sign_up(self):
        self.driver.find_element(*self.SIGNUP_BTN_LOCATOR).click()

    def press_log_in(self):
        self.driver.find_element(*self.LOGIN_BTN_LOCATOR).click()
