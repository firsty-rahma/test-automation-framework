from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
import time, random

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
    
    def find_a_file(self):
        """Find a random file link, return None if not found"""
        links = self.get_all_download_links()
        link_list = [link.text.lower() for link in links]
        return random.choice(link_list) if link_list else self.get_first_download_link()
        
    def get_first_download_link(self):
        """Get the first download link"""
        links = self.get_all_download_links()
        return links[0] if links else None
    
    def click_download_link(self, link_element):
        """Click a download link"""
        DOWNLOAD_LINK = (By.LINK_TEXT, link_element)
        
        # Wait for element to be clickable (ensures page has settled)
        self.wait.until(EC.element_to_be_clickable(DOWNLOAD_LINK))

        # Click using JavaScript
        self.click_element(DOWNLOAD_LINK)
    
    def get_link_text(self, link_element):
        """Get text from link element"""
        print(link_element)
        return link_element