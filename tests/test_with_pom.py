# test_complete_pom.py
"""Complete test suite using Page Object Model"""
import pytest
import os
import tempfile
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from config import Config
from selenium.webdriver.common.by import By
from pages.home_page import HomePage
from pages.add_remove_page import AddRemovePage
from pages.dropdown_page import DropdownPage
from pages.checkboxes_page import CheckboxesPage
from pages.multiple_windows_page import MultipleWindowsPage
from pages.context_menu_page import ContextMenuPage
from pages.file_download_page import FileDownloadPage
from pages.file_upload_page import FileUploadPage
from pages.status_codes_page import StatusCodesPage
from pages.key_presses_page import KeyPressesPage
from pages.basic_auth_page import BasicAuthPage


class TestAddRemoveElements:
    """Test suite for Add/Remove Elements functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, base_url):
        self.home_page = HomePage(driver, base_url)
        self.add_remove_page = AddRemovePage(driver)
        self.home_page.navigate()
        self.home_page.go_to_add_remove_elements()
    
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_add_and_remove_element(self):
        """Test adding and removing an element"""
        # Add element
        self.add_remove_page.click_add_element()
        assert self.add_remove_page.is_delete_button_visible(), \
            "Delete button should be visible after adding"
        
        # Remove element
        self.add_remove_page.click_delete_element()
        assert self.add_remove_page.is_delete_button_removed(), \
            "Delete button should be removed"


class TestBasicAuth:
    """Test suite for Basic Authentication"""
    
    @pytest.mark.smoke
    def test_basic_auth_success(self, driver):
        """Test successful basic authentication"""
        auth_page = BasicAuthPage(driver, Config.USERNAME, Config.PASSWORD)
        auth_page.navigate_with_auth()
        
        page_text = auth_page.get_page_text()
        assert "congratulations" in page_text, \
            "Should see success message after authentication"


class TestDropdown:
    """Test suite for Dropdown functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, base_url):
        self.home_page = HomePage(driver, base_url)
        self.dropdown_page = DropdownPage(driver)
        self.home_page.navigate()
        self.home_page.go_to_dropdown()
    
    @pytest.mark.regression
    @pytest.mark.ui
    def test_select_option_1(self):
        """Test selecting Option 1"""
        self.dropdown_page.select_option_by_text("Option 1")
        assert self.dropdown_page.get_selected_option_text() == "Option 1"
    
    @pytest.mark.regression
    @pytest.mark.ui
    def test_select_option_2(self):
        """Test selecting Option 2"""
        self.dropdown_page.select_option_by_text("Option 2")
        assert self.dropdown_page.get_selected_option_text() == "Option 2"


