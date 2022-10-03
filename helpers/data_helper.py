import json

from selenium.common import TimeoutException


def get_test_data():
    with open('./test_data/data.json', 'r') as f:
        file = json.load(f)
    return file


def screenshot_decorator(func):
    def wrapper_func(self, *args):
        try:
            func(self, *args)
        except TimeoutException as e:
            self.driver.save_screenshot("screenshot_wait_error.png")
            raise e
    return wrapper_func
