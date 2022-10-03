from time import sleep

import pytest
import requests
from assertpy import assert_that

from helpers.data_generation_helper import *
from helpers.data_helper import *
from helpers.api_helper import ApiHelper
from pages.base import Base
from pages.main_page import MainPage
from pages.sign_up_login_page import SignUpLogInPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage

test_data = get_test_data()


class TestClass:

    def setup(self):
        self.driver = Base.setup_with_headless()
        self.main_page = MainPage(self.driver)
        self.sign_up_login_page = SignUpLogInPage(self.driver)
        self.product_page = ProductPage(self.driver)
        self.cart_page = CartPage(self.driver)
        self.api = ApiHelper()
        self.url = test_data["baseUrl"]
        self.api_url = test_data["apiUrl"]
        self.driver.get(self.url)
        self.main_page.wait_for_main_page_to_load()
        self.user_name = generate_user_data(12)
        self.password = generate_user_data(8)
        self.encoded_password = encode_password(self.password)

    def teardown(self):
        self.driver.quit()

    def test_product_catalog_create_user_verify_created(self):
        """Creating a user and verifying created user can successfully log in"""

        self.main_page.open_sign_in_menu()
        self.sign_up_login_page.wait_for_sign_up_form_to_load()
        self.sign_up_login_page.fill_sign_up_form(self.user_name, self.password)
        self.sign_up_login_page.press_sign_up()
        self.sign_up_login_page.wait_for_alert()
        text = self.sign_up_login_page.get_alert_text_and_close()
        assert text == test_data["signUpSuccess"]

        self.main_page.open_log_in_menu()
        self.sign_up_login_page.wait_for_log_in_form_to_load()
        self.sign_up_login_page.fill_in_log_in_form(self.user_name, self.password)
        self.sign_up_login_page.press_log_in()
        actual_user_name = self.main_page.get_welcome_title()
        assert self.user_name in actual_user_name

    def test_product_catalog_add_items_to_cart(self):
        """Log in with existing user, adding items to cart"""

        resp = self.api.register_user(self.api_url + test_data["signUpUrl"], self.user_name, self.encoded_password)
        assert resp.status_code == 200

        cookie = self.api.get_log_in_token(self.api_url + test_data["logInUrl"], self.user_name, self.encoded_password)
        self.main_page.add_auth_cookie(test_data["authCookieKey"], cookie)
        self.driver.refresh()

        self.main_page.wait_for_welcome_title()

        self.add_product_to_cart(test_data["catalogItems"][0], test_data["itemsAddToCart"][0],
                                 test_data["productAddedMessage"])
        self.add_product_to_cart(test_data["catalogItems"][1], test_data["itemsAddToCart"][1],
                                 test_data["productAddedMessage"])

        self.main_page.open_cart()
        self.cart_page.wait_for_cart_items_to_load()
        cart_items = self.cart_page.get_cart_product_titles()
        assert len(cart_items) == len(test_data["itemsAddToCart"])

        counted_total_price = self.cart_page.get_cart_product_sum()
        actual_total_price = self.cart_page.get_total_price()

        assert_that(sorted(cart_items)).is_equal_to(sorted(test_data["itemsAddToCart"]))
        assert counted_total_price == actual_total_price

        self.cart_page.press_order_button()
        self.cart_page.wait_for_purchase_form_to_load()
        self.cart_page.fill_purchase_form(test_data["customerName"], test_data["customerCountry"],
                                          test_data["customerCity"], test_data["customerCardNumber"],
                                          test_data["customerCardExpirationMonth"],
                                          test_data["customerCardExpirationYear"])
        self.cart_page.press_purchase_button()
        purchase_message = self.cart_page.get_success_message()

        assert f"Amount: {counted_total_price} USD" in purchase_message

        self.cart_page.submit_purchase_message()
        self.main_page.wait_for_main_page_to_load()
        self.main_page.open_cart()
        self.cart_page.wait_for_cart_to_load()
        cart_items = self.cart_page.get_cart_product_titles()
        assert len(cart_items) == 0

    def test_get_items_from_cart_with_api(self):
        """Add item to cart, verify items with API"""
        resp = self.api.register_user(self.api_url + test_data["signUpUrl"], self.user_name, self.encoded_password)
        assert resp.status_code == 200
        product_to_buy = test_data["itemsAddToCart"][0]
        print(product_to_buy)

        cookie = self.api.get_log_in_token(self.api_url + test_data["logInUrl"], self.user_name, self.encoded_password)
        self.main_page.add_auth_cookie(test_data["authCookieKey"], cookie)
        self.driver.refresh()

        self.main_page.wait_for_welcome_title()
        self.add_product_to_cart(test_data["catalogItems"][0], product_to_buy,
                                 test_data["productAddedMessage"])
        self.main_page.open_cart()
        self.cart_page.wait_for_cart_items_to_load()
        cart_items = self.cart_page.get_cart_product_titles()
        cart_item_prices = self.cart_page.get_cart_items_price()
        items = self.api.get_cart_items(self.api_url + test_data["cartItemsUrl"], cookie)
        assert len(items["Items"]) == len(cart_items) == 1

        item_id = items["Items"][0]["prod_id"]
        item_info = self.api.get_product_details(self.api_url + test_data["cartItemDetailsUrl"], item_id)

        assert item_info["title"] == product_to_buy
        assert item_info["id"] == test_data["testProductId"]
        assert item_info["price"] == cart_item_prices[0] == test_data["testProductPrice"]

    def add_product_to_cart(self, category, product, message):
        self.main_page.open_category_tab(category, product)
        self.main_page.open_catalog_product(product)
        self.product_page.wait_for_product_page_to_open(product)
        self.product_page.add_to_cart()
        self.sign_up_login_page.wait_for_alert()
        text = self.sign_up_login_page.get_alert_text_and_close()
        assert text == message

        self.main_page.click_header_logo()
        self.main_page.wait_for_main_page_to_load()
