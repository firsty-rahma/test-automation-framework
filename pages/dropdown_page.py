from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class DropdownPage(BasePage):
    # Locators
    DROPDOWN = (By.ID, "dropdown")
    
    def get_dropdown_element(self):
        """Get the Select element for dropdown"""
        element = self.wait.until(EC.presence_of_element_located(self.DROPDOWN))
        return Select(element)
    
    def select_option_by_text(self, text):
        """Select dropdown option by visible text"""
        dropdown = self.get_dropdown_element()
        dropdown.select_by_visible_text(text)
    
    def get_selected_option_text(self):
        """Get currently selected option text"""
        dropdown = self.get_dropdown_element()
        return dropdown.first_selected_option.text