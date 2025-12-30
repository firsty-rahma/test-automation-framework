# conftest.py - CORRECTED VERSION
import pytest
from selenium import webdriver
import os
from datetime import datetime

@pytest.fixture
def driver():
    """Create and configure Chrome driver"""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless=new")  # Headless mode for CI/CD
    chrome_options.add_argument("--no-sandbox")     # Required for Docker/CI
    chrome_options.add_argument("--disable-dev-shm-usage")  # Memory optimization
    chrome_options.add_argument("--disable-gpu")    # No GPU in CI
    chrome_options.add_argument("--window-size=1920,1080")  # Consistent size

    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.fixture
def base_url():
    """Base URL for the test site"""
    return "https://the-internet.herokuapp.com"


# Screenshot on failure hook - FIXED VERSION
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture screenshots on test failure.
    This runs after each test and captures a screenshot if the test failed.
    """
    # Execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()
    
    # Only capture screenshot during the actual test execution phase (not setup/teardown)
    if rep.when == "call" and rep.failed:
        # Get the driver fixture from the test
        driver = None
        
        # Try to get driver from funcargs (works for function-level fixtures)
        if hasattr(item, 'funcargs'):
            driver = item.funcargs.get('driver', None)
        
        # Try to get from fixturenames
        if driver is None and hasattr(item, 'fixturenames'):
            if 'driver' in item.fixturenames:
                try:
                    driver = item.funcargs.get('driver')
                except:
                    pass
        
        if driver:
            try:
                # Create screenshots directory if it doesn't exist
                screenshots_dir = "screenshots"
                if not os.path.exists(screenshots_dir):
                    os.makedirs(screenshots_dir)
                    print(f"\n📁 Created directory: {screenshots_dir}")
                
                # Generate screenshot filename with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                # Clean up test name for filename
                test_name = item.nodeid.replace("::", "_").replace("/", "_").replace("\\", "_")
                screenshot_name = f"{test_name}_{timestamp}.png"
                screenshot_path = os.path.join(screenshots_dir, screenshot_name)
                
                # Capture screenshot
                driver.save_screenshot(screenshot_path)
                
                # Print the screenshot location (visible in console)
                print(f"\n📸 Screenshot saved: {screenshot_path}")
                
                # Verify file was created
                if os.path.exists(screenshot_path):
                    file_size = os.path.getsize(screenshot_path)
                    print(f"✅ Screenshot file created: {file_size} bytes")
                else:
                    print(f"❌ Screenshot file not found at {screenshot_path}")
                
                # Attach screenshot to HTML report (if using pytest-html)
                if hasattr(rep, 'extra'):
                    try:
                        # Add screenshot to HTML report
                        html = f'<div><img src="../{screenshot_path}" alt="screenshot" ' \
                               f'style="width:600px;height:auto;" onclick="window.open(this.src)" ' \
                               f'style="cursor:pointer;"/></div>'
                        rep.extra.append(pytest.html.extra.html(html))
                    except Exception as e:
                        print(f"⚠️  Could not attach to HTML report: {str(e)}")
                
            except Exception as e:
                print(f"\n⚠️  Could not capture screenshot: {str(e)}")
                import traceback
                traceback.print_exc()
        else:
            print(f"\n⚠️  No driver found for test: {item.nodeid}")
            print(f"   Available fixtures: {getattr(item, 'fixturenames', [])}")
            print(f"   Funcargs: {list(getattr(item, 'funcargs', {}).keys())}")