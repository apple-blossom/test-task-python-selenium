# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By

from pages.base import Base


class MainPage(Base):

    """ Main page class"""

    MENU_WRAPPER_LOCATOR = (By.CSS_SELECTOR, ".ml-auto")
    MENU_LOGO = (By.ID, "nava")
    MENU_SIGNUP_LOCATOR = (By.ID, "signin2")
    MENU_LOGIN_LOCATOR = (By.ID, "login2")
    MENU_WELCOME_LOCATOR = (By.ID, "nameofuser")
    MENU_CART_LOCATOR = (By.ID, "cartur")
    CATEGORY_WRAPPER_LOCATOR = (By.ID, "cat")
    PRODUCTS_GRID_LOCATOR = (By.ID, "tbodyid")

    def __init__(self, driver):
        super().__init__(driver)

    def click_header_logo(self):
        self.driver.find_element(*self.MENU_LOGO).click()

    def wait_for_main_page_to_load(self):
        self.wait_for_element_to_be_present(self.CATEGORY_WRAPPER_LOCATOR)

    def open_category_tab(self, expected_catalog_item_title, item_to_open_text):
        item_title_locator = self.locator_by_text(item_to_open_text, "a")
        self.open_item(self.CATEGORY_WRAPPER_LOCATOR, expected_catalog_item_title)
        self.wait_for_element_to_be_present(item_title_locator)

    def open_catalog_product(self, product_name):
        self.open_item(self.CATEGORY_WRAPPER_LOCATOR, product_name, "a")

    def open_sign_in_menu(self):
        self.driver.find_element(*self.MENU_SIGNUP_LOCATOR).click()

    def open_log_in_menu(self):
        self.driver.find_element(*self.MENU_LOGIN_LOCATOR).click()

    def open_cart(self):
        self.wait_for_element_to_be_present(self.MENU_CART_LOCATOR)
        self.driver.find_element(*self.MENU_CART_LOCATOR).click()

    def wait_for_welcome_title(self):
        self.wait_for_element_to_be_present(self.MENU_WELCOME_LOCATOR)

    def get_welcome_title(self):
        self.wait_for_welcome_title()
        return self.driver.find_element(*self.MENU_WELCOME_LOCATOR).text
