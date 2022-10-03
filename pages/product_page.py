from selenium.webdriver.common.by import By

from pages.base import Base


class ProductPage(Base):

    """ Product page class """

    PRODUCT_TITLE_LOCATOR = (By.CSS_SELECTOR, "h2.name")
    ADD_TO_CART_BTN_LOCATOR = (By.CSS_SELECTOR, ".btn-success")

    def __init__(self, driver):
        super().__init__(driver)

    def wait_for_product_page_to_open(self, product_title):
        self.wait_for_text_to_be_preset(self.PRODUCT_TITLE_LOCATOR, product_title)

    def add_to_cart(self):
        self.driver.find_element(*self.ADD_TO_CART_BTN_LOCATOR).click()
