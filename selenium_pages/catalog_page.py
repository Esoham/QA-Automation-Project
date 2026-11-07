"""Selenium page object: browser actions live here; business assertions stay in tests."""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


class CatalogPage:
    SEARCH = (By.ID, "search")
    CATEGORY = (By.ID, "category")
    SUBMIT = (By.CSS_SELECTOR, "#search-form button[type=submit]")
    PRODUCTS = (By.CSS_SELECTOR, "#results article")
    STATUS = (By.ID, "status")
    QUOTE_STATUS = (By.ID, "quote-status")

    def __init__(self, driver, base_url: str):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, timeout=10)

    def open(self):
        self.driver.get(self.base_url + "/")
        self.wait.until(EC.text_to_be_present_in_element(self.STATUS, "products found"))
        return self

    def search(self, text: str, category: str = ""):
        entry = self.wait.until(EC.element_to_be_clickable(self.SEARCH))
        entry.clear()
        entry.send_keys(text)
        Select(self.driver.find_element(*self.CATEGORY)).select_by_visible_text(
            category if category else "All categories"
        )
        self.driver.find_element(*self.SUBMIT).click()
        return self

    def wait_for_count(self, expected: int):
        self.wait.until(lambda driver: (
            len(driver.find_elements(*self.PRODUCTS)) == expected
            and driver.find_element(*self.STATUS).text == f"{expected} products found"
        ))
        return self

    def product_count(self):
        return len(self.driver.find_elements(*self.PRODUCTS))

    def status(self):
        return self.driver.find_element(*self.STATUS).text

    def quote(self, sku: str):
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//button[normalize-space(.)='Quote {sku}']")
        )).click()
        return self

    def quote_message_containing(self, expected: str):
        self.wait.until(EC.text_to_be_present_in_element(self.QUOTE_STATUS, expected))
        return self.driver.find_element(*self.QUOTE_STATUS).text
