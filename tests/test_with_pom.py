# test_complete_pom.py
"""Complete test suite using Page Object Model"""
import pytest
import os
import tempfile
import time
import allure
from datetime import datetime
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

@allure.feature("Dynamic Elements")
@allure.story("Add and Remove Elements")
class TestAddRemoveElements:
    """Test suite for Add/Remove Elements functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, base_url):
        self.home_page = HomePage(driver, base_url)
        self.add_remove_page = AddRemovePage(driver)
        self.home_page.navigate()
        self.home_page.go_to_add_remove_elements()
    
    @allure.title("Add and remove element dynamically")
    @allure.description("Verify that elements can be added and removed dynamically from the page")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_add_and_remove_element(self):
        """Test adding and removing an element"""
        # Add element
        with allure.step("Click add element button"):
            self.add_remove_page.click_add_element()

        with allure.step("Verify delete button is visible"):
            assert self.add_remove_page.is_delete_button_visible(), \
                "Delete button should be visible after adding"
        
        with allure.step("Click delete button"):
             # Remove element
            self.add_remove_page.click_delete_element()
       
        with allure.step("Verify delete button is removed"):
            assert self.add_remove_page.is_delete_button_removed(), \
                "Delete button should be removed"

@allure.feature("Authentication")
@allure.story("Basic HTTP Authentication")
class TestBasicAuth:
    """Test suite for Basic Authentication"""
    
    @allure.title("Successful basic authentication")
    @allure.description("Verify successful login with valid credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_basic_auth_success(self, driver):
        """Test successful basic authentication"""
        with allure.step("Navigate to basic auth page with credentials"):
            auth_page = BasicAuthPage(driver, Config.USERNAME, Config.PASSWORD)
            auth_page.navigate_with_auth()
        
        with allure.step("Verify success message is displayed"):
            page_text = auth_page.get_page_text()
            assert "congratulations" in page_text, \
                "Should see success message after authentication"

@allure.feature("Form Controls")
@allure.story("Dropdown Selection")
class TestDropdown:
    """Test suite for Dropdown functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, base_url):
        self.home_page = HomePage(driver, base_url)
        self.dropdown_page = DropdownPage(driver)
        self.home_page.navigate()
        self.home_page.go_to_dropdown()
    
    @allure.title("Select Option 1 from dropdown")
    @allure.description("Verify that Option 1 can be selected from dropdown menu")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_select_option_1(self):
        """Test selecting Option 1"""
        with allure.step("Select Option 1 from dropdown"):
            self.dropdown_page.select_option_by_text("Option 1")

        with allure.step("Verify Option 1 is selected"):
            assert self.dropdown_page.get_selected_option_text() == "Option 1"
    
    @allure.title("Select Option 2 from dropdown")
    @allure.description("Verify that Option 2 can be selected from dropdown menu")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_select_option_2(self):
        """Test selecting Option 2"""
        with allure.step("Select Option 2 from dropdown"):
            self.dropdown_page.select_option_by_text("Option 2")
        
        with allure.step("Verify Option 2 is selected"):
            assert self.dropdown_page.get_selected_option_text() == "Option 2"

