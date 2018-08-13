from hamcrest import *
import pytest
import selenium
import requests
from selenium.webdriver.common.by import By


class TestServerFunctionality:
    def setup_class(self):
        self.host = 'restream.sloppy.zone'
        self.command = 'rest/product/search'
        self.url = 'http://{}/{}'.format(self.host, self.command)


    @pytest.fixture(scope="function")
    def get_all(self):
        response_all = requests.get(self.url)
        all_item = response_all.json()['data']
        return all_item


    @pytest.yield_fixture(scope='session')
    def driver(self):
        driver = selenium.webdriver.Chrome("D:\\downloads\\avtotests\\chromedriver.exe")
        driver.implicitly_wait(10)
        driver.maximize_window()
        yield driver
        driver.quit()


    def test_getall(self):
        response = requests.get(self.url)
        assert_that(response.status_code, equal_to(200))


    def test_response(self):
        response = requests.get(self.url, params={'q': 'apple'})
        assert_that(response.status_code, equal_to(200))
        items = response.json()['data']
        assert_that(len(items), greater_than(0))
        for item in items:
            assert_that(item['name'].lower(), contains_string('apple'))


    def test_discription(self):
        response = requests.get(self.url, params={'q': 'a'})
        assert_that(response.status_code, equal_to(200))
        items = response.json()['data']
        for item in items:
            assert_that(
                (item['description'].lower(), contains_string('a')) or (item['name'].lower(), contains_string('a')))


    def test_many_word(self):
        response = requests.get(self.url, params={
            'q': 'aapplettestsignedapplettestsignedapplettestsignedapplettestsignedapplettestsignedapplettestsignedapplettestsignedapplettestsignedapplettestsignedapplettestsignedapplettestsignedapplettestsignedapplettestsignedapplettestsignedapplettestsignedapplettestsigned'})
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
        response = requests.get(self.url, params={
            'q': '< form % 20 action =»http: // live.hh.ru» > < input % 20 type =»submit» > < / form >'})
        assert_that(response.status_code, equal_to(200))
        items = response.json()['data']
        assert_that(len(items), equal_to(0))


    def test_inverted_commas(self):
        """it's bug"""
        response = requests.get(self.url, params={'q': ' \'OWASP\' '})
        assert_that(response.status_code, equal_to(200))
        items = response.json()['data']
        assert_that(len(items), equal_to(0))
        # assert_that(response.status_code, equal_to(500))


    def test_check_goods_count(self, driver):
        driver.get('https://restream.sloppy.zone/#/search')
        driver.find_element(By.CSS_SELECTOR, " div > ul > li> form > div > input").send_keys('OWASP')
        driver.find_element(By.ID, "searchButton").click()

        items = driver.find_elements(By.CSS_SELECTOR, '[data-ng-repeat="product in products"]')

        web_products = list()
        for item in items:
            row = item.find_elements(By.CSS_SELECTOR, '.ng-binding')
            name = row[0].get_attribute("innerHTML")
            description = row[1].get_attribute("innerHTML")
            price = row[2].get_attribute("innerHTML")
            product = {
                "name": name,
                "description": description,
                "price": float(price)
            }

            web_products.append(product)

        response = requests.get(self.url, params={'q': 'OWASP'})
        api_items = response.json()['data']

        filtered_items = list()
        for item in api_items:
            filtered_item = {key: item[key] for key in ['name', 'description', 'price']}
            filtered_items.append(filtered_item)

        for web, api in zip(web_products, filtered_items):
            assert_that(web, has_entries(api))

        assert_that(len(web_products), equal_to(len(filtered_items)))
