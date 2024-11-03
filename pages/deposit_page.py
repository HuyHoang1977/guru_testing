from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DepositPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

        # Locators
        self.accountno_textbox = (By.NAME, "accountno")
        self.amount_textbox = (By.NAME, "ammount")
        self.description_textbox = (By.NAME, "desc")
        self.submit_button = (By.XPATH, "//input[@value='Submit']")
        self.reset_button = (By.XPATH, "//input[@value='Reset']")
        
        # Locators for error messages (these IDs may vary depending on actual implementation)
        self.heading_successfully = (By.CLASS_NAME, "heading3")
        self.accountno_error = (By.ID, "message2")
        self.amount_error = (By.ID, "message1")
        self.description_error = (By.ID, "message17")
    
    def open_page(self, url):
         # Tìm phần tử có href chứa giá trị `url` và click để mở trang
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//a[contains(@href, '{url}')]"))
        )
        element.click()
        
    def enter_accountno(self, accountno):
        field = self.driver.find_element(*self.accountno_textbox)
        field.clear()
        field.send_keys(accountno)
        
    def enter_amount(self, amount):
        field = self.driver.find_element(*self.amount_textbox)
        field.clear()
        field.send_keys(amount)
        
    def enter_description(self, description):
        field = self.driver.find_element(*self.description_textbox)
        field.clear()
        field.send_keys(description)
        
    def click_submit(self):
        self.driver.find_element(*self.submit_button).click()
        
    def click_reset(self):
        self.driver.find_element(*self.reset_button).click()
        
    def find_element(self, *locator):
        return self.driver.find_element(*locator)
    
    def get_error_message(self, field_error_locator):
        return self.driver.find_element(*field_error_locator).text
        
        
        
        