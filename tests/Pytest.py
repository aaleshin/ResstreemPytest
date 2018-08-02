from telnetlib import EC
from hamcrest import *
import pytest
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import requests
import unittest
import json
from random import choice


class TestServerFunctionality(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(TestServerFunctionality, self).__init__(*a, **kw)
        self.host = 'restream.sloppy.zone'
        self.command = 'rest/product/search'
        self.url = 'http://{}/{}'.format(self.host, self.command)

    def test_example(self):
        response = requests.get(self.url, params={'q': 'apple'})

        assert_that(response.status_code, equal_to(200))

        items = response.json()['data']

        for item in items:
            assert_that(item['name'].lower(), contains_string('apple'))


if __name__ == '__main__':
    unittest.main(verbosity=2)

#
# DEFAULT_HEADER = 'application/json'
#
# SUCCESS = 200


# class TestServerFunctionality(unittest.TestCase):
#
    # def __init__(self, *a, **kw):
    #     super(TestServerFunctionality, self).__init__(*a, **kw)
#         self.host = 'restream.sloppy.zone/rest'
#         self.command = '/product/search'
#         self.url = 'https://{}/{}'.format(self.host, self.command)
#
#     def test_get_product(self):
#         status_code, text = self._get_request()
#         self.assertEqual(status_code, SUCCESS)
#         print(text)
#
#     def _get_request(self, identificator=None):
#         _url = self.url
#         if identificator:
#             _url = "{}/{}".format(self.url, identificator)
#         _response = requests.get(_url)
#         return _response.status_code, _response.json()
#

# if __name__ == '__main__':
#     unittest.main(verbosity=2)
#
# ------------------------------------------------------

# class CMClient:
#     def __init__(self, config):
#         self.username = config['username']
#         self.password = config['password']
#
#     def get(self, endpoint):
#         return self.request('get', endpoint)
#
#     def post(self, json, endpoint):
#         return self.request('post', endpoint, json=json.__dict__)
#
#     def put(self, json, endpoint):
#         return self.request('put', endpoint, json=json.__dict__)
#
#     def delete(self, endpoint):
#         return self.request('delete', endpoint)
#
#     def request(self, method, endpoint, params=None, json=None, files=None, data=None):
#         url = 'http://{}:{}/{}'.format(endpoint)
#         response = requests.request(
#             method,
#             url,
#             files=files,
#             data=data,
#             params=params,
#             json=json
#         )
#         print(response.url, response.status_code, response.text)
#
#         return response
#
#     def auth_request(self):
#         url = 'http://{}:{}/login'.format
#         data = {
#             'email': self.username,
#             'password': self.password,
#         }
#         response = requests.request('post', url, data=data)
#         print(response.url, response.status_code, response.text)
#
#         return response



# @pytest.fixture(scope="session")
# def driver_init(request):
#     web_driver = webdriver.Chrome("D:\\downloads\\avtotests\\chromedriver.exe")
#     request.cls.driver = web_driver
#     yield
#     web_driver.close()
#
# @pytest.mark.usefixtures("driver_init")
# class CheckUI():
#     def test_check_goods_count(self, driver):
#         wait = WebDriverWait(self.driver, 3)
#         driver.get('https://restream.sloppy.zone/#/search')
#         wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[value='Find Flights']"))).click()

