from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class NewAccountPage:

    def __init__(self, driver):
        self.driver = driver
        self.customer_id_textbox = (By.NAME, "cusid")
        self.account_type_combobox = (By.NAME, "selaccount")
        self.initial_deposit_textbox = (By.NAME, "inideposit")
        self.submit_button = (By.XPATH, "//input[@value='submit']")
        self.reset_button = (By.XPATH, "//input[@value='reset']")
        
        # error messages
        self.heading_successfully = (By.CLASS_NAME, "heading3")
        self.account_id_error = (By.ID, "message14")
        self.initial_deposit_error = (By.ID, "message19")
        
    
    def open_page(self, url):
        # Tìm phần tử có href chứa giá trị `url` và click để mở trang
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//a[contains(@href, '{url}')]"))
        )
        element.click()

    def enter_customer_id(self, customer_id):
        field = self.driver.find_element(*self.customer_id_textbox)
        field.clear()
        field.send_keys(customer_id)

    def select_account_type(self, account_type):
        select_element = Select(self.driver.find_element(*self.account_type_combobox))
        select_element.select_by_visible_text(account_type)  # Select by visible text
    
    def enter_initial_deposit(self, initial_deposit):
        field = self.driver.find_element(*self.initial_deposit_textbox)
        field.clear()
        field.send_keys(initial_deposit)

    def click_submit(self):
        self.driver.find_element(*self.submit_button).click()
    
    def get_error_message(self, field_error_locator):
        return self.driver.find_element(*field_error_locator).text    
    def click_reset(self):
        self.driver.find_element(*self.reset_button).click()
        
    def find_element(self, *locator):
        return self.driver.find_element(*locator)