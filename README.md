# Selenium WebDriver Test Automation Framework

[![Selenium Tests](https://github.com/firsty-rahma/test-automation-framework/actions/workflows/selenium-tests.yml/badge.svg)](https://github.com/firsty-rahma/test-automation-framework/actions/workflows/selenium-tests.yml)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Selenium](https://img.shields.io/badge/selenium-4.15+-green.svg)](https://www.selenium.dev/)

A comprehensive test automation framework demonstrating modern software testing practices. This project showcases industry-standard design patterns, CI/CD integration, and professional test organization.

> **Note**: This project was developed with modern development tools including AI assistance (Claude Sonnet 4.5) for code optimization and best practices guidance, following current industry standards where developers leverage AI tools alongside traditional resources.

## 🎯 Project Overview

This framework demonstrates proficiency in:
- **Selenium WebDriver** for browser automation
- **Page Object Model (POM)** design pattern for maintainability
- **Pytest** framework with fixtures and markers
- **CI/CD integration** with GitHub Actions
- **Professional reporting** and test organization

## ✨ Key Features

### 1. Page Object Model Architecture
- Clear separation between page logic and test logic
- Reusable page components with `BasePage` class
- Easy maintenance when UI changes
- Scalable structure for growing test suites

### 2. Comprehensive Test Coverage (13 Tests)
✅ **UI Interactions**
- Add/Remove Elements dynamically
- Dropdown menus selection
- Checkbox state management
- Keyboard input detection

✅ **File Operations**
- File upload functionality
- File download with verification

✅ **Authentication & Security**
- Basic HTTP authentication

✅ **Advanced Interactions**
- Context menu (right-click) handling
- Multiple windows/tabs management

✅ **API/Status Testing**
- HTTP status codes (200, 404, 500)

### 3. Professional Test Organization
Tests are categorized using pytest markers:
- `@pytest.mark.smoke` - Critical path tests (fast feedback)
- `@pytest.mark.regression` - Full test suite coverage
- `@pytest.mark.ui` - User interface interaction tests
- `@pytest.mark.slow` - Tests requiring longer execution time
- `@pytest.mark.download` / `@pytest.mark.upload` - File operation tests

### 4. Robust Wait Strategies
- Explicit waits for element visibility and interactivity
- Custom wait conditions for dynamic content
- Implicit wait configuration for stability
- Smart handling of timing-sensitive operations

## 🏗️ Project Structure

```
test-automation-framework/
│
├── pages/                      # Page Object Model classes
│   ├── __init__.py
│   ├── base_page.py           # Base class with common methods
│   ├── home_page.py           # Home page navigation
│   ├── add_remove_page.py     # Add/Remove Elements page
│   ├── dropdown_page.py       # Dropdown page
│   ├── checkboxes_page.py     # Checkboxes page
│   ├── context_menu_page.py   # Context menu page
│   ├── file_download_page.py  # File download page
│   ├── file_upload_page.py    # File upload page
│   ├── status_codes_page.py   # Status codes page
│   ├── key_presses_page.py    # Key presses page
│   ├── multiple_windows_page.py # Multiple windows page
│   └── basic_auth_page.py     # Basic auth page
│
├── tests/                      # Test suites
│   ├── __init__.py
│   ├── test_with_pom.py       # POM-based test suite (primary)
│   └── test_basic.py          # Legacy tests (pre-refactoring)
│
├── reports/                    # Test reports (auto-generated)
├── .github/
│   └── workflows/
│       └── selenium-tests.yml  # CI/CD pipeline configuration
│
├── config.py                   # Configuration settings
├── conftest.py                 # Pytest fixtures
├── pytest.ini                  # Pytest configuration
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🚀 Getting Started

### Prerequisites
- Python 3.9 or higher
- Chrome browser
- Git

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/firsty-rahma/test-automation-framework.git
cd test-automation-framework
```

2. **Create a virtual environment (recommended):**
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Verify ChromeDriver:**
   - ChromeDriver should be installed automatically with Selenium
   - Or download manually from: https://chromedriver.chromium.org/

## 🧪 Running Tests

### Basic Test Execution

```bash
# Run all POM-based tests (recommended)
pytest tests/test_with_pom.py -v

# Run legacy tests
pytest tests/test_basic.py -v

# Run all tests
pytest -v
```

### Generate HTML Report

```bash
pytest tests/test_with_pom.py --html=reports/report.html --self-contained-html
```

Then open `reports/report.html` in your browser to view results.

### Run Tests by Category

```bash
# Quick smoke tests (critical path validation)
pytest -m smoke -v

# Full regression suite
pytest -m regression -v

# Only UI interaction tests
pytest -m ui -v

# Exclude slow tests (for faster feedback during development)
pytest -m "not slow" -v

# File operation tests only
pytest -m "download or upload" -v
```

### Run Specific Tests

```bash
# Run specific test class
pytest tests/test_with_pom.py::TestCheckboxes -v

# Run specific test method
pytest tests/test_with_pom.py::TestCheckboxes::test_checkboxes_toggle -v

# Run tests matching keyword
pytest -k "dropdown" -v
```

### Parallel Execution (Faster)

```bash
# Run tests in parallel with 4 workers
pytest -n 4 -v
```

## 📊 Test Reports

After running tests with the `--html` flag, the report includes:
- ✅ Test execution summary (pass/fail/skip counts)
- ⏱️ Execution time for each test
- 📝 Detailed error messages and stack traces
- 🗂️ Test hierarchy and organization
- 📈 Historical test trends (when run multiple times)

## 🔄 CI/CD Integration

### GitHub Actions Workflow

The project includes automated testing that runs:
- ✅ On every push to `main` or `develop` branches
- ✅ On every pull request
- ✅ Daily at 2 AM UTC (scheduled)
- ✅ Manually via GitHub Actions UI

**Workflow stages:**
1. Setup Python and Chrome environment
2. Install dependencies
3. Run smoke tests (fast feedback)
4. Run full test suite
5. Upload test reports as artifacts (retained for 30 days)

**View Results:**
- Go to the **Actions** tab in your GitHub repository
- Click on any workflow run to see test results
- Download test reports from artifacts

## 📈 Test Coverage Summary

| Feature | Test Class | Tests | Status |
|---------|-----------|-------|--------|
| Add/Remove Elements | `TestAddRemoveElements` | 1 | ✅ |
| Basic Authentication | `TestBasicAuth` | 1 | ✅ |
| Dropdown Selection | `TestDropdown` | 2 | ✅ |
| Context Menu | `TestContextMenu` | 1 | ✅ |
| File Download | `TestFileDownload` | 1 | ✅ |
| File Upload | `TestFileUpload` | 1 | ✅ |
| HTTP Status Codes | `TestStatusCodes` | 3 | ✅ |
| Checkboxes | `TestCheckboxes` | 1 | ✅ |
| Key Presses | `TestKeyPresses` | 1 | ✅ |
| Multiple Windows | `TestMultipleWindows` | 1 | ✅ |

**Total**: 13 automated tests

## 🛠️ Tech Stack

| Technology | Purpose | Version |
|------------|---------|---------|
| **Python** | Programming language | 3.9+ |
| **Selenium WebDriver** | Browser automation | 4.15+ |
| **Pytest** | Testing framework | 7.4+ |
| **pytest-html** | HTML test reporting | 4.1+ |
| **GitHub Actions** | CI/CD pipeline | - |
| **Chrome/ChromeDriver** | Test browser | Latest |

## 🎓 Skills Demonstrated

This project showcases:

**Technical Skills:**
- Test automation with Selenium WebDriver
- Python programming (OOP, fixtures, decorators)
- Page Object Model design pattern
- Pytest framework and markers
- Explicit/implicit wait strategies
- File handling and browser interactions

**Software Engineering Practices:**
- Clean code architecture
- Design patterns (POM, DRY principles)
- Test organization and maintainability
- Version control with Git
- CI/CD pipeline configuration
- Documentation best practices

**Problem-Solving:**
- Dynamic element handling
- Multi-window management
- File upload/download testing
- Timing and synchronization issues

## 📝 Configuration

### config.py
```python
BASE_URL = "https://the-internet.herokuapp.com"
TIMEOUT = 10  # seconds
BROWSER = "chrome"
```

### pytest.ini
Key configurations:
- Test discovery patterns
- Marker definitions (smoke, regression, ui, etc.)
- HTML report settings
- Logging configuration

## 🔄 Project Evolution

This project demonstrates continuous improvement:

### Phase 1: Initial Implementation ✅
- Direct Selenium WebDriver usage
- Functional test coverage
- Basic test organization

### Phase 2: Refactoring with POM ✅
- Implemented Page Object Model
- Created reusable page classes
- Improved test maintainability

### Phase 3: Professional Setup ✅
- Added pytest markers for test organization
- Configured HTML reporting
- Set up CI/CD pipeline

### Phase 4: Future Enhancements 🔄
- [ ] API testing integration
- [ ] Allure reporting
- [ ] Cross-browser testing (Firefox, Edge)
- [ ] Screenshot capture on test failure
- [ ] Database validation tests

## 📚 Resources & Learning

This project was built using best practices from:
- [Selenium Documentation](https://www.selenium.dev/documentation/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Page Object Model Pattern](https://www.selenium.dev/documentation/test_practices/encouraged/page_object_models/)
- Modern AI tools for code optimization and best practices

## 🤝 Development Approach

This project demonstrates modern software development practices:
- Utilizing AI tools (Claude Sonnet 4.5) for code optimization and best practices
- Following industry-standard design patterns
- Continuous learning and improvement
- Emphasis on clean, maintainable code

## 📄 License

This project is for educational and portfolio purposes.

## 👤 Author

**Your Name**
- GitHub: [@firsty-rahma](https://github.com/firsty-rahma)
- LinkedIn: [Firstyani Rahma](https://www.linkedin.com/in/firstyani-rahma-412990236/)

---

### Test Site Credit
This framework uses [the-internet.herokuapp.com](https://the-internet.herokuapp.com) - a website specifically designed for automation testing practice.

**Last Updated:** December 2025