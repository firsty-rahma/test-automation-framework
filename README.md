# Selenium WebDriver Test Automation Framework

[![Selenium Tests](https://github.com/yourusername/test-automation-framework/actions/workflows/selenium-tests.yml/badge.svg)](https://github.com/yourusername/test-automation-framework/actions/workflows/selenium-tests.yml)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Selenium](https://img.shields.io/badge/selenium-4.15+-green.svg)](https://www.selenium.dev/)
[![Tests](https://img.shields.io/badge/tests-13%20passing-brightgreen)](https://github.com/yourusername/test-automation-framework)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A production-ready test automation framework demonstrating industry best practices for web UI testing. Built with Selenium WebDriver, Page Object Model design pattern, and comprehensive CI/CD integration.

> **Development Approach**: This project showcases modern software development practices, utilizing AI tools (Claude Sonnet 4.5) for code optimization and architectural guidance, following industry standards where developers leverage AI alongside traditional resources for enhanced productivity and code quality.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Architecture](#-architecture)
- [Getting Started](#-getting-started)
- [Running Tests](#-running-tests)
- [Screenshot on Failure](#-screenshot-on-failure)
- [CI/CD Integration](#-cicd-integration)
- [Test Organization](#-test-organization)
- [Test Coverage](#-test-coverage)
- [Configuration](#-configuration)
- [Technical Stack](#-technical-stack)
- [Project Structure](#-project-structure)
- [Best Practices](#-best-practices)
- [Contributing](#-contributing)

---

## 🎯 Overview

This framework demonstrates comprehensive test automation capabilities with:

- **13 Automated Test Cases** covering critical UI workflows
- **Page Object Model (POM)** for maintainable, scalable test architecture
- **Automated Screenshot Capture** on test failures for rapid debugging
- **CI/CD Pipeline** with GitHub Actions for continuous testing
- **HTML Reporting** with embedded screenshots and detailed metrics
- **Professional Code Organization** following industry best practices

**Test Site**: [the-internet.herokuapp.com](https://the-internet.herokuapp.com) - A dedicated automation practice site

---

## ✨ Key Features

### 1. Page Object Model Architecture

**Design Pattern Implementation:**
- Separation of page logic from test logic for enhanced maintainability
- Reusable `BasePage` class with common web interaction methods
- Individual page classes for each application page/feature
- Eliminates code duplication and improves test readability

**Benefits:**
- ✅ Easy maintenance when UI changes
- ✅ Reusable components across multiple tests
- ✅ Clear abstraction layers
- ✅ Scalable for growing test suites

### 2. Screenshot on Failure 📸

**Automatic failure capture system** that enhances debugging efficiency:

**How It Works:**
```
Test Execution → Test Fails → pytest Hook Triggered → Screenshot Captured
                                                     ↓
                                    Saved to screenshots/ directory
                                                     ↓
                                    Embedded in HTML report
                                                     ↓
                                    Uploaded to CI/CD artifacts
```

**Features:**
- ✅ Automatic screenshot capture on any test failure
- ✅ Unique filename with timestamp and test name
- ✅ Screenshots embedded directly in HTML reports
- ✅ Uploaded as CI/CD artifacts (7-day retention)
- ✅ Local storage in `screenshots/` directory

**Screenshot Naming Convention:**
```
tests_test_with_pom.py_TestCheckboxes_test_checkboxes_toggle_20241224_143022.png
│                      │                │                      │
│                      │                │                      └─ Timestamp (YYYYMMDD_HHMMSS)
│                      │                └─ Test method name
│                      └─ Test class name
└─ Test file path
```

**Viewing Screenshots:**

**Local Development:**
```bash
# After test failure
ls screenshots/

# View most recent screenshot
open screenshots/$(ls -t screenshots/ | head -1)  # Mac
start screenshots/$(ls -t screenshots/ | head -1)  # Windows
```

**CI/CD (GitHub Actions):**
1. Navigate to **Actions** tab
2. Click on failed workflow run
3. Scroll to **Artifacts** section
4. Download `failure-screenshots.zip`

**HTML Reports:**
- Screenshots automatically embedded in test failure details
- Click screenshot for full-size view
- Hover for additional metadata

### 3. Comprehensive Test Coverage

**UI Interaction Tests:**
- Dynamic element manipulation (Add/Remove)
- Form controls (Dropdowns, Checkboxes)
- Keyboard input detection and validation
- Context menu (right-click) interactions

**File Operations:**
- File upload with validation
- File download with integrity verification
- Temporary file handling

**Advanced Scenarios:**
- HTTP Basic Authentication
- Multiple window/tab management
- HTTP status code validation (200, 404, 500)

### 4. Professional Test Organization

**Pytest Markers** for flexible test execution:

```python
@pytest.mark.smoke      # Critical path tests - run first
@pytest.mark.regression # Full test suite - comprehensive coverage
@pytest.mark.ui         # User interface interaction tests
@pytest.mark.slow       # Tests requiring longer execution (>5s)
@pytest.mark.download   # File download operations
@pytest.mark.upload     # File upload operations
@pytest.mark.windows    # Multiple window handling
```

**Benefits:**
- Run critical tests first for fast feedback
- Execute specific test categories as needed
- Exclude slow tests during rapid development
- Organize tests by feature or risk level

### 5. Robust Wait Strategies

**Multiple wait mechanisms** for reliable test execution:

- **Explicit Waits**: Custom conditions for specific elements
- **Implicit Waits**: Global timeout for element location
- **Smart Waits**: Dynamic waits for AJAX and async operations
- **Custom Wait Functions**: Specialized conditions for complex scenarios

**Example Wait Implementations:**
```python
# Explicit wait for element clickability
wait.until(EC.element_to_be_clickable((By.ID, "submit-button")))

# Custom wait for file download completion
wait.until(lambda d: len(os.listdir(download_dir)) > 0)

# Wait for page title
wait.until(EC.title_is("Expected Page Title"))
```

---

## 🏗️ Architecture

### Page Object Model Structure

```
┌─────────────────────────────────────────────────────────┐
│                    Test Layer                            │
│  (test_with_pom.py - Test Classes & Methods)            │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  Page Object Layer                       │
│  (HomePage, DropdownPage, CheckboxesPage, etc.)         │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                   Base Page Layer                        │
│  (BasePage - Common methods & utilities)                │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                 Selenium WebDriver                       │
│  (Browser automation & interaction)                     │
└─────────────────────────────────────────────────────────┘
```

### Design Principles

1. **Separation of Concerns**: Test logic separated from page interaction logic
2. **DRY (Don't Repeat Yourself)**: Common methods centralized in BasePage
3. **Single Responsibility**: Each page class handles only its page's elements
4. **Encapsulation**: Page elements and actions hidden from tests
5. **Maintainability**: UI changes require updates only in page objects

---

## 🚀 Getting Started

### Prerequisites

| Requirement | Minimum Version | Purpose |
|-------------|----------------|---------|
| Python | 3.9+ | Runtime environment |
| pip | Latest | Package management |
| Chrome | Latest | Test browser |
| Git | Latest | Version control |

### Installation

**1. Clone the repository:**
```bash
git clone https://github.com/yourusername/test-automation-framework.git
cd test-automation-framework
```

**2. Create and activate virtual environment:**

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Verify installation:**
```bash
# Check Python version
python --version

# Check Selenium installation
python -c "import selenium; print(f'Selenium {selenium.__version__} installed')"

# Verify page objects import
python -c "from pages.home_page import HomePage; print('✅ Page objects working')"
```

**5. Create necessary directories:**
```bash
mkdir -p reports screenshots
```

### Quick Start

**Run a single smoke test:**
```bash
pytest tests/test_with_pom.py::TestBasicAuth::test_basic_auth_success -v
```

**Expected output:**
```
tests/test_with_pom.py::TestBasicAuth::test_basic_auth_success PASSED [100%]
======================== 1 passed in 3.42s ========================
```

---

## 🧪 Running Tests

### Basic Execution

```bash
# Run all tests
pytest tests/test_with_pom.py -v

# Run all tests with detailed output
pytest tests/test_with_pom.py -vv

# Run with print statements visible
pytest tests/test_with_pom.py -v -s
```

### Generate HTML Report

```bash
# Generate comprehensive HTML report
pytest tests/test_with_pom.py --html=reports/report.html --self-contained-html

# Then open the report
# Mac: open reports/report.html
# Windows: start reports/report.html
# Linux: xdg-open reports/report.html
```

**Report Contents:**
- ✅ Test execution summary (pass/fail/skip)
- ⏱️ Individual test execution times
- 📊 Total duration and statistics
- 📸 Embedded screenshots for failures
- 📝 Error messages and stack traces
- 🏷️ Test markers and categories

### Run Tests by Category

```bash
# Quick smoke tests (critical path validation)
pytest -m smoke -v

# Full regression suite
pytest -m regression -v

# Only UI interaction tests
pytest -m ui -v

# File operation tests
pytest -m "download or upload" -v

# Exclude slow tests (for rapid development)
pytest -m "not slow" -v

# Combine multiple markers
pytest -m "smoke and ui" -v
```

### Run Specific Tests

```bash
# Run specific test class
pytest tests/test_with_pom.py::TestCheckboxes -v

# Run specific test method
pytest tests/test_with_pom.py::TestCheckboxes::test_checkboxes_toggle -v

# Run tests matching keyword
pytest -k "checkbox" -v

# Run tests in specific file
pytest tests/test_with_pom.py -v
```

### Advanced Execution Options

```bash
# Stop after first failure
pytest tests/test_with_pom.py -x

# Stop after N failures
pytest tests/test_with_pom.py --maxfail=3

# Run last failed tests only
pytest tests/test_with_pom.py --lf

# Run failed tests first, then others
pytest tests/test_with_pom.py --ff

# Parallel execution (requires pytest-xdist)
pytest tests/test_with_pom.py -n 4  # 4 parallel workers

# Show slowest 5 tests
pytest tests/test_with_pom.py --durations=5
```

### Debugging Tests

```bash
# Drop into debugger on failure
pytest tests/test_with_pom.py --pdb

# Verbose output with print statements
pytest tests/test_with_pom.py -vv -s

# Show local variables on failure
pytest tests/test_with_pom.py -l
```

---

## 📸 Screenshot on Failure

### Technical Implementation

**Hook Function (`conftest.py`):**
```python
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture screenshots automatically on test failure"""
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get('driver', None)
        if driver:
            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"screenshots/{item.nodeid}_{timestamp}.png"
            
            # Capture and save
            driver.save_screenshot(screenshot_path)
```

### Configuration Options

**Directory Structure:**
```bash
screenshots/
├── tests_test_with_pom.py_TestCheckboxes_test_toggle_20241224_143022.png
├── tests_test_with_pom.py_TestDropdown_test_select_20241224_143045.png
└── tests_test_with_pom.py_TestFileUpload_test_upload_20241224_143108.png
```

**Customization:**

Change screenshot directory:
```python
# In conftest.py
screenshots_dir = "test_failures"  # Instead of "screenshots"
```

Capture screenshots for all tests (not just failures):
```python
# In conftest.py - remove the 'failed' condition
if rep.when == "call":  # Captures for all tests
    driver.save_screenshot(screenshot_path)
```

### Integration with CI/CD

Screenshots are automatically uploaded as artifacts in GitHub Actions:

**Configuration (`.github/workflows/selenium-tests.yml`):**
```yaml
- name: Upload screenshots on failure
  if: failure()
  uses: actions/upload-artifact@v4
  with:
    name: failure-screenshots
    path: screenshots/
    retention-days: 7
```

**Accessing CI/CD Screenshots:**
1. Go to **Actions** tab in GitHub
2. Click on the failed workflow run
3. Scroll to **Artifacts** section at the bottom
4. Download **failure-screenshots.zip**
5. Extract and view screenshot files

### Best Practices

✅ **DO:**
- Review screenshots immediately after test failures
- Share screenshots with team members for collaborative debugging
- Keep screenshots in `.gitignore` to avoid repository bloat
- Use descriptive test names for easier screenshot identification

❌ **DON'T:**
- Commit screenshot files to version control
- Rely solely on screenshots without checking logs
- Ignore screenshot file size (compress if needed)
- Keep old screenshots indefinitely (clean up regularly)

---

## 🔄 CI/CD Integration

### GitHub Actions Workflow

**Automated Testing Pipeline:**

```yaml
Trigger Events:
├── Push to main/develop branch
├── Pull request creation
├── Scheduled (daily at 2 AM UTC)
└── Manual trigger (workflow_dispatch)

Pipeline Stages:
├── 1. Environment Setup
│   ├── Checkout code
│   ├── Setup Python 3.11
│   ├── Install Chrome browser
│   └── Install dependencies
├── 2. Test Execution
│   ├── Run smoke tests (fast feedback)
│   └── Run full test suite
├── 3. Artifact Collection
│   ├── Upload HTML reports (30-day retention)
│   └── Upload failure screenshots (7-day retention)
└── 4. Results Summary
    └── Generate test summary in GitHub UI
```

**Workflow Configuration:**

Location: `.github/workflows/selenium-tests.yml`

Key features:
- ✅ Automated Chrome/ChromeDriver installation
- ✅ Python dependency caching for faster runs
- ✅ Parallel test execution capability
- ✅ Artifact upload for test reports and screenshots
- ✅ Test summary in GitHub Actions UI

**Viewing Results:**

1. **In GitHub UI:**
   - Go to repository → **Actions** tab
   - Click on workflow run
   - View test summary and artifacts

2. **Email Notifications:**
   - Configure in GitHub Settings → Notifications
   - Get alerts for failed workflow runs

3. **Badge Status:**
   - README badge shows current test status
   - Updates automatically after each run

---

## 🎯 Test Organization

### Test Structure

```
tests/test_with_pom.py
├── TestAddRemoveElements      [1 test]  @smoke @ui
├── TestBasicAuth              [1 test]  @smoke
├── TestDropdown               [2 tests] @regression @ui
├── TestContextMenu            [1 test]  @ui
├── TestFileDownload           [1 test]  @download @slow
├── TestFileUpload             [1 test]  @upload
├── TestStatusCodes            [3 tests] @regression
├── TestCheckboxes             [1 test]  @smoke @ui
├── TestKeyPresses             [1 test]  @ui
└── TestMultipleWindows        [1 test]  @windows
```

### Marker Definitions

| Marker | Purpose | Test Count | Execution Time |
|--------|---------|------------|----------------|
| `smoke` | Critical path validation | 3 | ~10 seconds |
| `regression` | Comprehensive coverage | 5 | ~30 seconds |
| `ui` | User interface tests | 8 | ~25 seconds |
| `slow` | Tests >5 seconds | 1 | ~20 seconds |
| `download` | File download tests | 1 | ~20 seconds |
| `upload` | File upload tests | 1 | ~5 seconds |
| `windows` | Multi-window tests | 1 | ~8 seconds |

### Recommended Test Execution Strategy

**During Development:**
```bash
# 1. Run smoke tests after each change
pytest -m smoke -v

# 2. Run feature-specific tests
pytest -m ui -v  # If working on UI

# 3. Run all tests before commit
pytest tests/test_with_pom.py -v
```

**Before Release:**
```bash
# 1. Full regression suite
pytest -m regression -v

# 2. All tests with HTML report
pytest tests/test_with_pom.py --html=reports/release-report.html --self-contained-html

# 3. Verify all markers
pytest --markers
```

---

## 📊 Test Coverage

### Feature Coverage Matrix

| Feature | Test Class | Tests | Status | Priority |
|---------|-----------|-------|--------|----------|
| Dynamic Elements | TestAddRemoveElements | 1 | ✅ | High |
| Authentication | TestBasicAuth | 1 | ✅ | High |
| Form Controls | TestDropdown | 2 | ✅ | High |
| Context Menus | TestContextMenu | 1 | ✅ | Medium |
| File Download | TestFileDownload | 1 | ✅ | High |
| File Upload | TestFileUpload | 1 | ✅ | High |
| HTTP Status | TestStatusCodes | 3 | ✅ | Medium |
| Checkboxes | TestCheckboxes | 1 | ✅ | High |
| Keyboard Input | TestKeyPresses | 1 | ✅ | Medium |
| Window Management | TestMultipleWindows | 1 | ✅ | High |

**Total:** 13 tests | **Passing:** 13 (100%) | **Coverage:** Critical workflows

---

## ⚙️ Configuration

### config.py

```python
class Config:
    BASE_URL = "https://the-internet.herokuapp.com"
    TIMEOUT = 10          # Explicit wait timeout (seconds)
    USERNAME = "admin"    # Basic auth username (demo)
    PASSWORD = "admin"    # Basic auth password (demo)
    BROWSER = "chrome"    # Default browser
```

### pytest.ini

```ini
[pytest]
# Test discovery
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# Markers
markers =
    smoke: Quick smoke tests
    regression: Full regression tests
    ui: UI interaction tests
    slow: Tests that take longer to run
    download: File download tests
    upload: File upload tests
    windows: Multiple windows tests

# Reporting
addopts = 
    -v
    --tb=short
    --strict-markers
    --html=reports/report.html
    --self-contained-html

# Logging
log_cli = true
log_cli_level = INFO
```

### conftest.py

Centralized pytest configuration:
- **Fixtures**: `driver`, `base_url`
- **Hooks**: Screenshot on failure
- **Setup/Teardown**: Browser lifecycle management

---

## 🛠️ Technical Stack

### Core Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.9+ | Programming language |
| **Selenium WebDriver** | 4.15+ | Browser automation |
| **Pytest** | 7.4+ | Testing framework |
| **pytest-html** | 4.1+ | HTML reporting |
| **pytest-xdist** | 3.5+ | Parallel execution |

### Development Tools

- **Git**: Version control
- **Virtual Environment**: Dependency isolation
- **Chrome/ChromeDriver**: Test browser
- **GitHub Actions**: CI/CD platform

### Python Packages

```txt
selenium==4.15.2        # Browser automation
pytest==7.4.3          # Testing framework
pytest-html==4.1.1     # HTML reports
pytest-xdist==3.5.0    # Parallel execution
```

---

## 📁 Project Structure

```
test-automation-framework/
│
├── .github/
│   └── workflows/
│       └── selenium-tests.yml         # CI/CD configuration
│
├── pages/                             # Page Object Model
│   ├── __init__.py                   # Package initializer
│   ├── base_page.py                  # Base page class
│   ├── home_page.py                  # Home/navigation page
│   ├── add_remove_page.py            # Add/Remove Elements page
│   ├── dropdown_page.py              # Dropdown page
│   ├── checkboxes_page.py            # Checkboxes page
│   ├── context_menu_page.py          # Context menu page
│   ├── file_download_page.py         # File download page
│   ├── file_upload_page.py           # File upload page
│   ├── status_codes_page.py          # Status codes page
│   ├── key_presses_page.py           # Key presses page
│   ├── multiple_windows_page.py      # Multiple windows page
│   └── basic_auth_page.py            # Basic auth page
│
├── tests/                             # Test suites
│   ├── __init__.py                   # Package initializer
│   ├── test_with_pom.py              # Main POM-based tests
│   └── test_basic.py                 # Legacy tests (optional)
│
├── reports/                           # Test reports (generated)
│   ├── report.html                   # Latest HTML report
│   └── *.html                        # Historical reports
│
├── screenshots/                       # Failure screenshots (generated)
│   └── *.png                         # Screenshot files
│
├── config.py                          # Test configuration
├── conftest.py                        # Pytest fixtures & hooks
├── pytest.ini                         # Pytest configuration
├── requirements.txt                   # Python dependencies
├── .gitignore                         # Git ignore rules
└── README.md                          # This file
```

---

## 💡 Best Practices Demonstrated

### Code Quality
- ✅ **DRY Principle**: No code duplication
- ✅ **SOLID Principles**: Single responsibility, open/closed
- ✅ **PEP 8**: Python style guide compliance
- ✅ **Type Hints**: Clear function signatures (optional)
- ✅ **Docstrings**: Comprehensive documentation

### Test Design
- ✅ **Independent Tests**: No dependencies between tests
- ✅ **Descriptive Names**: Clear test purpose from name
- ✅ **Arrange-Act-Assert**: Clear test structure
- ✅ **Explicit Assertions**: Meaningful failure messages
- ✅ **Setup/Teardown**: Proper test lifecycle management

### Framework Design
- ✅ **Page Object Model**: Separation of concerns
- ✅ **Reusable Components**: BasePage with common methods
- ✅ **Configuration Management**: Centralized settings
- ✅ **Error Handling**: Graceful failure management
- ✅ **Logging**: Comprehensive test execution logs

### DevOps
- ✅ **CI/CD Integration**: Automated testing
- ✅ **Version Control**: Git best practices
- ✅ **Documentation**: Comprehensive README
- ✅ **Artifact Management**: Report and screenshot storage

---

## 🎓 Skills Demonstrated

### Technical Skills
- **Test Automation**: Selenium WebDriver, web UI testing
- **Python Programming**: OOP, fixtures, decorators, hooks
- **Design Patterns**: Page Object Model, Factory pattern
- **Testing Frameworks**: Pytest, markers, fixtures, parameterization
- **CI/CD**: GitHub Actions, workflow automation
- **Version Control**: Git, branching, pull requests

### Software Engineering
- **Clean Code**: Readable, maintainable, documented
- **Architecture**: Layered design, separation of concerns
- **Problem Solving**: Handling timing, synchronization, edge cases
- **Documentation**: Technical writing, code comments
- **Best Practices**: Industry standards, coding conventions

### Quality Assurance
- **Test Strategy**: Risk-based testing, smoke vs regression
- **Test Organization**: Markers, categories, priorities
- **Debugging**: Screenshots, logs, error analysis
- **Reporting**: HTML reports, metrics, visualization

---

## 🤝 Contributing

This is a portfolio project demonstrating test automation capabilities. Feedback and suggestions are welcome!

### Suggesting Improvements

1. Open an issue describing the improvement
2. Provide context and rationale
3. Include examples if applicable

### Reporting Bugs

1. Check existing issues first
2. Provide reproduction steps
3. Include error messages and screenshots
4. Specify environment details

---

## 📄 License

This project is for educational and portfolio purposes.

---

## 👤 Author

**Your Name**
- GitHub: [@firsty-rahma](https://github.com/firsty-rahma)
- LinkedIn: [Firstyani Rahma](https://www.linkedin.com/in/firstyani-rahma-412990236/)
- Email: firsty.rahma9521@gmail.com

---

## 🙏 Acknowledgments

- **Test Site**: [the-internet.herokuapp.com](https://the-internet.herokuapp.com) - Excellent automation practice resource
- **Selenium**: WebDriver team for browser automation tools
- **Pytest**: Testing framework community
- **AI Assistance**: Claude Sonnet 4.5 for code optimization and architectural guidance

---

## 📚 Additional Resources

### Learning Materials
- [Selenium Documentation](https://www.selenium.dev/documentation/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Page Object Model Pattern](https://www.selenium.dev/documentation/test_practices/encouraged/page_object_models/)
- [Python Testing Best Practices](https://docs.python-guide.org/writing/tests/)

### Related Projects
- [Selenium Examples](https://github.com/SeleniumHQ/selenium/tree/trunk/py/test)
- [pytest-selenium](https://github.com/pytest-dev/pytest-selenium)

---

**Last Updated:** December 2024

**Project Status:** ✅ Active | 📈 Continuously Improving

---

<div align="center">

### ⭐ If you find this project helpful, please consider giving it a star!

**Built with ❤️ and modern development tools**

</div>