# -*- coding: utf-8 -*-
from time import sleep

from selenium.webdriver.common.by import By

from pages.base import Base


class CartPage(Base):

    """ Cart page class"""

    CART_ITEMS_TABLE_LOCATOR = (By.ID, "tbodyid")
    CART_ITEMS_TITLE_LOCATOR = (By.CSS_SELECTOR, "tr td:nth-of-type(2)")
    CART_ITEMS_PRICE_LOCATOR = (By.CSS_SELECTOR, "tr td:nth-of-type(3)")
    TOTAL_PRICE_LOCATOR = (By.ID, "totalp")
    ORDER_BTN_LOCATOR = (By.CSS_SELECTOR, ".btn-success")
    ORDER_FORM_NAME_LOCATOR = (By.ID, "name")
    ORDER_FORM_COUNTRY_LOCATOR = (By.ID, "country")
    ORDER_FORM_CITY_LOCATOR = (By.ID, "city")
    ORDER_FORM_CARD_NUMBER_LOCATOR = (By.ID, "card")
    ORDER_FORM_CARD_MONTH_LOCATOR = (By.ID, "month")
    ORDER_FORM_CARD_YEAR_LOCATOR = (By.ID, "year")
    ORDER_FORM_PURCHASE_BTN_LOCATOR = (By.CSS_SELECTOR, "#orderModal .btn-primary")
    ORDER_ALERT_MESSAGE_LOCATOR = (By.CSS_SELECTOR, ".sweet-alert h2")
    ORDER_ALERT_DETAILS_LOCATOR = (By.CSS_SELECTOR, ".sweet-alert .text-muted")
    ORDER_ALERT_SUBMIT_LOCATOR = (By.CSS_SELECTOR, ".sweet-alert .confirm")

    def __init__(self, driver):
        super().__init__(driver)

    def wait_for_cart_to_load(self):
        self.wait_for_element_to_be_present(self.CART_ITEMS_TABLE_LOCATOR)

    def wait_for_cart_items_to_load(self):
        self.wait_for_all_elements_to_be_present(self.CART_ITEMS_TITLE_LOCATOR)

    def get_cart_product_titles(self):
        titles = self.driver.find_elements(*self.CART_ITEMS_TITLE_LOCATOR)
        return [title.text for title in titles]

    def get_cart_items_price(self):
        prices = self.driver.find_elements(*self.CART_ITEMS_PRICE_LOCATOR)
        return [int(price.text) for price in prices]

    def get_cart_product_sum(self):
        prices = self.get_cart_items_price()
        return sum([int(price) for price in prices])

    def get_total_price(self):
        return int(self.driver.find_element(*self.TOTAL_PRICE_LOCATOR).text)

    def press_order_button(self):
        return self.driver.find_element(*self.ORDER_BTN_LOCATOR).click()

    def press_purchase_button(self):
        return self.driver.find_element(*self.ORDER_FORM_PURCHASE_BTN_LOCATOR).click()

    def wait_for_purchase_form_to_load(self):
        self.wait_for_element_to_be_present(self.ORDER_FORM_NAME_LOCATOR)

    def fill_purchase_form(self, name, country, city, card_number, card_expiration_month, card_expiration_year):
        self.driver.find_element(*self.ORDER_FORM_NAME_LOCATOR).send_keys(name)
        self.driver.find_element(*self.ORDER_FORM_COUNTRY_LOCATOR).send_keys(country)
        self.driver.find_element(*self.ORDER_FORM_CITY_LOCATOR).send_keys(city)
        self.driver.find_element(*self.ORDER_FORM_CARD_NUMBER_LOCATOR).send_keys(card_number)
        self.driver.find_element(*self.ORDER_FORM_CARD_MONTH_LOCATOR).send_keys(card_expiration_month)
        self.driver.find_element(*self.ORDER_FORM_CARD_YEAR_LOCATOR).send_keys(card_expiration_year)

    def get_success_message(self):
        self.wait_for_element_to_be_present(self.ORDER_ALERT_MESSAGE_LOCATOR)
        return self.driver.find_element(*self.ORDER_ALERT_DETAILS_LOCATOR).text

    def submit_purchase_message(self):
        sleep(2)
        self.driver.find_element(*self.ORDER_ALERT_SUBMIT_LOCATOR).click()