class TestContextMenu:
    """Test suite for Context Menu functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, base_url):
        self.home_page = HomePage(driver, base_url)
        self.context_page = ContextMenuPage(driver)
        self.home_page.navigate()
        self.home_page.go_to_context_menu()
    
    @pytest.mark.ui
    def test_right_click_context_menu(self):
        """Test right-click context menu"""
        # Right-click on hot spot
        self.context_page.right_click_hot_spot()
        
        # Verify alert text
        alert_text = self.context_page.get_alert_text()
        assert "You selected a context menu" in alert_text
        
        # Accept alert
        self.context_page.accept_alert()


class TestFileDownload:
    """Test suite for File Download functionality"""
    
    @pytest.mark.download
    @pytest.mark.slow
    @pytest.mark.skipif(
        os.getenv('CI') == 'true',
        reason="File downloads are unreliable in CI/CD headless Chrome environment"
    )
    def test_file_download(self, base_url):
        """Test file download functionality"""
        download_dir = tempfile.mkdtemp()
        
        # Configure Chrome with download preferences AND headless mode
        chrome_options = webdriver.ChromeOptions()
        
        # Download preferences
        prefs = {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
            "profile.default_content_settings.popups": 0,
            "download.manager.showDownloadStarted": False,  # Don't show download started
            "browser.download.folderList": 2,  # Custom location
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        # Headless mode for CI/CD compatibility - IMPORTANT for downloads
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # CRITICAL: Enable downloads in headless mode
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        
        download_driver = webdriver.Chrome(options=chrome_options)
        
        # CRITICAL: Enable downloads in headless Chrome
        download_driver.execute_cdp_cmd("Page.setDownloadBehavior", {
            "behavior": "allow",
            "downloadPath": download_dir
        })
        
        download_driver.implicitly_wait(Config.TIMEOUT)
        
        try:
            # Navigate to download page
            download_page = FileDownloadPage(download_driver)
            download_driver.get(f"{base_url}/download")
            download_page.wait_for_page_load()
            
            # Find a text or PDF file
            target_link = download_page.find_text_or_pdf_file()
            if target_link is None:
                target_link = download_page.get_first_download_link()
            
            file_name = download_page.get_link_text(target_link)
            print(f"Attempting to download: {file_name}")
            
            # Get initial file list
            initial_files = set(os.listdir(download_dir))
            
            # Click download link
            download_page.click_download_link(target_link)
            print("Download link clicked, waiting for file...")
            
            # Wait for download to complete - improved logic with longer timeout
            def wait_for_download_complete(directory, initial_files, timeout=60):
                """Wait for a new file to appear and be fully downloaded"""
                end_time = time.time() + timeout
                
                while time.time() < end_time:
                    current_files = set(os.listdir(directory))
                    new_files = current_files - initial_files
                    
                    # Filter out temporary files
                    completed_files = [f for f in new_files 
                                     if not f.endswith('.crdownload') 
                                     and not f.endswith('.tmp')
                                     and not f.endswith('.part')]
                    
                    if completed_files:
                        # Found a completed file, wait a bit more to ensure it's fully written
                        time.sleep(3)  # Increased wait time
                        file_path = os.path.join(directory, completed_files[0])
                        
                        # Verify file has content
                        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                            return file_path, completed_files[0]
                    
                    time.sleep(1)
                    
                    # Debug: print current files
                    if int(time.time() - end_time + timeout) % 10 == 0:
                        print(f"Current files in directory: {os.listdir(directory)}")
                
                return None, None
            
            downloaded_file_path, downloaded_filename = wait_for_download_complete(
                download_dir, initial_files, timeout=60
            )
            
            assert downloaded_file_path is not None, \
                f"Download did not complete within 60 seconds. Files in directory: {os.listdir(download_dir)}"
            
            # Verify file size
            file_size = os.path.getsize(downloaded_file_path)
            assert file_size > 0, f"Downloaded file is empty (size: {file_size} bytes)"
            
            print(f"✅ Successfully downloaded: {downloaded_filename} ({file_size} bytes)")
            
        finally:
            download_driver.quit()
            # Cleanup
            try:
                for file in os.listdir(download_dir):
                    file_path = os.path.join(download_dir, file)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                os.rmdir(download_dir)
            except Exception as e:
                print(f"Cleanup warning: {e}")
        
        try:
            # Navigate to download page
            download_page = FileDownloadPage(download_driver)
            download_driver.get(f"{base_url}/download")
            download_page.wait_for_page_load()
            
            # Find a text or PDF file
            target_link = download_page.find_text_or_pdf_file()
            if target_link is None:
                target_link = download_page.get_first_download_link()
            
            file_name = download_page.get_link_text(target_link)
            print(f"Attempting to download: {file_name}")
            
            # Get initial file list
            initial_files = set(os.listdir(download_dir))
            
            # Click download link
            download_page.click_download_link(target_link)
            print("Download link clicked, waiting for file...")
            
            # Wait for download to complete - improved logic
            def wait_for_download_complete(directory, initial_files, timeout=30):
                """Wait for a new file to appear and be fully downloaded"""
                end_time = time.time() + timeout
                
                while time.time() < end_time:
                    current_files = set(os.listdir(directory))
                    new_files = current_files - initial_files
                    
                    # Filter out temporary files
                    completed_files = [f for f in new_files 
                                     if not f.endswith('.crdownload') 
                                     and not f.endswith('.tmp')
                                     and not f.endswith('.part')]
                    
                    if completed_files:
                        # Found a completed file, wait a bit more to ensure it's fully written
                        time.sleep(2)
                        file_path = os.path.join(directory, completed_files[0])
                        
                        # Verify file has content
                        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                            return file_path, completed_files[0]
                    
                    time.sleep(0.5)
                
                return None, None
            
            downloaded_file_path, downloaded_filename = wait_for_download_complete(
                download_dir, initial_files, timeout=30
            )
            
            assert downloaded_file_path is not None, \
                "Download did not complete within 30 seconds or file is empty"
            
            # Verify file size
            file_size = os.path.getsize(downloaded_file_path)
            assert file_size > 0, f"Downloaded file is empty (size: {file_size} bytes)"
            
            print(f"✅ Successfully downloaded: {downloaded_filename} ({file_size} bytes)")
            
        finally:
            download_driver.quit()
            # Cleanup
            try:
                for file in os.listdir(download_dir):
                    file_path = os.path.join(download_dir, file)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                os.rmdir(download_dir)
            except Exception as e:
                print(f"Cleanup warning: {e}")


class TestFileUpload:
    """Test suite for File Upload functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, base_url):
        self.home_page = HomePage(driver, base_url)
        self.upload_page = FileUploadPage(driver)
        self.home_page.navigate()
        self.home_page.go_to_file_upload()
    
    @pytest.mark.upload
    def test_file_upload(self):
        """Test file upload functionality"""
        file_name = "test_upload.txt"
        file_path = os.path.join(os.getcwd(), file_name)
        
        # Create test file
        with open(file_path, 'w') as f:
            f.write("Test content for file upload")
        
        try:
            # Upload file
            self.upload_page.upload_file(file_path)
            self.upload_page.click_submit()
            
            # Verify upload
            uploaded_file = self.upload_page.get_uploaded_filename()
            assert uploaded_file == file_name, \
                f"Expected {file_name}, but got {uploaded_file}"
            
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)


