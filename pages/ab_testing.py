from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class ABTestingPage(BasePage):
    HEADING = (By.TAG_NAME, 'h3')
    HEADER_LIST = ['A/B Test Variation 1', 'A/B Test Control']
    COOKIE = {'name' : 'optimizelyOptOut', 'value': 'true'}

    def get_the_header(self):
        """Get the header"""
        element = self.get_element(self.HEADING)
        return element.text
    
    def test_forge_cookie_on_target_page(self):
        """Verify changed text after forging an opt-out cookie"""
        header_text = self.get_the_header()
        assert header_text in self.HEADER_LIST
        
        self.driver.add_cookie(self.COOKIE)
        self.driver.refresh()

        header_text = self.get_the_header()
        assert header_text == 'No A/B Test'
    
    def test_url_parameter(self):
        """Verify changed text after append an opt out parameter to URL"""
        url = "https://the-internet.herokuapp.com/abtest?optimizely_opt_out=true"
        self.driver.get(url)
        self.driver.switch_to.alert.dismiss()

        header_text = self.get_the_header()
        assert header_text == 'No A/B Test'

        

