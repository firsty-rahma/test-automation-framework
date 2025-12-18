from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class FileUploadPage(BasePage):
    # Locators
    FILE_INPUT = (By.ID, "file-upload")
    SUBMIT_BUTTON = (By.ID, "file-submit")
    UPLOADED_FILES = (By.ID, "uploaded-files")
    
    def upload_file(self, file_path):
        """Select file for upload"""
        upload_input = self.driver.find_element(*self.FILE_INPUT)
        upload_input.send_keys(file_path)
    
    def click_submit(self):
        """Click the submit button"""
        submit_btn = self.driver.find_element(*self.SUBMIT_BUTTON)
        submit_btn.click()
    
    def get_uploaded_filename(self):
        """Get the uploaded filename"""
        return self.get_text(self.UPLOADED_FILES)