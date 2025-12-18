"""Add/Remove Elements page object"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class AddRemovePage(BasePage):
    # Locators
    ADD_BUTTON = (By.XPATH, "//button[text()='Add Element']")
    DELETE_BUTTON = (By.CLASS_NAME, "added-manually")

    def click_add_element(self):
        """Click the Add Element button"""
        self.click_element(self.ADD_BUTTON)
    
    def click_delete_element(self):
        """Click the Add Element button"""
        self.click_element(self.DELETE_BUTTON)
    
    def is_delete_button_visible(self):
        """Check if delete button is visible"""
        return self.is_element_visible(self.DELETE_BUTTON)
    
    def is_delete_button_removed(self):
        """Check if delete button has been removed"""
        try:
            self.wait.until(EC.invisibility_of_element_located(self.DELETE_BUTTON))
            return True
        except:
            return False
    