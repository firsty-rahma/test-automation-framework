from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
import time

class FileDownloadPage(BasePage):
    # Locators
    EXAMPLE_CONTAINER = (By.CSS_SELECTOR, ".example")
    DOWNLOAD_LINKS = (By.CSS_SELECTOR, ".example a")
    
    def wait_for_page_load(self):
        """Wait for download page to fully load"""
        self.wait.until(EC.presence_of_element_located(self.EXAMPLE_CONTAINER))
    
    def get_all_download_links(self):
        """Get all download link elements"""
        return self.wait.until(EC.presence_of_all_elements_located(self.DOWNLOAD_LINKS))
    
    def find_text_or_pdf_file(self):
        """Find a .txt or .pdf file link, return None if not found"""
        links = self.get_all_download_links()
        for link in links:
            link_text = link.text.lower()
            if link_text.endswith('.txt') or link_text.endswith('.pdf'):
                return link
        return None
    
    def get_first_download_link(self):
        """Get the first download link"""
        links = self.get_all_download_links()
        return links[0] if links else None
    
    def click_download_link(self, link_element):
        """Click a download link using JavaScript - Now, without arbitary waits"""
        # Scroll into view and wait for it to be stable
        self.driver.execute_script("arguments[0].scrollIntoView(true);", link_element)
        
        # Wait for element to be clickable (ensures page has settled)
        self.wait.until(EC.element_to_be_clickable(link_element))

        # Click using JavaScript
        self.driver.execute_script("arguments[0].click();", link_element)
    
    def get_link_text(self, link_element):
        """Get text from link element"""
        return link_element.text