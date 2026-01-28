# conftest.py - WITH CROSS-BROWSER AND ALLURE SUPPORT
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import os
from datetime import datetime
import allure


def pytest_addoption(parser):
    """Add command-line options for browser selection"""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to run tests on: chrome, firefox, edge"
    )


@pytest.fixture(scope="function")
def browser_name(request):
    """Get browser name from command line option"""
    return request.config.getoption("--browser")


@pytest.fixture
def driver(browser_name):
    """Create and configure browser driver based on browser_name"""
    driver = None
    
    # Check if running in CI environment
    is_ci = os.getenv('CI') == 'true'
    
    # Chrome configuration
    if browser_name.lower() == "chrome":
        chrome_options = webdriver.ChromeOptions()
        
        # IMPORTANT: Set Chrome binary location for local testing
        if not is_ci:
            # Your Chrome for Testing location
            chrome_path = r"C:\Users\Nisa\Downloads\chrome-win64\chrome.exe"
            if os.path.exists(chrome_path):
                chrome_options.binary_location = chrome_path
                print(f"✅ Using Chrome at: {chrome_path}")
        
        # Only add headless in CI/CD
        if is_ci:
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
        
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Get ChromeDriver with specific version matching Chrome 144
        try:
            service = ChromeService(ChromeDriverManager(driver_version="144").install())
        except:
            # Fallback to latest
            service = ChromeService(ChromeDriverManager(driver_version="latest").install())
        
        driver = webdriver.Chrome(
            service=service,
            options=chrome_options
        )
        allure.attach("Chrome", name="Browser", attachment_type=allure.attachment_type.TEXT)
    
    # Firefox configuration
    elif browser_name.lower() == "firefox":
        firefox_options = webdriver.FirefoxOptions()
        
        # Only add headless in CI/CD
        if is_ci:
            firefox_options.add_argument("--headless")
        
        firefox_options.add_argument("--width=1920")
        firefox_options.add_argument("--height=1080")
        
        # Firefox preferences for better CI/CD performance
        firefox_options.set_preference("browser.startup.page", 0)
        firefox_options.set_preference("browser.cache.disk.enable", False)
        firefox_options.set_preference("browser.cache.memory.enable", False)
        firefox_options.set_preference("browser.cache.offline.enable", False)
        firefox_options.set_preference("network.http.use-cache", False)
        
        # Increase timeout for CI/CD
        firefox_options.timeouts = {'implicit': 30000, 'pageLoad': 60000, 'script': 60000}
        
        try:
            service = FirefoxService(GeckoDriverManager().install())
            # Increase service timeout
            service.service_args = ['--log', 'debug']
            
            driver = webdriver.Firefox(
                service=service,
                options=firefox_options
            )
        except Exception as e:
            print(f"⚠️ Firefox initialization error: {e}")
            raise
        
        allure.attach("Firefox", name="Browser", attachment_type=allure.attachment_type.TEXT)
    
    # Edge configuration
    elif browser_name.lower() == "edge":
        edge_options = webdriver.EdgeOptions()
        
        # Only add headless in CI/CD
        if is_ci:
            edge_options.add_argument("--headless")
            edge_options.add_argument("--no-sandbox")
            edge_options.add_argument("--disable-dev-shm-usage")
            edge_options.add_argument("--disable-gpu")
        
        edge_options.add_argument("--window-size=1920,1080")
        
        driver = webdriver.Edge(
            service=EdgeService(EdgeChromiumDriverManager().install()),
            options=edge_options
        )
        allure.attach("Edge", name="Browser", attachment_type=allure.attachment_type.TEXT)
    
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")
    
    # Set implicit wait - longer for Firefox
    if browser_name.lower() == "firefox":
        driver.implicitly_wait(30)
    else:
        driver.implicitly_wait(10)
    
    # Set page load timeout
    driver.set_page_load_timeout(60)
    
    # Attach browser info to Allure
    allure.dynamic.parameter("Browser", browser_name)
    
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