from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class CheckboxesPage(BasePage):
    CHECKBOXES = (By.CSS_SELECTOR, "input[type='checkbox']")

    def get_all_checkboxes(self):
        """Get all checkbox elements"""
        return self.wait.until(EC.presence_of_all_elements_located(self.CHECKBOXES))
    
    def click_checkbox(self, index):
        """Click checkbox at specific index"""
        checkboxes = self.get_all_checkboxes()
        checkboxes[index].click()
    
    def is_checkbox_selected(self, index):
        """Check if checkbox at index is selected"""
        checkboxes = self.get_all_checkboxes()
        return checkboxes[index].is_selected()
    
    def get_checkbox_count(self):
        """Get total number of checkboxes"""
        return len(self.get_all_checkboxes())
    