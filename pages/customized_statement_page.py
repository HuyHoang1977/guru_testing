from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CustomizedStatementPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
   
        # Locators
        self.account_field = (By.NAME, "accountno")
        self.fdate_field = (By.NAME, "fdate")
        self.tdate_field = (By.NAME, "tdate")
        self.amount_lower_field = (By.NAME, "amountlowerlimit")
        self.numtransaction_field = (By.NAME, "numtransaction")
        self.submit_button = (By.NAME, "AccSubmit")
        self.reset_button = (By.NAME, "res")
        
        self.heading_successfully = (By.CLASS_NAME, "heading3")
        self.account_error = (By.ID, "message2")
        self.fdate_error = (By.ID, "message26")
        self.tdate_error = (By.ID, "message27")
        self.amount_lower_error = (By.ID, "message12")
        self.numtransaction_error = (By.ID, "message13")

    def open_page(self, url):
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//a[contains(@href, '{url}')]"))
        )
        element.click()

    def enter_account(self, payer_account):
        field = self.driver.find_element(*self.account_field)
        field.clear()
        field.send_keys(payer_account)
        
    def enter_fdate(self, fdate):
        field = self.driver.find_element(*self.fdate_field)
        field.clear()
        field.send_keys(fdate)
        
    def enter_tdate(self, tdate):
        field = self.driver.find_element(*self.tdate_field)
        field.clear()
        field.send_keys(tdate)
    
    def enter_amount_lower(self, amount_lower):
        field = self.driver.find_element(*self.amount_lower_field)
        field.clear()
        field.send_keys(amount_lower)
        
    def enter_numtransaction(self, numtransaction):
        field = self.driver.find_element(*self.numtransaction_field)
        field.clear()
        field.send_keys(numtransaction)
        
    def click_submit(self):
        self.driver.find_element(*self.submit_button).click()
        
    def click_reset(self):
        self.driver.find_element(*self.reset_button).click()

    def get_error_message(self, field_error_locator):
        return self.driver.find_element(*field_error_locator).text
