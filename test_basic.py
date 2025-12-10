# test_basic.py
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from config import Config
import os
import tempfile
import time

def test_add_remove_elements(driver, base_url):
    """Test adding and removing elements dynamically"""
    driver.get(base_url)
    
    # Navigate to feature
    link = driver.find_element(By.LINK_TEXT, "Add/Remove Elements")
    link.click()
    
    # Add element
    wait = WebDriverWait(driver, Config.TIMEOUT)
    add_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Add Element']")))
    add_button.click()
    
    # Verify element added
    delete_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "added-manually")))
    assert delete_button.is_displayed(), "Delete button should be visible after adding element"
    
    # Remove element
    delete_button.click()
    
    # Verify element removed
    wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "added-manually")))

def test_basic_auth_success(driver):
    """Test successful basic authentication"""
    url = f"https://{Config.USERNAME}:{Config.PASSWORD}@the-internet.herokuapp.com/basic_auth"
    driver.get(url)
    
    page_text = driver.find_element(By.TAG_NAME, "body").text.lower()
    assert "congratulations" in page_text, "Should see success message after authentication"

def test_dropdown_selection(driver, base_url):
    """Test dropdown menu selection"""
    driver.get(base_url)
    
    # Navigate to dropdown
    link = driver.find_element(By.LINK_TEXT, "Dropdown")
    link.click()
    
    # Select options
    wait = WebDriverWait(driver, Config.TIMEOUT)
    select_element = Select(wait.until(EC.presence_of_element_located((By.ID, "dropdown"))))
    
    # Test Option 1
    select_element.select_by_visible_text("Option 1")
    assert select_element.first_selected_option.text == "Option 1", "Option 1 should be selected"
    
    # Test Option 2
    select_element.select_by_visible_text("Option 2")
    assert select_element.first_selected_option.text == "Option 2", "Option 2 should be selected"

def test_context_menu(driver, base_url):
    """Test right-click context menu"""
    driver.get(base_url)
    
    # Navigate to context menu
    link = driver.find_element(By.LINK_TEXT, "Context Menu")
    link.click()
    
    # Right-click on hot spot
    wait = WebDriverWait(driver, Config.TIMEOUT)
    hot_spot = wait.until(EC.presence_of_element_located((By.ID, "hot-spot")))
    
    action = ActionChains(driver)
    action.context_click(hot_spot).perform()
    
    # Handle alert
    alert = wait.until(EC.alert_is_present())
    assert "You selected a context menu" in alert.text, "Alert should mention context menu"
    alert.accept()

