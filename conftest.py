# conftest.py - Adding screenshot on failure

import pytest
from selenium import webdriver
import os
from datetime import datetime

@pytest.fixture
def driver():
    """Create and configure Chrome driver"""
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.fixture
def base_url():
    """Base URL for the test site"""
    return "https://the-internet.herokuapp.com"

# Screenshot on failure hook
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture screenshots on test failure.
    This runs after each test and captures a screenshot if the test failed.
    """
    # Execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # Check if the test failed during the "call" phase (actual test execution)
    if rep.when == "call" and rep.failed:
        # Get the driver fixture from the test
        try:
            driver = item.funcargs.get('driver', None)

            if driver:
                # Create screenshote directory if it doesn't exist
                screenshots_dir = "screenshots"
                if not os.path.exists(screenshots_dir):
                    os.makedirs(screenshots_dir)

                # Generate screenshot filename with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                test_name = item.nodeid.replace("::", "_").replace("/", "_")
                screenshot_name = f"{test_name}_{timestamp}.png"
                screenshot_path = os.path.join(screenshots_dir, screenshot_name)

                # Capture screenshot
                driver.save_screenshot(screenshot_path)

                # Print the screenshot location
                print(f"\n📸 Screenshot saved: {screenshot_path}")
                
                # Attach screenshot to HTML report (if using pytest-html)
                if hasattr(rep, 'extra'):
                    # Add screenshot to HTML report
                    html = f'<div><img src="../{screenshot_path}" alt="screenshot" ' \
                           f'style="width:600px;height:auto;" onclick="window.open(this.src)" ' \
                           f'style="cursor:pointer;"/></div>'
                    rep.extra.append(pytest.html.extra.html(html))
        except Exception as e:
                print(f"\n⚠️  Could not capture screenshot: {str(e)}")

# Optional: Hook to add extra HTML content to reports
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Enhanced reporting with extra information"""
    outcome = yield
    report = outcome.get_result()
    
    # Add extra information for HTML reports
    if report.when == 'call':
        # Add test description to report
        test_doc = item.function.__doc__
        if test_doc and hasattr(report, 'extra'):
            report.extra.append(pytest.html.extra.text(test_doc, name="Description"))
        
        # Add marker information
        markers = [marker.name for marker in item.iter_markers()]
        if markers and hasattr(report, 'extra'):
            report.extra.append(pytest.html.extra.text(", ".join(markers), name="Test Markers"))