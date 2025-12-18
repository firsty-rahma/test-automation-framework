from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class KeyPressesPage(BasePage):
    # Locators
    INPUT_FIELD = (By.ID, "target")
    RESULT_TEXT = (By.ID, "result")
    
    def wait_for_input_field(self):
        """Wait for input field to be visible"""
        return self.wait.until(EC.visibility_of_element_located(self.INPUT_FIELD))
    
    def press_key(self, key):
        """Send key press to input field"""
        input_field = self.wait_for_input_field()
        input_field.send_keys(key)
    
    def get_result_text(self):
        """Get the result text showing which key was pressed"""
        result = self.driver.find_element(*self.RESULT_TEXT)
        return result.text