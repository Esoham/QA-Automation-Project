from .base_page import BasePage
from selenium.webdriver.common.by import By

class HomePage(BasePage):
    # Locators
    SEARCH_INPUT = (By.ID, "search-input")
    SEARCH_BUTTON = (By.ID, "search-button")
    FEATURED_PRODUCTS = (By.CLASS_NAME, "featured-product")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://example-greengrocer-site.com"  # Replace with actual URL when available

    def navigate(self):
        self.driver.get(self.url)

    def search_product(self, product_name):
        self.input_text(self.SEARCH_INPUT, product_name)
        self.click(self.SEARCH_BUTTON)

    def get_featured_products(self):
        return self.driver.find_elements(*self.FEATURED_PRODUCTS)

    def is_search_visible(self):
        return self.is_element_visible(self.SEARCH_INPUT)
