import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.home_page import HomePage
from api.product_api import ProductAPI

@pytest.fixture(scope="module")
def driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    yield driver
    driver.quit()

@pytest.fixture(scope="module")
def api():
    return ProductAPI()

def test_search_integration(driver, api):
    # Use API to add a product
    new_product = {
        "name": "Organic Mangoes",
        "price": 2.99,
        "category": "Fruits"
    }
    response = api.create_product(new_product)
    assert response.status_code == 201
    product_id = response.json()["id"]

    # Use UI to search for the product
    home_page = HomePage(driver)
    home_page.navigate()
    home_page.search_product("Organic Mangoes")

    # Assert that the product is visible in search results
    # (You'll need to add a method to HomePage to check search results)
    assert home_page.is_product_in_search_results("Organic Mangoes")

    # Clean up: delete the product using API
    delete_response = api.delete_product(product_id)
    assert delete_response.status_code == 204
