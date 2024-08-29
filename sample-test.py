from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def test_homepage_title():
    # Setup WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    try:
        # Navigate to the homepage
        driver.get("https://example-greengrocer-site.com")  # Replace with actual URL when available
        
        # Check the title
        assert "GreenGrocer" in driver.title, "Homepage title does not contain 'GreenGrocer'"
        
        # Additional checks can be added here
        
    finally:
        # Cleanup
        driver.quit()
