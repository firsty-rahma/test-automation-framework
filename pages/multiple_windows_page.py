from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class MultipleWindowsPage(BasePage):
    # Locators
    HEADING = (By.TAG_NAME)
    CLICK_HERE_LINK = (By.LINK_TEXT, "Click Here")

    def get_heading_text(self):
        """Get page heading text"""
        return self.get_text(self.HEADING)
    
    def click_here(self):
        """Click the 'Click Here' link to open new window"""
        self.click_element(self.CLICK_HERE_LINK)

    def wait_for_new_window(self, original_handles):
        """Wait for new window to open"""
        self.wait.until(lambda d: len(d.window_handles) > len(original_handles))

    def switch_to_new_window(self, original_handle):
        """Switch to the newly opened window"""
        for handle in self.driver.window_handles:
            if handle != original_handle:
                self.driver.switch_to.window(handle)
                break
            
    def switch_to_window(self, handle):
        """Switch to specific window handle"""
        self.driver.switch_to.window(handle)
    
    def close_current_window(self):
        """Close the current window"""
        self.driver.close()
    
    def get_current_window_handle(self):
        """Get current window handle"""
        return self.driver.current_window_handle
    
    def get_all_window_handles(self):
        """Get all window handles"""
        return self.driver.window_handles
    
    def get_page_title(self):
        """Get current page title"""
        return self.driver.title
    
    def wait_for_title(self, title):
        """Wait for page title to match"""
        self.wait.until(EC.title_is(title))