# Test Automation Framework

I developed this project as part of my journey to learn automation testing with Selenium. I consulted various resources, including documentation, tutorials, and AI assistance, to understand the best practices.

## Features
✅ 11 automated test scenarios
✅ pytest framework with fixtures  
✅ Explicit waits for reliability  
✅ Clean test structure  

## Current Status
🔄 **In Progress**
- [x] Basic Selenium tests
- [x] Page Object Model structure
- [ ] API tests (in progress)
- [ ] CI/CD with GitHub Actions
- [ ] Comprehensive documentation

## Test Coverage
- Add/Remove Elements
- Basic Authentication
- Dropdown and Checkboxes Selection
- Context Menu
- File Upload and Download
- Status Codes (200, 404, 500)
- Switching Windows

## Tech Stack
- Python 3.9+
- Selenium WebDriver
- pytest
- Chrome WebDriver

## Installation
```bash
# Clone repository
git clone https://github.com/yourusername/test-automation-framework.git
cd test-automation-framework

# Install dependencies
pip install -r requirements.txt

# Make sure ChromeDriver is installed
# Download from: https://chromedriver.chromium.org/
```

## Usage
```bash
# Run all tests
pytest test_basic.py -v

# Run specific test
pytest test_basic.py::test_add_remove_elements -v

# Run tests matching pattern
pytest -k "auth" -v

# Generate HTML report
pytest test_basic.py --html=report.html --self-contained-html
