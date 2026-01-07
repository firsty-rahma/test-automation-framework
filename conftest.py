# conftest.py - WITH ALLURE INTEGRATION
import pytest
from selenium import webdriver
import os
from datetime import datetime
import allure

@pytest.fixture
def driver():
    """Create and configure Chrome driver"""
    chrome_options = webdriver.ChromeOptions()
    
    # Add arguments for headless mode and CI/CD compatibility
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.fixture
def base_url():
    """Base URL for the test site"""
    return "https://the-internet.herokuapp.com"


# Screenshot on failure hook - WITH ALLURE
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture screenshots on test failure.
    Screenshots are attached to both local storage and Allure reports.
    """
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        driver = None
        
        if hasattr(item, 'funcargs'):
            driver = item.funcargs.get('driver', None)
        
        if driver is None and hasattr(item, 'fixturenames'):
            if 'driver' in item.fixturenames:
                try:
                    driver = item.funcargs.get('driver')
                except:
                    pass
        
        if driver:
            try:
                # Create screenshots directory
                screenshots_dir = "screenshots"
                if not os.path.exists(screenshots_dir):
                    os.makedirs(screenshots_dir)
                    print(f"\n📁 Created directory: {screenshots_dir}")
                
                # Generate screenshot filename
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                test_name = item.nodeid.replace("::", "_").replace("/", "_").replace("\\", "_")
                screenshot_name = f"{test_name}_{timestamp}.png"
                screenshot_path = os.path.join(screenshots_dir, screenshot_name)
                
                # Capture screenshot
                driver.save_screenshot(screenshot_path)
                print(f"\n📸 Screenshot saved: {screenshot_path}")
                
                # Verify file creation
                if os.path.exists(screenshot_path):
                    file_size = os.path.getsize(screenshot_path)
                    print(f"✅ Screenshot file created: {file_size} bytes")
                    
                    # Attach to Allure report
                    with open(screenshot_path, 'rb') as image_file:
                        allure.attach(
                            image_file.read(),
                            name=f"Screenshot on Failure - {test_name}",
                            attachment_type=allure.attachment_type.PNG
                        )
                
                # Attach to HTML report (if using pytest-html)
                if hasattr(rep, 'extra'):
                    try:
                        html = f'<div><img src="../{screenshot_path}" alt="screenshot" ' \
                               f'style="width:600px;height:auto;" onclick="window.open(this.src)" ' \
                               f'style="cursor:pointer;"/></div>'
                        rep.extra.append(pytest.html.extra.html(html))
                    except Exception as e:
                        print(f"⚠️  Could not attach to HTML report: {str(e)}")
                
            except Exception as e:
                print(f"\n⚠️  Could not capture screenshot: {str(e)}")
        else:
            print(f"\n⚠️  No driver found for test: {item.nodeid}")