def test_file_download(driver, base_url):
    """Test file download functionality"""
    # Create temporary download directory
    download_dir = tempfile.mkdtemp()
    
    # Configure Chrome to download to specific folder
    chrome_options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    # Create new driver with download preferences
    download_driver = webdriver.Chrome(options=chrome_options)
    download_driver.implicitly_wait(Config.TIMEOUT)
    
    try:
        # Navigate to file download page
        download_driver.get(f"{base_url}/download")
        
        # Wait for page to fully load
        wait = WebDriverWait(download_driver, Config.TIMEOUT)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".example")))
        
        # Wait for download links to be visible and clickable
        download_links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".example a")))
        assert len(download_links) > 0, "Should have download links available"
        
        # Try to find a small text file (easier to download quickly)
        # Look for .txt or .pdf files first
        target_link = None
        for link in download_links:
            link_text = link.text.lower()
            if link_text.endswith('.txt') or link_text.endswith('.pdf'):
                target_link = link
                break
        
        # If no txt/pdf found, use first link
        if target_link is None:
            target_link = download_links[0]
        
        file_name = target_link.text
        print(f"Attempting to download: {file_name}")
        
        # Scroll to element to ensure it's in viewport
        download_driver.execute_script("arguments[0].scrollIntoView(true);", target_link)
        time.sleep(0.5)
        
        # Click using JavaScript
        download_driver.execute_script("arguments[0].click();", target_link)
        
        # Wait for file to download completely (check for non-.crdownload files)
        def is_download_complete(directory):
            files = os.listdir(directory)
            # Filter out Chrome's temporary download files
            completed_files = [f for f in files if not f.endswith('.crdownload') and not f.endswith('.tmp')]
            return len(completed_files) > 0
        
        # Wait up to 20 seconds for download to complete
        download_complete = False
        for i in range(20):
            if is_download_complete(download_dir):
                download_complete = True
                break
            time.sleep(1)
            if i % 3 == 0:  # Print progress every 3 seconds
                print(f"Waiting for download... ({i}s)")
        
        assert download_complete, "Download did not complete within 20 seconds"
        
        # Get the completed file
        files = [f for f in os.listdir(download_dir) if not f.endswith('.crdownload') and not f.endswith('.tmp')]
        assert len(files) > 0, "No files were downloaded"
        
        downloaded_file = os.path.join(download_dir, files[0])
        
        # Wait a bit more to ensure file writing is complete
        time.sleep(1)
        
        # Verify file is not empty
        file_size = os.path.getsize(downloaded_file)
        assert file_size > 0, f"Downloaded file is empty (size: {file_size} bytes)"
        
        print(f"✅ Successfully downloaded: {files[0]} ({file_size} bytes)")
        
    finally:
        # Cleanup
        download_driver.quit()
        
        # Remove downloaded files
        try:
            for file in os.listdir(download_dir):
                file_path = os.path.join(download_dir, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            os.rmdir(download_dir)
        except Exception as e:
            print(f"Cleanup warning: {e}")

def test_file_upload(driver, base_url):
    """Test file upload functionality"""
    driver.get(base_url)
    
    # Navigate to file upload
    link = driver.find_element(By.LINK_TEXT, "File Upload")
    link.click()
    
    # Create test file
    file_name = "test_upload.txt"
    file_path = os.path.join(os.getcwd(), file_name)
    
    # Create file
    with open(file_path, 'w') as f:
        f.write("Test content for file upload")
    
    try:
        # Upload file
        upload_button = driver.find_element(By.ID, 'file-upload')
        submit_button = driver.find_element(By.ID, 'file-submit')
        
        upload_button.send_keys(file_path)
        submit_button.click()
        
        # Verify upload
        wait = WebDriverWait(driver, Config.TIMEOUT)
        uploaded_file = wait.until(EC.presence_of_element_located((By.ID, 'uploaded-files'))).text
        assert uploaded_file == file_name, f"Expected {file_name}, but got {uploaded_file}"
        
    finally:
        # Cleanup
        if os.path.exists(file_path):
            os.remove(file_path)

def test_status_code_200(driver, base_url):
    """Test 200 OK status code page"""
    driver.get(f"{base_url}/status_codes/200")
    
    wait = WebDriverWait(driver, Config.TIMEOUT)
    page_text = wait.until(EC.presence_of_element_located((By.TAG_NAME, "p"))).text
    
    assert "200" in page_text, "Page should display status code 200"

def test_status_code_404(driver, base_url):
    """Test 404 Not Found status code page"""
    driver.get(f"{base_url}/status_codes/404")
    
    wait = WebDriverWait(driver, Config.TIMEOUT)
    page_text = wait.until(EC.presence_of_element_located((By.TAG_NAME, "p"))).text
    
    assert "404" in page_text, "Page should display status code 404"

def test_status_code_500(driver, base_url):
    """Test 500 Server Error status code page"""
    driver.get(f"{base_url}/status_codes/500")
    
    wait = WebDriverWait(driver, Config.TIMEOUT)
    page_text = wait.until(EC.presence_of_element_located((By.TAG_NAME, "p"))).text
    
    assert "500" in page_text, "Page should display status code 500"

def test_checkboxes(driver, base_url):
    """Test checkbox interactions"""
    driver.get(base_url)
    
    # Navigate to Checkboxes
    link = driver.find_element(By.LINK_TEXT, "Checkboxes")
    link.click()
    
    wait = WebDriverWait(driver, Config.TIMEOUT)
    
    # Find ALL checkboxes (note: find_elements, plural!)
    checkboxes = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[type='checkbox']")))
    
    assert len(checkboxes) == 2, "Should have 2 checkboxes"
    
    # Test checkbox 1 (initially unchecked)
    checkbox1 = checkboxes[0]
    initial_state_1 = checkbox1.is_selected()
    
    # Click checkbox 1
    checkbox1.click()
    assert checkbox1.is_selected() != initial_state_1, "Checkbox 1 state should change after click"
    
    # Test checkbox 2 (initially checked)
    checkbox2 = checkboxes[1]
    initial_state_2 = checkbox2.is_selected()
    
    # Click checkbox 2
    checkbox2.click()
    assert checkbox2.is_selected() != initial_state_2, "Checkbox 2 state should change after click"
    
    print("✅ Both checkboxes tested successfully")

def test_switch_windows(driver, base_url):
    """Test switching between multiple windows"""
    driver.get(base_url)
    
    # Navigate to Multiple Windows
    wait = WebDriverWait(driver, Config.TIMEOUT)
    link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Multiple Windows")))
    link.click()
    
    # Store the main window handle
    main_window_handle = driver.current_window_handle
    print(f"Main window handle: {main_window_handle}")
    
    # Wait for page to load and verify we're on the right page
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "h3")))
    heading = driver.find_element(By.TAG_NAME, "h3").text
    assert "Multiple Windows" in heading, f"Should be on Multiple Windows page, but heading is: {heading}"
    
    # Click the "Click Here" link to open new window
    click_here_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Click Here")))
    click_here_link.click()
    
    # Wait for new window to open
    wait.until(lambda d: len(d.window_handles) > 1)
    
    # Get all window handles
    all_handles = driver.window_handles
    assert len(all_handles) == 2, "Should have 2 windows open"
    
    # Switch to the new window
    for handle in all_handles:
        if handle != main_window_handle:
            driver.switch_to.window(handle)
            break
    
    # Verify we're in the new window
    wait.until(EC.title_is("New Window"))
    assert driver.title == "New Window", "Should be in new window"
    
    # Wait for content to load
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "h3")))
    assert "New Window" in driver.page_source, "Should see 'New Window' text"
    
    # Close the new window
    driver.close()
    
    # Switch back to the main window
    driver.switch_to.window(main_window_handle)
    
    # Verify we're back in the main window
    assert "The Internet" in driver.title, "Should be back in main window"
    
    print("✅ Window switching works correctly")