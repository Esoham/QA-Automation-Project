"""Selenium 4 smoke tests of the local fictional catalog. One isolated driver per test."""
import os
import pytest

pytest.importorskip("selenium", reason="Install requirements-dev.txt to run Selenium tests")
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from selenium_pages.catalog_page import CatalogPage

pytestmark = pytest.mark.selenium


@pytest.fixture
def selenium_driver():
    options = Options()
    for flag in ("--headless=new", "--window-size=1280,900", "--disable-dev-shm-usage",
                 "--no-sandbox", "--disable-gpu"):
        options.add_argument(flag)
    chrome_path = os.environ.get("SELENIUM_CHROME_BINARY")
    if chrome_path:
        options.binary_location = chrome_path
    driver_path = os.environ.get("SELENIUM_DRIVER_PATH")
    service = Service(executable_path=driver_path) if driver_path else Service()
    driver = webdriver.Chrome(service=service, options=options)
    try:
        yield driver
    finally:
        driver.quit()


def test_selenium_search_parts_by_specification(selenium_driver, server_url):
    page = CatalogPage(selenium_driver, server_url).open()
    page.search("M6", "Fasteners").wait_for_count(3)
    assert page.status() == "3 products found"
    assert page.product_count() == 3


def test_selenium_valid_quote_has_correct_price(selenium_driver, server_url):
    page = CatalogPage(selenium_driver, server_url).open()
    message = page.quote("BOLT-M6").quote_message_containing("Quote for BOLT-M6: $0.35")
    assert message == "Quote for BOLT-M6: $0.35"


def test_selenium_out_of_stock_quote_explains_problem(selenium_driver, server_url):
    page = CatalogPage(selenium_driver, server_url).open()
    message = page.quote("GLOVE-N").quote_message_containing("Insufficient stock for GLOVE-N")
    assert message == "Quote unavailable: Insufficient stock for GLOVE-N"
