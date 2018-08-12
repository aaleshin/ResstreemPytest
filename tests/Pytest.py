import hamcrest
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
        # a = 0
        # for count in all_item:
        #     if all_item.has['id']:
        #         a += 1
        # return all_item, a
        # print(all_item, a)


    def test_getall(self):
        response = requests.get(self.url)
        hamcrest.assert_that(response.status_code, hamcrest.equal_to(200))


    def test_response(self):
        response = requests.get(self.url, params={'q': 'apple'})
        hamcrest.assert_that(response.status_code, hamcrest.equal_to(200))
        items = response.json()['data']
        hamcrest.assert_that(len(items), hamcrest.greater_than(0))
        for item in items:
            hamcrest.assert_that(item['name'].lower(), hamcrest.contains_string('apple'))


    def test_discription(self):
        response = requests.get(self.url, params={'q': 'a'})
        hamcrest.assert_that(response.status_code, hamcrest.equal_to(200))
        items = response.json()['data']
        for item in items:
            hamcrest.assert_that((item['description'].lower(), hamcrest.contains_string('a')) or (item['name'].lower(), hamcrest.contains_string('a')))


    def test_many_word(self):
        response = requests.get(self.url, params={'q': 'aapplettestsignedapplettestsignedapplettestsignedapplettestsignedapplettestsignedapplettestsignedapplettestsignedapplettestsignedapplettestsignedapplettestsignedapplettestsignedapplettestsignedapplettestsignedapplettestsignedapplettestsignedapplettestsigned'})
        hamcrest.assert_that(response.status_code, hamcrest.equal_to(200))
        items = response.json()['data']
        hamcrest.assert_that(items, hamcrest.equal_to([]))
        hamcrest.assert_that(len(items), hamcrest.equal_to(0))


    def test_big_lette(self):
        response = requests.get(self.url, params={'q': 'OWASP'})
        hamcrest.assert_that(response.status_code, hamcrest.equal_to(200))
        items = response.json()['data']
        for item in items:
            hamcrest.assert_that(item['name'], hamcrest.contains_string('OWASP'))


    def test_numbers(self, get_all):
        response = requests.get(self.url, params={'q': '12345'})
        hamcrest.assert_that(response.status_code, hamcrest.equal_to(200))
        items = response.json()['data']
        hamcrest.assert_that(items, hamcrest.equal_to([]))
        hamcrest.assert_that(len(items), hamcrest.equal_to(0))


    def test_empty(self, get_all):
        response = requests.get(self.url, params={'q': ''})
        hamcrest.assert_that(response.status_code, hamcrest.equal_to(200))
        items_empty_test = response.json()['data']
        hamcrest.assert_that(items_empty_test, get_all)


    def test_gap(self, get_all):
        response = requests.get(self.url, params={'q': ' '})
        hamcrest.assert_that(response.status_code, hamcrest.equal_to(200))
        items = response.json()['data']
        hamcrest.assert_that(items, get_all)


    def test_word_with_gap(self):
        response = requests.get(self.url, params={'q': 'OWA SP"'})
        hamcrest.assert_that(response.status_code, hamcrest.equal_to(200))
        items = response.json()['data']
        hamcrest.assert_that(len(items), hamcrest.equal_to(0))


    def test_null(self, get_all):
        response = requests.get(self.url, params={'q': None})
        hamcrest.assert_that(response.status_code, hamcrest.equal_to(200))
        items = response.json()['data']
        hamcrest.assert_that(items, get_all)


    def test_symbol(self):
        response = requests.get(self.url, params={'q': '«»‘~!@#$%^&*()?>,./\<][ /*<!—«»♣☺♂'})
        hamcrest.assert_that(response.status_code, hamcrest.equal_to(200))
        items = response.json()['data']
        hamcrest.assert_that(len(items), hamcrest.equal_to(0))


    def test_sql(self):
        response = requests.get(self.url, params={'q': 'select*'})
        hamcrest.assert_that(response.status_code, hamcrest.equal_to(200))
        items = response.json()['data']
        hamcrest.assert_that(len(items), hamcrest.equal_to(0))


    def test_xss(self):
        response = requests.get(self.url, params={'q': '<script>alert("XSS1")</script>'})
        hamcrest.assert_that(response.status_code, hamcrest.equal_to(200))
        items = response.json()['data']
        hamcrest.assert_that(len(items), hamcrest.equal_to(0))


    def test_injections(self):
        response = requests.get(self.url, params={'q': 'DROP TABLE user;'})
        hamcrest.assert_that(response.status_code, hamcrest.equal_to(200))
        items = response.json()['data']
        hamcrest.assert_that(len(items), hamcrest.equal_to(0))


    def test_html_injections(self):
        response = requests.get(self.url, params={'q': '< form % 20 action =»http: // live.hh.ru» > < input % 20 type =»submit» > < / form >'})
        hamcrest.assert_that(response.status_code, hamcrest.equal_to(200))
        items = response.json()['data']
        hamcrest.assert_that(len(items), hamcrest.equal_to(0))


    def test_inverted_commas(self):
        """it's bug"""
        response = requests.get(self.url, params={'q': ' \'OWASP\' '})
        hamcrest.assert_that(response.status_code, hamcrest.equal_to(200))
        items = response.json()['data']
        hamcrest.assert_that(len(items), hamcrest.equal_to(0))
        # assert_that(response.status_code, equal_to(500))


    @pytest.yield_fixture(scope='session')
    def driver(self):
        driver = selenium.webdriver.Chrome("D:\\downloads\\avtotests\\chromedriver.exe")
        driver.implicitly_wait(10)
        driver.maximize_window()
        yield driver
        driver.quit()


    def test_check_goods_count(self, driver):
        driver.get('https://restream.sloppy.zone/#/search')
        driver.find_element(By.CSS_SELECTOR, " div > ul > li> form > div > input").send_keys('OWASP')
        driver.find_element(By.ID, "searchButton").click()

        # newitems = driver.find_element(By.CSS_SELECTOR, "body > div.container-fluid.ng-scope > div > div > table > tbody > tr > td:nth-child(2)").size
        # print(newitems)

        response = requests.get(self.url, params={'q': 'OWASP'})
        hamcrest.assert_that(response.status_code, hamcrest.equal_to(200))
        # all_date = response.json()['data']
        # print(all)
        name = response.json()['data']['name']
        description = response.json()['data']['description']
        price = response.json()['data']['price']

        rows = driver.find_elements(By.TAG_NAME, "tr")
        count = 0
        for row in rows:
            # Get the columns
            col_name = row.find_elements(By.TAG_NAME, "td")[2]  # This is the product Name column
            col_description = row.find_elements(By.TAG_NAME, "td")[3]  # This is the Description column
            col_price = row.find_elements(By.TAG_NAME, "td)")[4]  # This is the Price column

            hamcrest.assert_that(col_name.text, hamcrest.equal_to(name)) and (col_description.text, hamcrest.equal_to(description)) and (col_price.text, hamcrest.equal_to(price))
