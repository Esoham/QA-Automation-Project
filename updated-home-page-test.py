import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.home_page import HomePage

@pytest.fixture
def driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    yield driver
    driver.quit()

def test_homepage_search(driver):
    home_page = HomePage(driver)
    home_page.navigate()
    
    assert home_page.is_search_visible(), "Search bar is not visible on the homepage"
    
    home_page.search_product("Organic Apples")
    # Add assertions to check search results

def test_featured_products(driver):
    home_page = HomePage(driver)
    home_page.navigate()
    
    featured_products = home_page.get_featured_products()
    assert len(featured_products) > 0, "No featured products found on the homepage"
