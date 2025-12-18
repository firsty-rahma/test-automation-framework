from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from pages.base_page import BasePage

class ContextMenuPage(BasePage):
    # Locators
    HOT_SPOT = (By.ID, "hot-spot")
    
    def right_click_hot_spot(self):
        """Right-click on the hot spot element"""
        hot_spot = self.wait.until(EC.presence_of_element_located(self.HOT_SPOT))
        action = ActionChains(self.driver)
        action.context_click(hot_spot).perform()
    
    def get_alert_text(self):
        """Get alert text and return it"""
        alert = self.wait.until(EC.alert_is_present())
        return alert.text
    
    def accept_alert(self):
        """Accept the alert"""
        alert = self.wait.until(EC.alert_is_present())
        alert.accept()