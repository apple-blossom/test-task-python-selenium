import requests
import json

from .data_helper import *


class ApiHelper:

    def register_user(self, url, username, encoded_password):
        return requests.post(url, json={"username": username, "password": encoded_password})

    def log_in(self, url, username, encoded_password):
        return requests.post(url, json={"username": username, "password": encoded_password})

    def get_log_in_token(self, url, username, password):
        response = self.log_in(url, username, password)
        if response.status_code == 200:
            return response.content.decode("utf-8").replace("Auth_token: ", "").replace('"', "").replace('\r', '')\
                .replace('\n', '')
        else:
            raise AssertionError(f"Wrong status code: {response.status_code}")

    def get_cart_items(self, url, auth_cookie):
        response = requests.post(url, json={"cookie": auth_cookie, "flag": True})
        if response.status_code == 200:
            return json.loads(response.content.decode("utf-8"))
        else:
            raise AssertionError(f"Wrong status code: {response.status_code}")

    def get_product_details(self, url, product_id):
        response = requests.post(url, json={"id": product_id})
        return json.loads(response.content.decode("utf-8"))