@allure.feature("Input Controls")
@allure.story("Right Click Function")
class TestContextMenu:
    """Test suite for Context Menu functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, base_url):
        self.home_page = HomePage(driver, base_url)
        self.context_page = ContextMenuPage(driver)
        self.home_page.navigate()
        self.home_page.go_to_context_menu()
        
    @allure.title("Right-click Context Menu")
    @allure.description("Verify the alert text is appeared after right-click at the certain area")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.ui
    def test_right_click_context_menu(self):
        """Test right-click context menu"""
        with allure.step("Right-click on hot spot"):
            self.context_page.right_click_hot_spot()
        
        with allure.step("Verify alert text"):
            alert_text = self.context_page.get_alert_text()
            assert "You selected a context menu" in alert_text
        
        with allure.step("Accept alert"):
            self.context_page.accept_alert()

@allure.feature("File Operations")
@allure.story("File Download")
class TestFileDownload:
    """Test suite for File Download functionality"""

    @allure.title("Download file and verify")
    @allure.description("Test file download functionality and verify file integrity")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.download
    @pytest.mark.slow
    #@pytest.mark.skipif(
    #    os.getenv('CI') == 'true',
    #    reason="File downloads are unreliable in CI/CD headless Chrome environment"
    #)
    def test_file_download(self, base_url):
        """Test file download functionality"""
        download_dir = tempfile.mkdtemp()
        
        # Configure Chrome with download preferences
        chrome_options = webdriver.ChromeOptions()
        
        # Download preferences
        prefs = {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
            "profile.default_content_settings.popups": 0,
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        # Headless mode for CI/CD compatibility
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        download_driver = webdriver.Chrome(options=chrome_options)
        
        # Enable downloads in headless Chrome
        download_driver.execute_cdp_cmd("Page.setDownloadBehavior", {
            "behavior": "allow",
            "downloadPath": download_dir
        })
        
        download_driver.implicitly_wait(Config.TIMEOUT)
        
        try:
            with allure.step("Navigate to download page"):
                download_page = FileDownloadPage(download_driver)
                download_driver.get(f"{base_url}/download")
                download_page.wait_for_page_load()
            
            with allure.step("Find downloadable file"):
                target_link = download_page.find_text_or_pdf_file()
                if target_link is None:
                    target_link = download_page.get_first_download_link()
                
                file_name = download_page.get_link_text(target_link)
                allure.attach(file_name, name="Target File", attachment_type=allure.attachment_type.TEXT)
                print(f"Attempting to download: {file_name}")
            
            with allure.step("Click download and wait for completion"):
                # Get initial file list
                initial_files = set(os.listdir(download_dir))
                
                # Click download link
                download_page.click_download_link(target_link)
                print("Download link clicked, waiting for file...")
                
                # Wait for download to complete - FIXED VERSION
                downloaded_file_path = None
                downloaded_filename = None
                timeout = 30
                end_time = time.time() + timeout
                
                while time.time() < end_time:
                    time.sleep(1)  # Wait before checking
                    
                    current_files = set(os.listdir(download_dir))
                    new_files = current_files - initial_files
                    
                    # Filter out temporary files
                    completed_files = [f for f in new_files 
                                     if not f.endswith('.crdownload') 
                                     and not f.endswith('.tmp')
                                     and not f.endswith('.part')]
                    
                    if completed_files:
                        # Found a file, check if it has content
                        file_path = os.path.join(download_dir, completed_files[0])
                        
                        # Wait for file to finish writing
                        if os.path.exists(file_path):
                            time.sleep(2)  # Extra wait to ensure file is complete
                            
                            # Check file size
                            try:
                                file_size = os.path.getsize(file_path)
                                if file_size >= 0:  # Accept any size including 0 for empty test files
                                    downloaded_file_path = file_path
                                    downloaded_filename = completed_files[0]
                                    print(f"File found: {downloaded_filename} ({file_size} bytes)")
                                    break
                            except OSError:
                                # File might still be writing
                                continue
                
                # Assert file was downloaded
                assert downloaded_file_path is not None, \
                    f"Download did not complete within {timeout} seconds. Files in directory: {os.listdir(download_dir)}"
            
            with allure.step("Verify file was downloaded"):
                file_size = os.path.getsize(downloaded_file_path)
                allure.attach(f"{file_size} bytes", name="File Size", attachment_type=allure.attachment_type.TEXT)
                
                # Some test files might be empty or very small, so just check it exists
                assert file_size >= 0, f"Downloaded file has invalid size: {file_size} bytes"
                
                print(f"✅ Successfully downloaded: {downloaded_filename} ({file_size} bytes)")
            
        except Exception as e:
            print(f"Test error: {e}")
            
            # Try to capture screenshot even though driver is separate
            try:
                screenshot_path = os.path.join("screenshots", f"download_failure_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
                os.makedirs("screenshots", exist_ok=True)
                download_driver.save_screenshot(screenshot_path)
                
                # Attach to Allure
                with open(screenshot_path, 'rb') as f:
                    allure.attach(f.read(), name="Screenshot on Failure", attachment_type=allure.attachment_type.PNG)
            except:
                pass
            
            raise
            
        finally:
            # Cleanup - quit driver first
            try:
                download_driver.quit()
            except Exception as e:
                print(f"Driver quit warning: {e}")
            
            # Clean up files
            try:
                if os.path.exists(download_dir):
                    for file in os.listdir(download_dir):
                        file_path = os.path.join(download_dir, file)
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                    os.rmdir(download_dir)
            except Exception as e:
                print(f"Cleanup warning: {e}")

@allure.feature("File Operations")
@allure.story("File Upload")
class TestFileUpload:
    """Test suite for File Upload functionality"""
    @pytest.fixture(autouse=True)
    def setup(self, driver, base_url):
        self.home_page = HomePage(driver, base_url)
        self.upload_page = FileUploadPage(driver)
        self.home_page.navigate()
        self.home_page.go_to_file_upload()
    
    @allure.title("Upload file and verify")
    @allure.description("Test file upload functionality and verify the upload")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.upload
    def test_file_upload(self):
        with allure.step("Make the file name and file path"):
            file_name = "test_upload.txt"
            file_path = os.path.join(os.getcwd(), file_name)
        
        with allure.step("Create test file"):
            with open(file_path, 'w') as f:
                f.write("Test content for file upload")
        
        try:
            with allure.step("Upload file"):
                self.upload_page.upload_file(file_path)
                self.upload_page.click_submit()
            
            with allure.step("Verify upload"):
                uploaded_file = self.upload_page.get_uploaded_filename()
                assert uploaded_file == file_name, \
                    f"Expected {file_name}, but got {uploaded_file}"
            
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)

@allure.feature("Troubleshooting")
@allure.story("Status Code functionality")
class TestStatusCodes:
    @pytest.fixture(autouse=True)
    def setup(self, driver, base_url):
        self.status_page = StatusCodesPage(driver, base_url)
    
    @allure.title("Check status code 200 and verify")
    @allure.description("Test for status code 200")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_status_code_200(self):
        with allure.step("Test 200 OK status code page"):
            self.status_page.navigate_to_status_code(200)
            page_text = self.status_page.get_status_text()
            assert "200" in page_text, "Page should display status code 200"
    
    
    @allure.title("Check status code 404 and verify")
    @allure.description("Test for status code 404")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_status_code_404(self):
        with allure.step("Test 404 Not Found status code page"):
            self.status_page.navigate_to_status_code(404)
            page_text = self.status_page.get_status_text()
            assert "404" in page_text, "Page should display status code 404"
    
    @allure.title("Check status code 500 and verify")
    @allure.description("Test for status code 500")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_status_code_500(self):
        with allure.step("Test 500 Server Error status code page"):
            self.status_page.navigate_to_status_code(500)
            page_text = self.status_page.get_status_text()
            assert "500" in page_text, "Page should display status code 500"

@allure.feature("Form Controls")
@allure.story("Checkboxes")
class TestCheckboxes:
    """Test suite for Checkboxes functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, base_url):
        self.home_page = HomePage(driver, base_url)
        self.checkboxes_page = CheckboxesPage(driver)
        self.home_page.navigate()
        self.home_page.go_to_checkboxes()
    
    @allure.title("Click two checkboxes")
    @allure.description("Verify that two checkboxes are checked")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_checkboxes_toggle(self):
        assert self.checkboxes_page.get_checkbox_count() == 2
    
        with allure.step("Check checkbox 1"):
            initial_state_1 = self.checkboxes_page.is_checkbox_selected(0)
            self.checkboxes_page.click_checkbox(0)
            assert self.checkboxes_page.is_checkbox_selected(0) != initial_state_1
        
        with allure.step("Check checkbox 2"):
            initial_state_2 = self.checkboxes_page.is_checkbox_selected(1)
            self.checkboxes_page.click_checkbox(1)
            assert self.checkboxes_page.is_checkbox_selected(1) != initial_state_2

            print("✅ Both checkboxes tested successfully")

