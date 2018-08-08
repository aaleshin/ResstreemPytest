import telnetlib
from hamcrest import *
import pytest
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import requests


class TestServerFunctionality:
    def setup_class(self):
        self.host = 'restream.sloppy.zone'
        self.command = 'rest/product/search'
        self.url = 'http://{}/{}'.format(self.host, self.command)


    @pytest.fixture(scope="function")
    def get_all(self):
        response_all = requests.get(self.url)
        return response_all.json()['data']


    def test_getall(self):
        response = requests.get(self.url)
        assert_that(response.status_code, equal_to(200))


    def test_response(self):
        response = requests.get(self.url, params={'q': 'apple'})
        assert_that(response.status_code, equal_to(200))
        items = response.json()['data']
        for item in items:
            assert_that(item['name'].lower(), contains_string('apple'))

    # почему не проходит тест?
    # def test_discription(self):
    #     response = requests.get(self.url, params={'q': 'a'})
    #     assert_that(response.status_code, equal_to(200))
    #     items = response.json()['data']
    #     for item in items:
    #         assert_that(item['description'].lower() or item['name'].lower(), contains_string('a'))


    def test_many_word(self):
        response = requests.get(self.url, params={'q': 'aapplettestsignedapplettestsignedapplettestsignedapplettestsignedapplettestsignedapplettestsignedapplettestsignedapplettestsignedapplettestsignedapplettestsignedapplettestsignedapplettestsignedapplettestsignedapplettestsignedapplettestsignedapplettestsigned'})
        assert_that(response.status_code, equal_to(200))
        items = response.json()['data']
        assert_that(items, equal_to([]))
        assert_that(len(items), equal_to(0))


    def test_big_lette(self):
        response = requests.get(self.url, params={'q': 'OWASP'})
        assert_that(response.status_code, equal_to(200))
        items = response.json()['data']
        for item in items:
            assert_that(item['name'], contains_string('OWASP'))


    def test_numbers(self, get_all):
        response = requests.get(self.url, params={'q': '12345'})
        assert_that(response.status_code, equal_to(200))
        items = response.json()['data']
        assert_that(items, equal_to([]))
        assert_that(len(items), equal_to(0))


    def test_empty(self, get_all):
        response = requests.get(self.url, params={'q': ''})
        assert_that(response.status_code, equal_to(200))
        items_empty_test = response.json()['data']
        assert_that(items_empty_test, get_all)


    def test_gap(self, get_all):
        response = requests.get(self.url, params={'q': ' '})
        assert_that(response.status_code, equal_to(200))
        items = response.json()['data']
        assert_that(items, get_all)


    def test_word_with_gap(self):
        response = requests.get(self.url, params={'q': 'OWA SP"'})
        assert_that(response.status_code, equal_to(200))
        items = response.json()['data']
        assert_that(len(items), equal_to(0))


    def test_null(self, get_all):
        response = requests.get(self.url, params={'q': None})
        assert_that(response.status_code, equal_to(200))
        items = response.json()['data']
        assert_that(items, get_all)


    def test_symbol(self):
        response = requests.get(self.url, params={'q': '«»‘~!@#$%^&*()?>,./\<][ /*<!—«»♣☺♂'})
        assert_that(response.status_code, equal_to(200))
        items = response.json()['data']
        assert_that(len(items), equal_to(0))


    def test_sql(self):
        response = requests.get(self.url, params={'q': 'select*'})
        assert_that(response.status_code, equal_to(200))
        items = response.json()['data']
        assert_that(len(items), equal_to(0))


    def test_xss(self):
        response = requests.get(self.url, params={'q': '<script>alert("XSS1")</script>'})
        assert_that(response.status_code, equal_to(200))
        items = response.json()['data']
        assert_that(len(items), equal_to(0))


    def test_injections(self):
        response = requests.get(self.url, params={'q': 'DROP TABLE user;'})
        assert_that(response.status_code, equal_to(200))
        items = response.json()['data']
        assert_that(len(items), equal_to(0))


    def test_html_injections(self):
        response = requests.get(self.url, params={'q': '< form % 20 action =»http: // live.hh.ru» > < input % 20 type =»submit» > < / form >'})
        assert_that(response.status_code, equal_to(200))
        items = response.json()['data']
        assert_that(len(items), equal_to(0))


    def test_inverted_commas(self):
        """it's bug"""
        response = requests.get(self.url, params={'q': ' \'OWASP\' '})
        assert_that(response.status_code, equal_to(500))




@pytest.fixture(scope="session")
def driver_init(request):
    web_driver = webdriver.Chrome("D:\\downloads\\avtotests\\chromedriver.exe")
    request.cls.driver = web_driver
    yield
    web_driver.close()


@pytest.mark.usefixtures("driver_init")
class CheckUI:
    def test_check_goods_count(self, driver):
        wait = WebDriverWait(self.driver, 3)
        driver.get('https://restream.sloppy.zone/#/search')
        wait.until(telnetlib.EC.visibility_of_element_located((By.CSS_SELECTOR, "input[value='Find Flights']"))).click()
