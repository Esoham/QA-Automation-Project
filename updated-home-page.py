from .base_page import BasePage
from selenium.webdriver.common.by import By
from utils.config_reader import ConfigReader

class HomePage(BasePage):
    # Locators
    SEARCH_INPUT = (By.ID, "search-input")
    SEARCH_BUTTON = (By.ID, "search-button")
    FEATURED_PRODUCTS = (By.CLASS_NAME, "featured-product")

    def __init__(self, driver):
        super().__init__(driver)
        config = ConfigReader()
        self.url = config.get_base_url()

    # ... rest of the methods remain the same