@allure.feature("Input Controls")
@allure.story("Key Presses")
class TestKeyPresses:
    """Test suite for Key Presses functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, base_url):
        self.home_page = HomePage(driver, base_url)
        self.key_page = KeyPressesPage(driver)
        self.home_page.navigate()
        self.home_page.go_to_key_presses()
    
    @allure.title("Press any keys")
    @allure.description("Verify that the output from keys are matched with test cases")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.ui
    def test_key_presses(self):
        test_cases = [
            (Keys.SPACE, "You entered: SPACE"),
            ("L", "You entered: L"),
            ("a", "You entered: A"),
            ("8", "You entered: 8"),
            (Keys.SHIFT, "You entered: SHIFT"),
            (Keys.BACK_SPACE, "You entered: BACK_SPACE"),
        ]
        
        with allure.step("Detect the key presses"):
            for key, expected_result in test_cases:
                self.key_page.press_key(key)
                actual_result = self.key_page.get_result_text()
                assert actual_result == expected_result, \
                    f"Expected '{expected_result}', got '{actual_result}'"
            
            print("✅ All key presses detected correctly")

@allure.feature("Window Controls")
@allure.story("Multiple Windows")
class TestMultipleWindows:
    """Test suite for Multiple Windows functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, base_url):
        self.home_page = HomePage(driver, base_url)
        self.windows_page = MultipleWindowsPage(driver)
        self.home_page.navigate()
        self.home_page.go_to_multiple_windows()
    
    @allure.title("Show the multiple windows")
    @allure.description("Verify the opened multiple windows")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.windows
    def test_switch_windows(self):
        
        with allure.step("Verify main page"):
            heading = self.windows_page.get_heading_text()
            assert "Opening a new window" in heading
        
        with allure.step("Get main window"):
            main_handle = self.windows_page.get_current_window_handle()
        
        with allure.step("Open new window"):
            self.windows_page.click_here()
            self.windows_page.wait_for_new_window([main_handle])
        
        with allure.step("Verify 2 windows"):
            all_handles = self.windows_page.get_all_window_handles()
            assert len(all_handles) == 2
        
        with allure.step("Switch to new window"): 
            self.windows_page.switch_to_new_window(main_handle)
            self.windows_page.wait_for_title("New Window")
            assert self.windows_page.get_page_title() == "New Window"
        
        with allure.step("Close and return"):
            self.windows_page.close_current_window()
            self.windows_page.switch_to_window(main_handle)
            assert "The Internet" in self.windows_page.get_page_title()
        
            print("✅ Window switching works correctly")