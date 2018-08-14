from hamcrest import *
import pytest
import selenium
import requests
from selenium.webdriver.common.by import By

mail = 'restream33@mailinator.com'
pasw = 'qwerty'


class TestClientFunctionality:
    def setup_class(self):
        self.host = 'restream.sloppy.zone'
        self.command = 'rest/product/search'
        self.url = 'http://{}/{}'.format(self.host, self.command)


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


    def test_check_good_cost(self, driver):
        driver.get('https://restream.sloppy.zone/#/search')
        driver.find_element(By.CSS_SELECTOR, "body > nav > div > ul > li:nth-child(1) > a").click()
        driver.find_element(By.ID, "userEmail").send_keys(mail)
        driver.find_element(By.ID, "userPassword").send_keys(pasw)
        driver.find_element(By.ID, "loginButton").click()

        items = driver.find_elements(By.CSS_SELECTOR, '[data-ng-repeat="product in products"]')
        web_products = list()
        for item in items:
            row = item.find_elements(By.CSS_SELECTOR, '.ng-binding')
            price = row[2]
            product = {
                "price": float(price)
            }

            web_products.append(product)

            print(web_products)