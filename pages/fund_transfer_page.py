from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class FundTransferPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
   
        # Locators
        self.payer_account_field = (By.NAME, "payersaccount")
        self.payee_account_field = (By.NAME, "payeeaccount")
        self.amount_field = (By.NAME, "ammount")
        self.description_field = (By.NAME, "desc")
        self.submit_button = (By.NAME, "AccSubmit")
        self.reset_button = (By.NAME, "res")
        
        # Locators for error messages (these IDs may vary depending on actual implementation)
        self.heading_successfully = (By.CLASS_NAME, "heading3")
        self.payer_account_error = (By.ID, "message10")
        self.payee_account_error = (By.ID, "message11")
        self.amount_error = (By.ID, "message1")
        self.description_error = (By.ID, "message17")

    def open_page(self, url):
        # Tìm phần tử có href chứa giá trị `url` và click để mở trang
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//a[contains(@href, '{url}')]"))
        )
        element.click()

    def enter_payer_account(self, payer_account):
        field = self.driver.find_element(*self.payer_account_field)
        field.clear()
        field.send_keys(payer_account)
        
    def enter_payee_account(self, payee_account):
        field = self.driver.find_element(*self.payee_account_field)
        field.clear()
        field.send_keys(payee_account)

    def enter_amount(self, amount):
        field = self.driver.find_element(*self.amount_field)
        field.clear()
        field.send_keys(amount)

    def enter_description(self, description):
        field = self.driver.find_element(*self.description_field)
        field.clear()
        field.send_keys(description)
        
    def click_submit(self):
        self.driver.find_element(*self.submit_button).click()
        
    def click_reset(self):
        self.driver.find_element(*self.reset_button).click()

    def get_error_message(self, field_error_locator):
        return self.driver.find_element(*field_error_locator).text