class TestStatusCodes:
    """Test suite for Status Codes functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, base_url):
        self.status_page = StatusCodesPage(driver, base_url)
    
    def test_status_code_200(self):
        """Test 200 OK status code page"""
        self.status_page.navigate_to_status_code(200)
        page_text = self.status_page.get_status_text()
        assert "200" in page_text, "Page should display status code 200"
    
    def test_status_code_404(self):
        """Test 404 Not Found status code page"""
        self.status_page.navigate_to_status_code(404)
        page_text = self.status_page.get_status_text()
        assert "404" in page_text, "Page should display status code 404"
    
    def test_status_code_500(self):
        """Test 500 Server Error status code page"""
        self.status_page.navigate_to_status_code(500)
        page_text = self.status_page.get_status_text()
        assert "500" in page_text, "Page should display status code 500"


class TestCheckboxes:
    """Test suite for Checkboxes functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, base_url):
        self.home_page = HomePage(driver, base_url)
        self.checkboxes_page = CheckboxesPage(driver)
        self.home_page.navigate()
        self.home_page.go_to_checkboxes()
    
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_checkboxes_toggle(self):
        """Test checkbox interactions"""
        assert self.checkboxes_page.get_checkbox_count() == 2
        
        # Test checkbox 1
        initial_state_1 = self.checkboxes_page.is_checkbox_selected(0)
        self.checkboxes_page.click_checkbox(0)
        assert self.checkboxes_page.is_checkbox_selected(0) != initial_state_1
        
        # Test checkbox 2
        initial_state_2 = self.checkboxes_page.is_checkbox_selected(1)
        self.checkboxes_page.click_checkbox(1)
        assert self.checkboxes_page.is_checkbox_selected(1) != initial_state_2
        
        print("✅ Both checkboxes tested successfully")


class TestKeyPresses:
    """Test suite for Key Presses functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, base_url):
        self.home_page = HomePage(driver, base_url)
        self.key_page = KeyPressesPage(driver)
        self.home_page.navigate()
        self.home_page.go_to_key_presses()
    
    @pytest.mark.ui
    def test_key_presses(self):
        """Test keyboard input detection"""
        test_cases = [
            (Keys.SPACE, "You entered: SPACE"),
            ("L", "You entered: L"),
            ("a", "You entered: A"),
            ("8", "You entered: 8"),
            (Keys.SHIFT, "You entered: SHIFT"),
            (Keys.BACK_SPACE, "You entered: BACK_SPACE"),
        ]
        
        for key, expected_result in test_cases:
            self.key_page.press_key(key)
            actual_result = self.key_page.get_result_text()
            assert actual_result == expected_result, \
                f"Expected '{expected_result}', got '{actual_result}'"
        
        print("✅ All key presses detected correctly")


class TestMultipleWindows:
    """Test suite for Multiple Windows functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, base_url):
        self.home_page = HomePage(driver, base_url)
        self.windows_page = MultipleWindowsPage(driver)
        self.home_page.navigate()
        self.home_page.go_to_multiple_windows()
    
    @pytest.mark.windows
    def test_switch_windows(self):
        """Test switching between multiple windows"""
        # Verify page
        heading = self.windows_page.get_heading_text()
        assert "Opening a new window" in heading
        
        # Get main window
        main_handle = self.windows_page.get_current_window_handle()
        
        # Open new window
        self.windows_page.click_here()
        self.windows_page.wait_for_new_window([main_handle])
        
        # Verify 2 windows
        all_handles = self.windows_page.get_all_window_handles()
        assert len(all_handles) == 2
        
        # Switch to new window
        self.windows_page.switch_to_new_window(main_handle)
        self.windows_page.wait_for_title("New Window")
        assert self.windows_page.get_page_title() == "New Window"
        
        # Close and return
        self.windows_page.close_current_window()
        self.windows_page.switch_to_window(main_handle)
        assert "The Internet" in self.windows_page.get_page_title()
        
        print("✅ Window switching works correctly")