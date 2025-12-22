"""Home page object - main landing page"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class HomePage(BasePage):
    # Locators
    ADD_REMOVE_LINK = (By.LINK_TEXT, "Add/Remove Elements")
    DROPDOWN_LINK = (By.LINK_TEXT, "Dropdown")
    CONTEXT_MENU_LINK = (By.LINK_TEXT, "Context Menu")
    FILE_DOWNLOAD_LINK = (By.LINK_TEXT, "Context Menu")
    FILE_UPLOAD_LINK = (By.LINK_TEXT, "File Upload")
    CHECKBOXES_LINK = (By.LINK_TEXT, "Checkboxes")
    KEY_PRESSES_LINK = (By.LINK_TEXT, "Key Presses")
    MULTIPLE_WINDOWS_LINK = (By.LINK_TEXT, "Multiple Windows")

    def __init__(self, driver, base_url):
        super().__init__(driver)
        self.base_url = base_url
    
    def navigate(self):
        """Navigate to home page"""
        self.driver.get(self.base_url)
    
    def go_to_add_remove_elements(self):
        """Navigate to Add/Remove Elements page"""
        self.click_element(self.ADD_REMOVE_LINK)
    
    def go_to_dropdown(self):
        """Navigate to Dropdown page"""
        self.click_element(self.DROPDOWN_LINK)

    def go_to_context_menu(self):
        """Navigate to Context Menu page"""
        self.click_element(self.CONTEXT_MENU_LINK)
    
    def go_to_file_download(self):
        """Navigate to File Download page"""
        self.click_element(self.FILE_DOWNLOAD_LINK)
    
    def go_to_file_upload(self):
        """Navigate to File Upload page"""
        self.click_element(self.FILE_UPLOAD_LINK)
    
    def go_to_checkboxes(self):
        """Navigate to Checkboxes page"""
        self.click_element(self.CHECKBOXES_LINK)
    
    def go_to_key_pressess(self):
        """Navigate to File Download page"""
        self.click_element(self.KEY_PRESSES_LINK)
    
    def go_to_multiple_windows(self):
        """Navigate to File Upload page"""
        self.click_element(self.MULTIPLE_WINDOWS_LINK)
    

    

