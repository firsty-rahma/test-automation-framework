"""Base page class that all page objects inherit from"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from config import Config

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.TIMEOUT)
    
    def click_element(self, locator):
        """Wait for element and click it"""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
        return element
    
    def enter_text(self, locator, text):
        """Wait for element and enter text"""
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)
        return element
    
    def get_text(self, locator):
        """Wait for element and get its text - FIXED"""
        element = self.wait.until(EC.visibility_of_element_located(locator))
        return element.text
    
    def get_element(self, locator):
        """Wait for element and return it"""
        return self.wait.until(EC.presence_of_element_located(locator))
    
    def is_element_visible(self, locator, timeout=None):
        """Check if element is visible"""
        try:
            wait_time = timeout if timeout else Config.TIMEOUT
            wait = WebDriverWait(self.driver, wait_time)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def scroll_to_element(self, locator):
        """Scroll element into view"""
        element = self.wait.until(EC.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        return element
    
    def js_click(self, locator):
        """Click element using JavaScript"""
        element = self.wait.until(EC.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].click();", element)
        return element