from selenium.webdriver.common.by import By

class DepositPage:

    def __init__(self, driver):
        self.driver = driver
        self.accountno_textbox = (By.NAME, "accountno")
        self.amount_textbox = (By.NAME, "ammount")
        self.description_textbox = (By.NAME, "desc")
        self.submit_button = (By.XPATH, "//input[@value='Submit']")
        self.reset_button = (By.XPATH, "//input[@value='Reset']")
    
    def open_page(self, url):
        self.driver.get(url)

    def enter_accountno(self, accountno):
        self.driver.find_element(*self.accountno_textbox).send_keys(accountno)

    def enter_amount(self, amount):
        self.driver.find_element(*self.amount_textbox).send_keys(amount)

    def enter_description(self, description):
        self.driver.find_element(*self.description_textbox).send_keys(description)

    def click_submit(self):
        self.driver.find_element(*self.submit_button).click()
        
    def click_reset(self):
        self.driver.find_element(*self.reset_button).click()