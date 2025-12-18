"""Basic Auth page object"""
from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class BasicAuthPage(BasePage):
    # Locators
    BODY_TEXT = (By.TAG_NAME, "body")
    
    def __init__(self, driver, username, password):
        super().__init__(driver)
        self.username = username
        self.password = password
    
    def navigate_with_auth(self):
        """Navigate to basic auth page with credentials in URL"""
        url = f"https://{self.username}:{self.password}@the-internet.herokuapp.com/basic_auth"
        self.driver.get(url)
    
    def get_page_text(self):
        """Get all text from page body"""
        return self.get_text(self.BODY_TEXT).lower()