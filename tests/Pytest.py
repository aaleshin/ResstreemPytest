from telnetlib import EC
from hamcrest import *
import pytest
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import requests
import json
from random import choice


class TestServerFunctionality():
    def setup(self):
        self.host = 'restream.sloppy.zone'
        self.command = 'rest/product/search'
        self.url = 'http://{}/{}'.format(self.host, self.command)


    def test_getall(self):
        response = requests.get(self.url)
        assert_that(response.status_code, equal_to(200))


    def test_many_word(self):
        response = requests.get(self.url, params={'q': 'aapplettestsignedapplettestsignedapplettestsignedapplettestsignedapplettestsignedapplettestsignedapplettestsignedapplettestsignedapplettestsignedapplettestsignedapplettestsignedapplettestsignedapplettestsignedapplettestsignedapplettestsignedapplettestsigned'})
        assert_that(response.status_code, equal_to(200))
        items = response.json()['data']
        for item in items:
            assert_that(item['name'].lower(), contains_string('apple'))
            print(items)


    def test_example(self):
        response = requests.get(self.url, params={'q': 'apple'})
        assert_that(response.status_code, equal_to(200))
        items = response.json()['data']
        for item in items:
            assert_that(item['name'].lower(), contains_string('apple'))



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

