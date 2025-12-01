# test_basic.py
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from config import Config
import os

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

def test_file_upload(driver, base_url):
    """Test file upload functionality"""
    driver.get(base_url)
    
    # Navigate to file upload
    link = driver.find_element(By.LINK_TEXT, "File Upload")
    link.click()
    
    # Create test file
    file_name = "test_upload.txt"
    file_path = os.path.join(os.getcwd(), file_name)
    
    # Create file if doesn't exist
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            f.write("Test content")
    
    # Upload file
    upload_button = driver.find_element(By.ID, 'file-upload')
    submit_button = driver.find_element(By.ID, 'file-submit')
    
    upload_button.send_keys(file_path)
    submit_button.click()
    
    # Verify upload
    wait = WebDriverWait(driver, Config.TIMEOUT)
    uploaded_file = wait.until(EC.presence_of_element_located((By.ID, 'uploaded-files'))).text
    assert uploaded_file == file_name, f"Expected {file_name}, but got {uploaded_file}"
    
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

def test_key_presses(driver, base_url):
    driver.get(base_url)
    
    # Navigate to Key Presses
    link = driver.find_element(By.LINK_TEXT, "Key Presses")
    link.click()

    wait = WebDriverWait(driver, Config.TIMEOUT)
    key_textbox = wait.until(EC.visibility_of_element_located((By.ID, "target")))
    
    key_textbox.send_keys(Keys.SPACE)
    assert driver.find_element(By.ID, "result").text == "You entered: SPACE"
    key_textbox.send_keys("L")
    assert driver.find_element(By.ID, "result").text == "You entered: L"
    key_textbox.send_keys("a")
    assert driver.find_element(By.ID, "result").text == "You entered: A"
    key_textbox.send_keys("8")
    assert driver.find_element(By.ID, "result").text == "You entered: 8"
    key_textbox.send_keys(Keys.SHIFT)
    assert driver.find_element(By.ID, "result").text == "You entered: SHIFT"
    key_textbox.send_keys("&")
    assert driver.find_element(By.ID, "result").text == "You entered: 7"
    key_textbox.send_keys("?")
    assert driver.find_element(By.ID, "result").text == "You entered: SLASH"
    key_textbox.send_keys(Keys.BACK_SPACE)
    assert driver.find_element(By.ID, "result").text == "You entered: BACK_SPACE"


