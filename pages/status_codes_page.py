from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class StatusCodesPage(BasePage):
    # Locators
    STATUS_TEXT = (By.TAG_NAME, "p")
    
    def __init__(self, driver, base_url):
        super().__init__(driver)
        self.base_url = base_url
    
    def navigate_to_status_code(self, code):
        """Navigate to specific status code page"""
        self.driver.get(f"{self.base_url}/status_codes/{code}")
    
    def get_status_text(self):
        """Get the status code text from page"""
        element = self.wait.until(EC.presence_of_element_located(self.STATUS_TEXT))
        return element.text